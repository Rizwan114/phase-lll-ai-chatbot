from sqlmodel import Session, select
from typing import Optional
from datetime import datetime
from ..models.conversation_model import Conversation


class ConversationService:
    @staticmethod
    def get_or_create(session: Session, user_id: str) -> Conversation:
        statement = select(Conversation).where(Conversation.user_id == user_id)
        conversation = session.exec(statement).first()
        if conversation:
            return conversation

        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    def get_by_id(session: Session, conversation_id: str, user_id: str) -> Optional[Conversation]:
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
        return session.exec(statement).first()

    @staticmethod
    def update_timestamp(session: Session, conversation_id: str) -> None:
        statement = select(Conversation).where(Conversation.id == conversation_id)
        conversation = session.exec(statement).first()
        if conversation:
            conversation.updated_at = datetime.now()
            session.add(conversation)
            session.commit()
