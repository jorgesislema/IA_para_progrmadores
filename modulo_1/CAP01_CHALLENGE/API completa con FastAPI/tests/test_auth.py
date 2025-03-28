# tests/test_auth.py

from fastapi.testclient import TestClient
from app.main import app

cliente = TestClient(app)

usuario_prueba = {
    "username": "usuario_test",
    "password": "clave_test"
}

# ----------- TEST:  Registro exitoso de usuario ----------
def test_registro_usuario():
    respuesta = cliente.post("/register", json=usuario_prueba)
    assert respuesta.status_code in [200, 400]  
    if respuesta.status_code == 200:
        assert respuesta.json()["message"] == "User registered successfully"
    elif respuesta.status_code == 400:
        assert respuesta.json()["detail"] == "El usuario ya existe"

# ---------- TEST:Login exitoso-----------
def test_login_correcto():
    respuesta = cliente.post("/login", json=usuario_prueba)
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "access_token" in datos
    assert datos["token_type"] == "bearer"

# ----------- TEST: Login fallido por contraseña incorrecta----------
def test_login_incorrecto():
    respuesta = cliente.post("/login", json={
        "username": "usuario_test",
        "password": "clave_incorrecta"
    })
    assert respuesta.status_code == 401
    assert respuesta.json()["detail"] == "Credenciales inválidas"

# ----------- TEST: Token se recibe y es válido-----------
def test_obtener_token_y_usarlo():
    login = cliente.post("/login", json=usuario_prueba)
    token = login.json()["access_token"]

    payload = {"numbers": [3, 1, 2]}
    respuesta = cliente.post("/bubble-sort", json=payload, params={"token": token})
    assert respuesta.status_code == 200
    assert respuesta.json()["numbers"] == [1, 2, 3]
