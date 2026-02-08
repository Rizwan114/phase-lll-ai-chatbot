import json
import sys
import os

# Add the backend directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from mcp.server.fastmcp import FastMCP
from sqlmodel import Session
from backend.src.database.database import engine
from backend.src.models.task_model import TaskCreate, TaskUpdate
from backend.src.services.task_service import TaskService

mcp = FastMCP("todo-task-manager")


@mcp.tool()
def add_task(user_id: str, title: str, description: str | None = None) -> str:
    """Create a new task for the user.

    Args:
        user_id: The ID of the user who owns the task.
        title: The title of the task (1-255 chars).
        description: Optional description of the task (0-1000 chars).
    """
    if not user_id or not user_id.strip():
        return json.dumps({"status": "error", "message": "user_id is required"})
    if not title or not title.strip():
        return json.dumps({"status": "error", "message": "Title is required"})
    if len(title) > 255:
        return json.dumps({"status": "error", "message": "Title must be 255 characters or fewer"})
    if description and len(description) > 1000:
        return json.dumps({"status": "error", "message": "Description must be 1000 characters or fewer"})

    try:
        with Session(engine) as session:
            task_create = TaskCreate(
                title=title.strip(),
                description=description.strip() if description else None,
                user_id=user_id,
            )
            task = TaskService.create_task(session, task_create)
            return json.dumps({
                "status": "success",
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat(),
                },
            })
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


@mcp.tool()
def list_tasks(user_id: str) -> str:
    """List all tasks for the user.

    Args:
        user_id: The ID of the user whose tasks to list.
    """
    if not user_id or not user_id.strip():
        return json.dumps({"status": "error", "message": "user_id is required"})

    try:
        with Session(engine) as session:
            tasks = TaskService.get_tasks_by_user(session, user_id)
            return json.dumps({
                "status": "success",
                "tasks": [
                    {
                        "id": t.id,
                        "title": t.title,
                        "description": t.description,
                        "completed": t.completed,
                        "created_at": t.created_at.isoformat(),
                    }
                    for t in tasks
                ],
                "count": len(tasks),
            })
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


@mcp.tool()
def complete_task(user_id: str, task_id: int) -> str:
    """Mark a task as completed (toggle).

    Args:
        user_id: The ID of the user who owns the task.
        task_id: The ID of the task to complete.
    """
    if not user_id or not user_id.strip():
        return json.dumps({"status": "error", "message": "user_id is required"})
    if task_id < 1:
        return json.dumps({"status": "error", "message": "task_id must be a positive integer"})

    try:
        with Session(engine) as session:
            task = TaskService.toggle_task_completion(session, task_id, user_id)
            if not task:
                return json.dumps({
                    "status": "error",
                    "message": f"Task with ID {task_id} not found for this user",
                })
            return json.dumps({
                "status": "success",
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "completed": task.completed,
                    "updated_at": task.updated_at.isoformat(),
                },
            })
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


@mcp.tool()
def update_task(
    user_id: str,
    task_id: int,
    title: str | None = None,
    description: str | None = None,
) -> str:
    """Update a task's title or description.

    Args:
        user_id: The ID of the user who owns the task.
        task_id: The ID of the task to update.
        title: New title for the task (optional, 1-255 chars).
        description: New description for the task (optional, 0-1000 chars).
    """
    if not user_id or not user_id.strip():
        return json.dumps({"status": "error", "message": "user_id is required"})
    if task_id < 1:
        return json.dumps({"status": "error", "message": "task_id must be a positive integer"})
    if title is None and description is None:
        return json.dumps({
            "status": "error",
            "message": "At least one field (title or description) must be provided",
        })
    if title is not None and (not title.strip() or len(title) > 255):
        return json.dumps({"status": "error", "message": "Title must be 1-255 characters"})
    if description is not None and len(description) > 1000:
        return json.dumps({"status": "error", "message": "Description must be 1000 characters or fewer"})

    try:
        with Session(engine) as session:
            task_update = TaskUpdate(
                title=title.strip() if title else None,
                description=description.strip() if description is not None else None,
            )
            task = TaskService.update_task(session, task_id, user_id, task_update)
            if not task:
                return json.dumps({
                    "status": "error",
                    "message": f"Task with ID {task_id} not found for this user",
                })
            return json.dumps({
                "status": "success",
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "updated_at": task.updated_at.isoformat(),
                },
            })
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


@mcp.tool()
def delete_task(user_id: str, task_id: int) -> str:
    """Delete a task permanently.

    Args:
        user_id: The ID of the user who owns the task.
        task_id: The ID of the task to delete.
    """
    if not user_id or not user_id.strip():
        return json.dumps({"status": "error", "message": "user_id is required"})
    if task_id < 1:
        return json.dumps({"status": "error", "message": "task_id must be a positive integer"})

    try:
        with Session(engine) as session:
            success = TaskService.delete_task(session, task_id, user_id)
            if not success:
                return json.dumps({
                    "status": "error",
                    "message": f"Task with ID {task_id} not found for this user",
                })
            return json.dumps({
                "status": "success",
                "message": f"Task {task_id} deleted successfully",
            })
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


if __name__ == "__main__":
    mcp.run(transport="stdio")
