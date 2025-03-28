
# Importamos FastAPI y las rutas de los algoritmos y autenticación
# app/main.py

from fastapi import FastAPI
from app.algorithms import router as algo_router
from app.auth import router as auth_router

app = FastAPI(title="FastAPI Algorithms API")

# Incluir rutas de algoritmos y autenticación
app.include_router(algo_router)
app.include_router(auth_router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "API funcionando correctamente"}

