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
