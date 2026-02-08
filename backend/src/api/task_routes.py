from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlmodel import Session
from typing import List
from ..database.database import engine
from ..models.task_model import TaskCreate, TaskUpdate, TaskPublic
from ..schemas.task_schemas import (
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskResponse,
    TaskListResponse,
    ErrorResponse
)
from ..services.task_service import TaskService
from ..utils.logger import log_info, log_error
from ..auth.middleware import get_current_user_from_token as get_current_user

router = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: str,
    task_request: TaskCreateRequest,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """
    Create a new task for the specified user.
    The user_id in the path must match the authenticated user.
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    try:
        # Prepare the task creation object
        task_create = TaskCreate(
            title=task_request.title,
            description=task_request.description,
            completed=task_request.completed,
            user_id=user_id
        )

        # Create the task using the service
        db_task = TaskService.create_task(session, task_create)

        log_info(f"Task created successfully", extra={
            "user_id": user_id,
            "task_id": db_task.id,
            "title": db_task.title
        })

        return TaskResponse.from_orm(db_task) if hasattr(TaskResponse, 'from_orm') else TaskResponse.model_validate(db_task)
    except Exception as e:
        log_error(f"Failed to create task: {str(e)}", extra={"user_id": user_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create task: {str(e)}"
        )


@router.get("/{user_id}/tasks", response_model=TaskListResponse)
def get_tasks(
    user_id: str,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
    offset: int = 0,
    limit: int = 100
):
    """
    Get all tasks for the specified user.
    The user_id in the path must match the authenticated user.
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view tasks for this user"
        )

    try:
        # Get tasks for the user
        db_tasks = TaskService.get_tasks_by_user(session, user_id, offset, limit)

        # Convert to response format
        tasks_response = [TaskResponse.from_orm(task) if hasattr(TaskResponse, 'from_orm') else TaskResponse.model_validate(task) for task in db_tasks]

        log_info(f"Retrieved {len(tasks_response)} tasks", extra={
            "user_id": user_id,
            "count": len(tasks_response)
        })

        return TaskListResponse(tasks=tasks_response, total=len(tasks_response))
    except Exception as e:
        log_error(f"Failed to retrieve tasks: {str(e)}", extra={"user_id": user_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve tasks: {str(e)}"
        )


@router.get("/{user_id}/tasks/{id}", response_model=TaskResponse)
def get_task(
    user_id: str,
    id: int = Path(..., ge=1),
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """
    Get a specific task by ID for the specified user.
    The user_id in the path must match the authenticated user.
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this task"
        )

    try:
        # Get the specific task
        db_task = TaskService.get_task_by_id(session, id, user_id)

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {id} not found"
            )

        log_info(f"Task retrieved successfully", extra={
            "user_id": user_id,
            "task_id": id
        })

        return TaskResponse.from_orm(db_task) if hasattr(TaskResponse, 'from_orm') else TaskResponse.model_validate(db_task)
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        log_error(f"Failed to retrieve task: {str(e)}", extra={"user_id": user_id, "task_id": id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve task: {str(e)}"
        )


@router.put("/{user_id}/tasks/{id}", response_model=TaskResponse)
def update_task(
    user_id: str,
    task_update: TaskUpdateRequest,
    id: int = Path(..., ge=1),
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """
    Update a specific task by ID for the specified user.
    The user_id in the path must match the authenticated user.
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    try:
        # Prepare the task update object, only passing fields that were actually sent
        update_data = task_update.model_dump(exclude_unset=True)
        task_update_obj = TaskUpdate(**update_data)

        # Update the task using the service
        db_task = TaskService.update_task(session, id, user_id, task_update_obj)

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {id} not found"
            )

        log_info(f"Task updated successfully", extra={
            "user_id": user_id,
            "task_id": id
        })

        return TaskResponse.from_orm(db_task) if hasattr(TaskResponse, 'from_orm') else TaskResponse.model_validate(db_task)
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        log_error(f"Failed to update task: {str(e)}", extra={"user_id": user_id, "task_id": id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update task: {str(e)}"
        )


@router.delete("/{user_id}/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: str,
    id: int = Path(..., ge=1),
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """
    Delete a specific task by ID for the specified user.
    The user_id in the path must match the authenticated user.
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    try:
        # Delete the task using the service
        success = TaskService.delete_task(session, id, user_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {id} not found"
            )

        log_info(f"Task deleted successfully", extra={
            "user_id": user_id,
            "task_id": id
        })

        return
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        log_error(f"Failed to delete task: {str(e)}", extra={"user_id": user_id, "task_id": id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete task: {str(e)}"
        )


@router.patch("/{user_id}/tasks/{id}/complete", response_model=TaskResponse)
def toggle_task_completion(
    user_id: str,
    id: int = Path(..., ge=1),
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """
    Toggle the completion status of a specific task by ID for the specified user.
    The user_id in the path must match the authenticated user.
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to toggle completion for this task"
        )

    try:
        # Toggle the task completion using the service
        db_task = TaskService.toggle_task_completion(session, id, user_id)

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {id} not found"
            )

        log_info(f"Task completion toggled successfully", extra={
            "user_id": user_id,
            "task_id": id,
            "completed": db_task.completed
        })

        return TaskResponse.from_orm(db_task) if hasattr(TaskResponse, 'from_orm') else TaskResponse.model_validate(db_task)
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        log_error(f"Failed to toggle task completion: {str(e)}", extra={"user_id": user_id, "task_id": id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to toggle task completion: {str(e)}"
        )