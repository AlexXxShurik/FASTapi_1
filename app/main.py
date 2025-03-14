from fastapi import FastAPI, WebSocket, HTTPException
from uuid import UUID
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate
from app.crud import get_tasks, get_task, create_task, update_task, delete_task
from app.celery_worker import send_report_task
from app.websocket_manager import manager


app = FastAPI()

@app.get("/tasks")
def read_tasks():
    return get_tasks()


@app.get("/tasks/{task_id}")
def read_task(task_id: UUID):
    task = get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks")
def add_task(task: TaskCreate):
    new_task = Task(**task.model_dump())
    return create_task(new_task)


@app.put("/tasks/{task_id}")
def update_task_endpoint(task_id: UUID, updated_task: TaskUpdate):
    task = get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    updated_data = updated_task.model_dump(exclude_unset=True)
    updated_task = task.copy(update=updated_data)
    return update_task(task_id, updated_task)


@app.delete("/tasks/{task_id}")
def remove_task(task_id: UUID):
    if not delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}


@app.post("/tasks/send_report")
def send_report(email: str):
    task = send_report_task.delay(email)
    return {"task_id": task.id}


@app.websocket("/ws/tasks")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        manager.disconnect(websocket)