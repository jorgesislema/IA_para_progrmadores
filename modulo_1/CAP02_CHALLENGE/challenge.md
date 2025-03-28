# CAP02_CHALLENGE

Este challenge está diseñado para que aprendas a enfrentarte a un repositorio relativamente grande por primera vez, con la ayuda de un asistente como Cody.

## Explora

1. Crea un nuevo Chat con Cody.
2. Haciendo referencia al `main.py` dentro de `/app`, pregúntale de qué trata el aplicativo.
   - Ejemplo: `@CAP02_CHALLENGE/path/to/file ¿Qué hace esta app?`

   Esta aplicación parece ser una API REST para gestionar tareas (tasks) utilizando FastAPI. La aplicación implementa un sistema CRUD (Create, Read, Update, Delete) para tareas con las siguientes funcionalidades:

Crear tareas (POST /): Permite añadir nuevas tareas al sistema.
Obtener una tarea específica (GET /{task_id}): Recupera una tarea por su ID.
Listar todas las tareas (GET /): Obtiene todas las tareas almacenadas.
Actualizar tareas (PUT /{task_id}): Modifica una tarea existente.
Eliminar tareas (DELETE /{task_id}): Borra una tarea del sistema.
La aplicación utiliza:

FastAPI como framework web
Un sistema de modelos para definir la estructura de las tareas (Task, UpdateTaskModel, TaskList)
Un módulo de base de datos (db) para persistir la información
El archivo main.py probablemente contiene el código para iniciar la aplicación FastAPI, configurar el enrutador de tareas (tasks_router) y posiblemente otras configuraciones como middleware, documentación automática (Swagger/OpenAPI), etc.

En resumen, es una aplicación de gestión de tareas (todo list) implementada como una API REST con FastAPI

### Haciendo uso de Cody, encuentra las respuestas a:

#### 3.1 ¿Qué hace el archivo `tasks_router.py`?

El archivo `tasks_router.py` define un enrutador (router) de FastAPI que maneja todas las operaciones relacionadas con las tareas en la aplicación. Su propósito principal es implementar los endpoints de la API REST para gestionar tareas, siguiendo el patrón CRUD (Create, Read, Update, Delete).

Específicamente, el archivo:
- Define un enrutador de FastAPI: `tasks_router = APIRouter()`
- Implementa los siguientes endpoints:
  - `POST /`: Crea una nueva tarea
  - `GET /{task_id}`: Obtiene una tarea específica por su ID
  - `GET /`: Lista todas las tareas disponibles
  - `PUT /{task_id}`: Actualiza una tarea existente
  - `DELETE /{task_id}`: Elimina una tarea
- Interactúa con la capa de datos (`db`)
- Maneja errores HTTP (ej. 404 cuando no se encuentra una tarea)
- Define modelos de respuesta para asegurar consistencia

#### 3.2 ¿Cuáles son los diferentes endpoints y qué hacen?

