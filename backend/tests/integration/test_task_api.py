import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from unittest.mock import patch
from src.main import app
from src.database.database import engine
from src.models.task_model import Task
from src.auth.middleware import get_current_user_from_token


def override_get_current_user():
    """Override auth dependency to return test user"""
    return "test_user"


@pytest.fixture(name="client")
def client_fixture():
    """Create a test client with an in-memory database"""
    # Create an in-memory SQLite database for testing
    test_engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(bind=test_engine)

    # Override the engine and auth dependency
    app.dependency_overrides[get_current_user_from_token] = override_get_current_user

    with patch("src.database.database.engine", test_engine):
        with TestClient(app) as client:
            yield client

    # Clean up overrides
    app.dependency_overrides.clear()


def test_create_task(client):
    """Test creating a task via the API"""
    response = client.post(
        "/api/test_user/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "completed": False
        },
        headers={"Authorization": "Bearer test-token"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] == False
    assert data["user_id"] == "test_user"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_tasks(client):
    """Test getting tasks for a user"""
    # First create a task
    create_response = client.post(
        "/api/test_user/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "completed": False
        },
        headers={"Authorization": "Bearer test-token"}
    )

    assert create_response.status_code == 201

    # Then get tasks
    response = client.get(
        "/api/test_user/tasks",
        headers={"Authorization": "Bearer test-token"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "tasks" in data
    assert len(data["tasks"]) >= 1
    assert data["tasks"][0]["title"] == "Test Task"


def test_get_specific_task(client):
    """Test getting a specific task"""
    # First create a task
    create_response = client.post(
        "/api/test_user/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "completed": False
        },
        headers={"Authorization": "Bearer test-token"}
    )

    assert create_response.status_code == 201
    created_task = create_response.json()
    task_id = created_task["id"]

    # Then get the specific task
    response = client.get(
        f"/api/test_user/tasks/{task_id}",
        headers={"Authorization": "Bearer test-token"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["id"] == task_id


def test_update_task(client):
    """Test updating a task"""
    # First create a task
    create_response = client.post(
        "/api/test_user/tasks",
        json={
            "title": "Original Task",
            "description": "Original Description",
            "completed": False
        },
        headers={"Authorization": "Bearer test-token"}
    )

    assert create_response.status_code == 201
    created_task = create_response.json()
    task_id = created_task["id"]

    # Then update the task
    response = client.put(
        f"/api/test_user/tasks/{task_id}",
        json={
            "title": "Updated Task",
            "description": "Updated Description",
            "completed": True
        },
        headers={"Authorization": "Bearer test-token"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated Description"
    assert data["completed"] == True


def test_delete_task(client):
    """Test deleting a task"""
    # First create a task
    create_response = client.post(
        "/api/test_user/tasks",
        json={
            "title": "Task to Delete",
            "description": "Description",
            "completed": False
        },
        headers={"Authorization": "Bearer test-token"}
    )

    assert create_response.status_code == 201
    created_task = create_response.json()
    task_id = created_task["id"]

    # Then delete the task
    response = client.delete(
        f"/api/test_user/tasks/{task_id}",
        headers={"Authorization": "Bearer test-token"}
    )

    assert response.status_code == 204  # No content

    # Verify the task is gone
    get_response = client.get(
        f"/api/test_user/tasks/{task_id}",
        headers={"Authorization": "Bearer test-token"}
    )
    assert get_response.status_code == 404
