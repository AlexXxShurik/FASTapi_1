from unittest.mock import patch

import pytest
import websockets
from fastapi.testclient import TestClient
from uuid import uuid4
from app.models import Task
from app.main import app

client = TestClient(app)

@pytest.fixture
def test_task():
    return Task(id=uuid4(), title="Test Task", description="This is a test task", completed=False)


def test_read_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_task(test_task):
    task_id = test_task.id
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404


def test_add_task():
    task_data = {"title": "New Task", "description": "This is a new task", "completed": False}
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 200
    assert response.json()["title"] == task_data["title"]


def test_update_task_endpoint(test_task):
    task_id = test_task.id
    updated_data = {"title": "Updated Task"}
    response = client.put(f"/tasks/{task_id}", json=updated_data)
    assert response.status_code == 404


def test_remove_task(test_task):
    task_id = test_task.id
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 404


def test_send_report():
    email = "test@example.com"

    with patch("app.celery_worker.send_report_task.delay") as mock_task:
        fake_task = type("FakeTask", (), {"id": "fake-task-id"})
        mock_task.return_value = fake_task

        response = client.post("/tasks/send_report", params={"email": email})

        mock_task.assert_called_once_with(email)

        assert response.status_code == 200
        assert response.json() == {"task_id": "fake-task-id"}


@pytest.mark.asyncio
async def test_websocket_endpoint():
    async with websockets.connect("ws://localhost:8000/ws/tasks") as websocket:
        await websocket.send("Test message")
        response = await websocket.recv()
        assert response == "Message received: Test message"