- **POST /**: Crea una nueva tarea
- **GET /{task_id}**: Obtiene una tarea por ID
- **GET /**: Lista todas las tareas
- **PUT /{task_id}**: Actualiza una tarea existente
- **DELETE /{task_id}**: Elimina una tarea específica

#### 3.3 ¿Cómo está construida la base de datos?

La base de datos está implementada mediante un módulo llamado `db`, que expone métodos CRUD:

```python
from db import db
```

- `db.add_task(task)`
- `db.get_task(task_id)`
- `db.get_tasks()`
- `db.update_task(task_id, task_update)`
- `db.delete_task(task_id)`

La base de datos usa modelos de datos definidos en `models.py`. Su implementación podría ser:
- En memoria (lista o diccionario)
- Archivos JSON
- Base de datos SQL (usando ORM)
- Base de datos NoSQL (como MongoDB)

Este enfoque desacopla la lógica de acceso a datos de la lógica de API.

#### 3.4 ¿Cómo se inicializa el aplicativo?

- Se importa FastAPI y el router de tareas.
- Se crea la instancia `app = FastAPI()`
- Se incluye el router con `app.include_router(tasks_router, prefix="/tasks")`
- Se define un endpoint raíz `/`
- FastAPI configura todas las rutas y empieza a escuchar con Uvicorn.

## Extiende

### 1. Añadir endpoint para eliminar todos los registros

1. Añadir método `delete_all_tasks()` en `FakeDB`:

```python
def delete_all_tasks(self):
    self.tasks = []
    return {"message": "All tasks deleted successfully"}
```

2. Añadir endpoint:

```python
@tasks_router.delete("/")
async def delete_all_tasks():
    result = db.delete_all_tasks()
    return result
```

### 2. Documentar el módulo `app/routers/tasks_router.py`

Documentación agregada en cada función del archivo para describir parámetros, retornos y excepciones.

## Corrige

### 1. Mejoras sugeridas con "Code Smells"

- Añadir endpoint `DELETE /` para eliminar todas las tareas
- Implementar paginación en `GET /`
- Añadir endpoint de búsqueda por título o descripción
- Añadir endpoint `PATCH /{task_id}/toggle` para marcar tareas como completadas o pendientes
- Validación de entradas y mejor manejo de errores usando `Path`, `Query`, `Body`

### 2. Implementación de mejoras sugeridas

- Se agregaron validaciones con `status`, `Query`, `Path`, `Body`
- Se implementó búsqueda (`/search?q=texto`)
- Se paginó el listado de tareas con `skip` y `limit`
- Se implementó `PATCH` para cambiar estado completado
- Se documentó el módulo con docstrings detallados en español

## 3.4 ¿Cómo se inicializa el aplicativo?

### Explicación del proceso de inicialización

**Importación de dependencias:**

- Se importa FastAPI del paquete fastapi
- Se importa tasks_router del módulo routers.tasks_router

**Creación de la instancia principal:**

- Se crea una instancia de FastAPI con app = FastAPI()

**Registro del router de tareas:**

- Se incluye el router de tareas en la aplicación principal usando app.include_router()
- Se especifica el prefijo /tasks para todas las rutas definidas en ese router
- Se asigna la etiqueta "tasks" para organizar la documentación automática

**Definición de la ruta raíz:**

- Se define un endpoint en la ruta raíz (/) que devuelve un mensaje simple
- Este endpoint sirve como una página de bienvenida o verificación de que la API está funcionando

**Funcionamiento**

Cuando se inicia la aplicación:

- FastAPI configura todas las rutas, incluyendo:
  - La ruta raíz / que muestra el mensaje de bienvenida
  - Todas las rutas de tareas bajo el prefijo /tasks (como /tasks/, /tasks/{task_id}, etc.)
- El servidor web (típicamente Uvicorn) comienza a escuchar solicitudes HTTP

Cuando llega una solicitud, FastAPI la dirige al controlador apropiado:

- Si la ruta comienza con /tasks, la solicitud se dirige al tasks_router
- Si la ruta es exactamente /, se maneja con la función root()

Este código sigue el patrón recomendado para estructurar aplicaciones FastAPI, separando las rutas en módulos específicos (routers) y manteniendo el archivo principal limpio y enfocado en la configuración de la aplicación

## Extiende

### 1. Añade un nuevo endpoint al aplicativo que permita eliminar TODOS los registros de db.

**Añadir un endpoint para eliminar todos los registros**

Para añadir un nuevo endpoint que permita eliminar todos los registros de la base de datos, necesitamos hacer dos cosas:

**Añadir un método a la clase FakeDB para eliminar todos los registros**

```python
def delete_all_tasks(self):
    self.tasks = []
    return {"message": "All tasks deleted successfully"}
```

Este método simplemente vacía la lista de tareas y devuelve un mensaje de confirmación.

**Crear un nuevo endpoint en el router de tareas que llame a este método**

```python
from fastapi import APIRouter, HTTPException
from models import Task, UpdateTaskModel, TaskList
from db import db

tasks_router = APIRouter()

@tasks_router.post("/", response_model=Task)
async def create_task(task: Task):
    return db.add_task(task)

@tasks_router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int):
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@tasks_router.get("/", response_model=TaskList)
async def get_tasks():
    tasks = db.get_tasks()
    return TaskList(tasks=tasks)

@tasks_router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: UpdateTaskModel):
    updated_task = db.update_task(task_id, task_update)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@tasks_router.delete("/{task_id}")
async def delete_task(task_id: int):
    db.delete_task(task_id)
    return {"message": "Task deleted successfully"}

@tasks_router.delete("/")
async def delete_all_tasks():
    """Delete all tasks from the database"""
    result = db.delete_all_tasks()
    return result
```

**Explicación**

- El nuevo endpoint usa el método HTTP DELETE en la ruta base ("/")
- Cuando se llama a este endpoint, se ejecuta la función delete_all_tasks()
- Esta función llama al método delete_all_tasks() de la base de datos
- El método de la base de datos vacía la lista de tareas
- Se devuelve un mensaje de confirmación al cliente

Este endpoint permitirá eliminar todas las tareas con una sola solicitud HTTP DELETE a la ruta /tasks/.
## 2. Documenta el módulo `app/routers/tasks_router.py`

```python
from fastapi import APIRouter, HTTPException
from models import Task, UpdateTaskModel, TaskList
from db import db

tasks_router = APIRouter()

"""
Crear una nueva tarea.

Agrega una tarea a la base de datos y devuelve la tarea creada.

Parámetros:
    task (Task): La tarea que se va a crear.

Devuelve:
    Task: La tarea recién creada con los campos generados automáticamente por el servidor.
"""
@tasks_router.post("/", response_model=Task)
async def create_task(task: Task):
    return db.add_task(task)

"""
Obtener una tarea específica por su ID.

Busca una tarea en la base de datos usando el ID proporcionado.
Lanza una excepción HTTP 404 si no se encuentra la tarea.

Parámetros:
    task_id (int): El identificador único de la tarea a recuperar.

Devuelve:
    Task: La tarea con el ID especificado.

Excepciones:
    HTTPException: Si no se encuentra una tarea con el ID proporcionado.
"""
@tasks_router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int):
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task

"""
Obtener todas las tareas.

Recupera todas las tareas de la base de datos y las devuelve como una lista.

Devuelve:
    TaskList: Una lista que contiene todas las tareas en la base de datos.
"""
@tasks_router.get("/", response_model=TaskList)
async def get_tasks():
    tasks = db.get_tasks()
    return TaskList(tasks=tasks)

"""
Actualizar una tarea existente.

Actualiza una tarea en la base de datos con el ID y los datos proporcionados.

Parámetros:
    task_id (int): El identificador único de la tarea a actualizar.
    task_update (UpdateTaskModel): Los datos que se desean actualizar para la tarea.

Devuelve:
    Task: La tarea actualizada con los campos modificados.

Excepciones:
    HTTPException: Si no se encuentra una tarea con el ID proporcionado.
"""
@tasks_router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: UpdateTaskModel):
    updated_task = db.update_task(task_id, task_update)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return updated_task

"""
Eliminar una tarea.

Elimina una tarea de la base de datos con el ID especificado.

Parámetros:
    task_id (int): El identificador único de la tarea a eliminar.

Devuelve:
    dict: Un mensaje de confirmación indicando que la tarea fue eliminada exitosamente.
"""
@tasks_router.delete("/{task_id}")
async def delete_task(task_id: int):
    db.delete_task(task_id)
    return {"message": "Tarea eliminada exitosamente"}
```

---

## Corrige

### 1. Mejoras potenciales identificadas con "Code Smells"

#### 1.1. Endpoint para eliminar todas las tareas
```python
"""
Eliminar todas las tareas.

Elimina todas las tareas de la base de datos.

Devuelve:
    dict: Un mensaje de confirmación indicando que todas las tareas fueron eliminadas exitosamente.
"""
@tasks_router.delete("/")
async def delete_all_tasks():
    db.delete_all_tasks()
    return {"message": "Todas las tareas eliminadas exitosamente"}
```

#### 1.2. Paginación para listar tareas
```python
"""
Obtener todas las tareas con paginación.

Recupera las tareas de la base de datos y las devuelve como una lista paginada.

Parámetros:
    skip (int): Número de tareas a omitir (para paginación).
    limit (int): Número máximo de tareas a devolver.

Devuelve:
    TaskList: Una lista paginada que contiene las tareas en la base de datos.
"""
@tasks_router.get("/", response_model=TaskList)
async def get_tasks(skip: int = 0, limit: int = 10):
    tasks = db.get_tasks(skip=skip, limit=limit)
    total = db.count_tasks()
    return TaskList(tasks=tasks, total=total, skip=skip, limit=limit)
```

#### 1.3. Búsqueda por texto
```python
"""
Buscar tareas por texto.

Busca tareas que contengan el texto especificado en su título o descripción.

Parámetros:
    q (str): Texto a buscar en las tareas.

Devuelve:
    TaskList: Una lista de tareas que coinciden con el criterio de búsqueda.
"""
@tasks_router.get("/search/", response_model=TaskList)
async def search_tasks(q: str):
    tasks = db.search_tasks(q)
    return TaskList(tasks=tasks)
```

#### 1.4. Cambiar estado de completado
```python
"""
Cambiar el estado de completado de una tarea.

Actualiza el estado de completado de una tarea existente.

Parámetros:
    task_id (int): El identificador único de la tarea a actualizar.
    completed (bool): El nuevo estado de completado.

Devuelve:
    Task: La tarea actualizada con el nuevo estado de completado.

Excepciones:
    HTTPException: Si no se encuentra una tarea con el ID proporcionado.
"""
@tasks_router.patch("/{task_id}/toggle", response_model=Task)
async def toggle_task_completion(task_id: int, completed: bool):
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    task_update = UpdateTaskModel(completed=completed)
    updated_task = db.update_task(task_id, task_update)
    return updated_task
```

#### 1.5. Validaciones adicionales
```python
from fastapi import APIRouter, HTTPException, Path, Body, Query, status

@tasks_router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: Task = Body(..., example={"title": "Nueva tarea", "description": "Descripción de la tarea", "completed": False})):
    if not task.title or task.title.isspace():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El título de la tarea no puede estar vacío"
        )
    return db.add_task(task)

@tasks_router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int = Path(..., gt=0, description="El ID de la tarea debe ser mayor que 0")):
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    return task

## 2. Implementa alguna de las mejoras propuestas por Cody AI

```python
from fastapi import APIRouter, HTTPException, Path, Body, Query, status
from models import Task, UpdateTaskModel, TaskList
from db import db


tasks_router = APIRouter()

"""
Crear una nueva tarea.

Agrega una tarea a la base de datos y devuelve la tarea creada.

Parámetros:
    task (Task): La tarea que se va a crear.

Devuelve:
    Task: La tarea recién creada con los campos generados automáticamente por el servidor.
"""
@tasks_router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: Task = Body(..., example={"title": "Nueva tarea", "description": "Descripción de la tarea", "completed": False})):
    if not task.title or task.title.isspace():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El título de la tarea no puede estar vacío"
        )
    return db.add_task(task)


"""
Obtener una tarea específica por su ID.

Busca una tarea en la base de datos usando el ID proporcionado.
Lanza una excepción HTTP 404 si no se encuentra la tarea.

Parámetros:
    task_id (int): El identificador único de la tarea a recuperar.

Devuelve:
    Task: La tarea con el ID especificado.

Excepciones:
    HTTPException: Si no se encuentra una tarea con el ID proporcionado.
"""
@tasks_router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int = Path(..., gt=0, description="El ID de la tarea debe ser mayor que 0")):
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    return task


"""
Obtener todas las tareas con paginación.

Recupera las tareas de la base de datos y las devuelve como una lista paginada.

Parámetros:
    skip (int): Número de tareas a omitir (para paginación).
    limit (int): Número máximo de tareas a devolver.

Devuelve:
    TaskList: Una lista paginada que contiene las tareas en la base de datos.
"""
@tasks_router.get("/", response_model=TaskList)
async def get_tasks(
    skip: int = Query(0, ge=0, description="Número de tareas a omitir"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de tareas a devolver")
):
    tasks = db.get_tasks()
    total = len(tasks)
    # Implementar paginación (asumiendo que get_tasks no tiene parámetros de paginación)
    paginated_tasks = tasks[skip:skip + limit]
    return TaskList(tasks=paginated_tasks, total=total, skip=skip, limit=limit)


"""
Buscar tareas por texto.

Busca tareas que contengan el texto especificado en su título o descripción.

Parámetros:
    q (str): Texto a buscar en las tareas.

Devuelve:
    TaskList: Una lista de tareas que coinciden con el criterio de búsqueda.
"""
@tasks_router.get("/search/", response_model=TaskList)
async def search_tasks(q: str = Query(..., min_length=1, description="Texto a buscar en las tareas")):
    tasks = db.get_tasks()
    q = q.lower()

    # Filtrar tareas que contienen el texto de búsqueda
    matching_tasks = [
        task for task in tasks 
        if q in task.title.lower() or 
           (hasattr(task, 'description') and task.description and q in task.description.lower())
    ]

    return TaskList(tasks=matching_tasks, total=len(matching_tasks), skip=0, limit=len(matching_tasks))


"""
Actualizar una tarea existente.

Actualiza una tarea en la base de datos con el ID y los datos proporcionados.

Parámetros:
    task_id (int): El identificador único de la tarea a actualizar.
    task_update (UpdateTaskModel): Los datos que se desean actualizar para la tarea.

Devuelve:
    Task: La tarea actualizada con los campos modificados.

Excepciones:
    HTTPException: Si no se encuentra una tarea con el ID proporcionado.
"""
@tasks_router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: int = Path(..., gt=0, description="El ID de la tarea debe ser mayor que 0"),
    task_update: UpdateTaskModel = Body(...)
):
    updated_task = db.update_task(task_id, task_update)
    if updated_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    return updated_task


"""
Cambiar el estado de completado de una tarea.

Actualiza el estado de completado de una tarea existente.

Parámetros:
    task_id (int): El identificador único de la tarea a actualizar.
    completed (bool): El nuevo estado de completado.

Devuelve:
    Task: La tarea actualizada con el nuevo estado de completado.

Excepciones:
    HTTPException: Si no se encuentra una tarea con el ID proporcionado.
"""
@tasks_router.patch("/{task_id}/toggle", response_model=Task)
async def toggle_task_completion(
    task_id: int = Path(..., gt=0),
    completed: bool = Body(..., embed=True)
):
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )

    task_update = UpdateTaskModel(completed=completed)
    updated_task = db.update_task(task_id, task_update)
    return updated_task


"""
Eliminar una tarea.

Elimina una tarea de la base de datos con el ID especificado.

Parámetros:
    task_id (int): El identificador único de la tarea a eliminar.

Devuelve:
    dict: Un mensaje de confirmación indicando que la tarea fue eliminada exitosamente.
"""
@tasks_router.delete("/{task_id}")
async def delete_task(task_id: int = Path(..., gt=0)):
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )

    db.delete_task(task_id)
    return {"message": "Tarea eliminada exitosamente"}


"""
Eliminar todas las tareas.

Elimina todas las tareas de la base de datos.

Devuelve:
    dict: Un mensaje de confirmación indicando que todas las tareas fueron eliminadas exitosamente.
"""
@tasks_router.delete("/")
async def delete_all_tasks():
    # Asumiendo que necesitamos implementar este método en la clase FakeDB
    db.tasks = []
    return {"message": "Todas las tareas eliminadas exitosamente"}
```
