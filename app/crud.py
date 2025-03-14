from uuid import UUID
from typing import Optional
from app.models import Task


tasks_db: list[Task] = []

def get_tasks() -> list[Task]:
    return tasks_db

def get_task(task_id: UUID) -> Optional[Task]:
    return next((task for task in tasks_db if task.id == task_id), None)

def create_task(task: Task) -> Task:
    tasks_db.append(task)
    return task

def update_task(task_id: UUID, updated_task: Task) -> Optional[Task]:
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db[i] = updated_task
            return tasks_db[i]
    return None

def delete_task(task_id: UUID) -> bool:
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db.pop(i)
            return True
    return False