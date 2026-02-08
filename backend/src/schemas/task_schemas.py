from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..models.task_model import TaskPublic

class TaskCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskToggleRequest(BaseModel):
    completed: bool

class TaskResponse(TaskPublic):
    pass

class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total: int

class ErrorResponse(BaseModel):
    detail: str