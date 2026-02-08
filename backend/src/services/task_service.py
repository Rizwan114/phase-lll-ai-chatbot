from sqlmodel import Session, select, and_
from typing import List, Optional
from datetime import datetime
from ..models.task_model import Task, TaskCreate, TaskUpdate
from ..utils.logger import log_info, log_error

class TaskService:
    @staticmethod
    def create_task(session: Session, task_create: TaskCreate) -> Task:
        """
        Create a new task in the database
        """
        try:
            # Create the task object
            db_task = Task.from_orm(task_create) if hasattr(Task, 'from_orm') else Task.model_validate(task_create)

            # Set the created_at and updated_at timestamps
            now = datetime.now()
            db_task.created_at = now
            db_task.updated_at = now

            # Add to session and commit
            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            log_info(f"Task created successfully with ID: {db_task.id}", extra={"user_id": db_task.user_id, "task_id": db_task.id})
            return db_task
        except Exception as e:
            log_error(f"Error creating task: {str(e)}", extra={"user_id": task_create.user_id})
            session.rollback()
            raise e

    @staticmethod
    def get_task_by_id(session: Session, task_id: int, user_id: str) -> Optional[Task]:
        """
        Get a specific task by ID for a specific user
        """
        try:
            statement = select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
            task = session.exec(statement).first()
            if task:
                log_info(f"Task retrieved successfully", extra={"user_id": user_id, "task_id": task_id})
            else:
                log_info(f"Task not found", extra={"user_id": user_id, "task_id": task_id})
            return task
        except Exception as e:
            log_error(f"Error retrieving task: {str(e)}", extra={"user_id": user_id, "task_id": task_id})
            raise e

    @staticmethod
    def get_tasks_by_user(session: Session, user_id: str, offset: int = 0, limit: int = 100) -> List[Task]:
        """
        Get all tasks for a specific user
        """
        try:
            statement = select(Task).where(Task.user_id == user_id).offset(offset).limit(limit)
            tasks = session.exec(statement).all()
            log_info(f"Retrieved {len(tasks)} tasks for user", extra={"user_id": user_id, "count": len(tasks)})
            return tasks
        except Exception as e:
            log_error(f"Error retrieving tasks for user: {str(e)}", extra={"user_id": user_id})
            raise e

    @staticmethod
    def update_task(session: Session, task_id: int, user_id: str, task_update: TaskUpdate) -> Optional[Task]:
        """
        Update a specific task for a specific user
        """
        try:
            # Get the existing task
            statement = select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
            db_task = session.exec(statement).first()

            if not db_task:
                log_info(f"Task not found for update", extra={"user_id": user_id, "task_id": task_id})
                return None

            # Update the task with provided values
            update_data = task_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_task, field, value)

            # Update the updated_at timestamp
            db_task.updated_at = datetime.now()

            # Commit the changes
            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            log_info(f"Task updated successfully", extra={"user_id": user_id, "task_id": task_id})
            return db_task
        except Exception as e:
            log_error(f"Error updating task: {str(e)}", extra={"user_id": user_id, "task_id": task_id})
            session.rollback()
            raise e

    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: str) -> bool:
        """
        Delete a specific task for a specific user
        """
        try:
            # Get the existing task
            statement = select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
            db_task = session.exec(statement).first()

            if not db_task:
                log_info(f"Task not found for deletion", extra={"user_id": user_id, "task_id": task_id})
                return False

            # Delete the task
            session.delete(db_task)
            session.commit()

            log_info(f"Task deleted successfully", extra={"user_id": user_id, "task_id": task_id})
            return True
        except Exception as e:
            log_error(f"Error deleting task: {str(e)}", extra={"user_id": user_id, "task_id": task_id})
            session.rollback()
            raise e

    @staticmethod
    def toggle_task_completion(session: Session, task_id: int, user_id: str) -> Optional[Task]:
        """
        Toggle the completion status of a task
        """
        try:
            # Get the existing task
            statement = select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
            db_task = session.exec(statement).first()

            if not db_task:
                log_info(f"Task not found for toggle", extra={"user_id": user_id, "task_id": task_id})
                return None

            # Toggle the completion status
            db_task.completed = not db_task.completed
            db_task.updated_at = datetime.now()

            # Commit the changes
            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            log_info(f"Task completion toggled", extra={"user_id": user_id, "task_id": task_id, "completed": db_task.completed})
            return db_task
        except Exception as e:
            log_error(f"Error toggling task completion: {str(e)}", extra={"user_id": user_id, "task_id": task_id})
            session.rollback()
            raise e