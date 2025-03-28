# Test unnitarios para los algoritmos de la API de FastAPI en Python 

# tests/test_algorithms.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Usuario de prueba
test_user = {
    "username": "testuser",
    "password": "testpass"
}

# ----------- HELPER: Obtener token válido -----------
def get_token():
    # Primero registra el usuario de prueba
    client.post("/register", json=test_user)

    # Luego inicia sesión para obtener el token
    response = client.post("/login", json=test_user)
    assert response.status_code == 200
    return response.json()["access_token"]


# ----------- TEST: Ordenar burbuja -----------
def test_bubble_sort():
    token = get_token()
    payload = {"numbers": [5, 2, 9, 1]}
    response = client.post("/bubble-sort", json=payload, params={"token": token})

    assert response.status_code == 200
    assert response.json()["numbers"] == [1, 2, 5, 9]


# ----------- TEST: Filtrar números pares -----------
def test_filter_even():
    token = get_token()
    payload = {"numbers": [5, 2, 9, 4]}
    response = client.post("/filter-even", json=payload, params={"token": token})

    assert response.status_code == 200
    assert response.json()["even_numbers"] == [2, 4]


# ----------- TEST: Sumar elementos -----------
def test_sum_elements():
    token = get_token()
    payload = {"numbers": [1, 2, 3]}
    response = client.post("/sum-elements", json=payload, params={"token": token})

    assert response.status_code == 200
    assert response.json()["sum"] == 6


# ----------- TEST: Busqueda valor maximo  -----------
def test_max_value():
    token = get_token()
    payload = {"numbers": [4, 7, 2]}
    response = client.post("/max-value", json=payload, params={"token": token})

    assert response.status_code == 200
    assert response.json()["max"] == 7


# ----------- TEST: busqueda binaria -----------
def test_binary_search_found():
    token = get_token()
    payload = {"numbers": [1, 3, 5, 7, 9], "target": 5}
    response = client.post("/binary-search", json=payload, params={"token": token})

    assert response.status_code == 200
    assert response.json()["found"] is True
    assert response.json()["index"] == 2


# ----------- TEST:Busqueda Binaria (No encontrado) -----------
def test_binary_search_not_found():
    token = get_token()
    payload = {"numbers": [1, 3, 5, 7, 9], "target": 8}
    response = client.post("/binary-search", json=payload, params={"token": token})

    assert response.status_code == 200
    assert response.json()["found"] is False
    assert response.json()["index"] == -1
