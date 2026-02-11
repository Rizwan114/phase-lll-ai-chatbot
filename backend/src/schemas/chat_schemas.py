from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime


class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str = Field(min_length=1, max_length=10000)


class ToolCallInfo(BaseModel):
    tool: str
    input: Any = None
    output: Any = None


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tool_calls: Optional[List[ToolCallInfo]] = None


class MessageInfo(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime


class ChatHistoryResponse(BaseModel):
    conversation_id: Optional[str] = None
    messages: List[MessageInfo] = []
