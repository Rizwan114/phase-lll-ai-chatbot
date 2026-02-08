from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
import uuid

if TYPE_CHECKING:
    from .message_model import Message


class Conversation(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(min_length=1, max_length=255, index=True, unique=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    messages: List["Message"] = Relationship(back_populates="conversation")
