# Description: Módulo de autenticación de usuarios
#librerias necesarias
from fastapi import APIRouter, HTTPException, Request
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.models import UserRegister, Token

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
fake_users_db = {}

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username not in fake_users_db:
            raise HTTPException(status_code=401, detail="Usuario inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.post("/register")
def register(user: UserRegister):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    hashed_pw = hash_password(user.password)
    fake_users_db[user.username] = {"username": user.username, "hashed_password": hashed_pw}
    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: UserRegister):
    db_user = fake_users_db.get(user.username)
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = create_access_token({"sub": user.username})
    return {"access_token": token}

