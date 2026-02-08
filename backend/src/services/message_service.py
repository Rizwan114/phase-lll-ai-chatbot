from sqlmodel import Session, select
from typing import List
from ..models.message_model import Message


class MessageService:
    @staticmethod
    def create(session: Session, conversation_id: str, user_id: str, role: str, content: str) -> Message:
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    @staticmethod
    def list_by_conversation(session: Session, conversation_id: str) -> List[Message]:
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        )
        return list(session.exec(statement).all())
