# CAP06_CHALLENGE : Testing con AI 

Este repositorio contiene la solución a la Parte 1 del challenge de Testing con Inteligencia Artificial. El objetivo es evaluar, testear y mejorar una función que determina si un número es primo, aplicando pruebas unitarias exhaustivas con `pytest`.

---

## Estructura del Proyecto

```
parte1/
├── challenge.md       # Instrucciones originales del reto
├── func.py            # Implementación de la función `es_primo`
├── func_test.py       # Pruebas unitarias desarrolladas por el participante
└── reference_test.py  # Pruebas oficiales de validación (solo lectura)
```

---

## Requisitos

- Python 3.8 o superior
- `pytest` instalado

```bash
pip install pytest
```

---

## Función Principal: `es_primo(num)`

Determina si un número es primo. Acepta solo números enteros positivos mayores o iguales a 2. Lanza un `TypeError` si se proporciona un tipo inválido.

---

## Pruebas Incluidas

### Pruebas del Desarrollador (`func_test.py`)

Cubre los siguientes casos:

- Primos conocidos (2, 3, 5, ..., 31)
- No primos conocidos (0, 1, 4, 6, ..., 20)
- Números negativos
- Números grandes (ej: 1000003)
- Tipos inválidos (strings, floats, None, listas)
- Inputs especiales como booleanos y flotantes cercanos a enteros

```bash
pytest parte1/func_test.py
```

###  Pruebas Oficiales (`reference_test.py`)

No deben modificarse. Evalúan automáticamente si la función cumple con los criterios del challenge.

```bash
pytest parte1/reference_test.py
```

---

## Objetivo

Desarrollar una función robusta y test-driven que pase todas las pruebas oficiales, aplicando buenas prácticas de testing, manejo de errores y eficiencia algorítmica.

---

## Progreso

- [x] Función `es_primo` optimizada
- [x] Pruebas unitarias implementadas
- [x] Manejo de errores validado
- [x] Pruebas oficiales superadas

---

##  Autor

**Jorge Sislema**  
Bootcamp Henry – Data Science  


---

