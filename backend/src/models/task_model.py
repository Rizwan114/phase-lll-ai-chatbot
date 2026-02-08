from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from .user_model import User

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: str = Field(min_length=1, max_length=255)  # Foreign key reference to User

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None

class TaskPublic(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime