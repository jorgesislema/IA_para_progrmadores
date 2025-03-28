# FastAPI Algorithms API - Challenge Copilotos

Este proyecto implementa una API en FastAPI que incluye algoritmos clásicos (ordenamiento, búsqueda, etc.) y autenticación básica con tokens JWT, todo desarrollado con el apoyo de copilotos de código como parte del reto CAP01_CHALLENGE.

## 🚀 Tecnologías usadas
- **FastAPI**
- **Pydantic**
- **Passlib**
- **PyJWT (jose)**
- **pytest**

---

## 🛠 Instalación y ejecución

### 1. Crear entorno virtual
```bash
python -m venv venv
```

### 2. Activar entorno virtual
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación localmente
```bash
uvicorn app.main:app --reload
```

### 5. Ver documentación interactiva
Abre tu navegador en:
```
http://localhost:8000/docs
```

---

## 🔐 Autenticación (JWT)

### 🔸 Registro de usuario
```
POST /register
Body:
{
  "username": "usuario",
  "password": "clave"
}
```

### 🔸 Login de usuario
```
POST /login
Body:
{
  "username": "usuario",
  "password": "clave"
}
```
**Respuesta:**
```json
{
  "access_token": "<TOKEN>",
  "token_type": "bearer"
}
```

### 🔸 Uso de token
Todos los endpoints requieren el token como **parámetro de consulta**:
```
?token=<TOKEN>
```

---

## 📘 Endpoints de algoritmos
Todos los métodos son `POST` y esperan un JSON con `numbers`.

### ✅ /bubble-sort
Ordena la lista con Bubble Sort.
```json
{
  "numbers": [5, 3, 1]
}
```

### ✅ /filter-even
Devuelve solo los números pares.

### ✅ /sum-elements
Suma todos los elementos de la lista.

### ✅ /max-value
Devuelve el número más alto.

### ✅ /binary-search
Busca un número usando búsqueda binaria.
```json
{
  "numbers": [1, 3, 5, 7],
  "target": 5
}
```

---

## 🧪 Pruebas Automatizadas

Ejecuta todas las pruebas con:
```bash
pytest
```

Incluye:
- `tests/test_auth.py`: Validación de login, registro y uso de tokens.
- `tests/test_algorithms.py`: Verifica el funcionamiento de cada endpoint.

---

## 🐳 Docker

### Construir imagen
```bash
docker build -t fastapi-algorithms-api .
```

### Ejecutar contenedor
```bash
docker run -d -p 8000:8000 fastapi-algorithms-api
```

### Acceder a la API
```
http://localhost:8000/docs
```

---

## 📌 Notas finales
- Este proyecto fue construido paso a paso con ayuda de un copiloto de código.
- Los tokens se pasan como **query parameters** por simplicidad educativa. En producción se recomienda usar headers.

---

### 🧠 Desarrollado para: CAP01_CHALLENGE
Con foco en aprendizaje práctico, seguridad básica y documentación.

---
