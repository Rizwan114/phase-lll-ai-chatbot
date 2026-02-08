from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class UserBase(SQLModel):
    user_id: str = Field(max_length=255, unique=True)


class User(UserBase, table=True):
    """
    User model representing a user in the system with unique identifier that owns tasks
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class UserCreate(UserBase):
    pass


class UserUpdate(SQLModel):
    user_id: Optional[str] = Field(default=None, max_length=255)


class UserPublic(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime