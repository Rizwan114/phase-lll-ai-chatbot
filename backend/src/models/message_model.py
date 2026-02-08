from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .conversation_model import Conversation


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: str = Field(foreign_key="conversation.id", index=True)
    user_id: str = Field(min_length=1, max_length=255)
    role: str = Field(min_length=1, max_length=20)  # "user" or "assistant"
    content: str = Field(min_length=1)
    created_at: datetime = Field(default_factory=datetime.now)

    conversation: Optional["Conversation"] = Relationship(back_populates="messages")
