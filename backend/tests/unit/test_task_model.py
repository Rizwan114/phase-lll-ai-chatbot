import pytest
from datetime import datetime
from src.models.task_model import Task, TaskCreate


def test_task_creation():
    """Test creating a task model instance"""
    task_create = TaskCreate(
        title="Test Task",
        description="Test Description",
        completed=False,
        user_id="user123"
    )

    assert task_create.title == "Test Task"
    assert task_create.description == "Test Description"
    assert task_create.completed == False
    assert task_create.user_id == "user123"


def test_task_required_fields():
    """Test that required fields are enforced"""
    # Title is required
    with pytest.raises(ValueError):
        TaskCreate(
            title="",  # Empty title should fail
            completed=False,
            user_id="user123"
        )

    # user_id is required
    with pytest.raises(ValueError):
        TaskCreate(
            title="Test Task",
            completed=False,
            user_id=""  # Empty user_id should fail
        )


def test_task_optional_fields():
    """Test that optional fields can be None"""
    task_create = TaskCreate(
        title="Test Task",
        completed=False,
        user_id="user123"
        # description is optional, so we don't provide it
    )

    assert task_create.title == "Test Task"
    assert task_create.description is None
    assert task_create.completed == False
    assert task_create.user_id == "user123"