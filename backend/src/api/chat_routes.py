from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ..database.database import engine
from ..schemas.chat_schemas import ChatRequest, ChatResponse, ToolCallInfo, ChatHistoryResponse, MessageInfo
from ..services.conversation_service import ConversationService
from ..services.message_service import MessageService
from ..agent.runner import run as run_agent
from ..auth.middleware import get_current_user_from_token as get_current_user
from ..utils.logger import log_info, log_error

router = APIRouter()


def get_session():
    with Session(engine) as session:
        yield session


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    # Verify user_id matches authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    try:
        # Step 1: Get or create conversation
        if request.conversation_id:
            conversation = ConversationService.get_by_id(
                session, request.conversation_id, user_id
            )
            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found",
                )
        else:
            conversation = ConversationService.get_or_create(session, user_id)

        # Step 2: Load message history
        db_messages = MessageService.list_by_conversation(session, conversation.id)
        messages = [
            {"role": msg.role, "content": msg.content} for msg in db_messages
        ]

        # Step 3: Persist user message
        MessageService.create(
            session, conversation.id, user_id, "user", request.message
        )

        # Step 4: Append current message to history for agent
        messages.append({"role": "user", "content": request.message})

        # Step 5: Run agent
        result = await run_agent(messages, user_id)

        # Step 6: Persist assistant response
        MessageService.create(
            session, conversation.id, user_id, "assistant", result.response
        )

        # Step 7: Update conversation timestamp
        ConversationService.update_timestamp(session, conversation.id)

        log_info("Chat message processed", extra={
            "user_id": user_id,
            "conversation_id": conversation.id,
        })

        # Step 8: Return response
        tool_calls = None
        if result.tool_calls:
            tool_calls = [
                ToolCallInfo(tool=tc.get("tool", ""), input=tc.get("input"))
                for tc in result.tool_calls
            ]

        return ChatResponse(
            conversation_id=conversation.id,
            response=result.response,
            tool_calls=tool_calls,
        )

    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Chat error: {str(e)}", extra={"user_id": user_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="I'm having trouble right now. Please try again.",
        )


@router.get("/{user_id}/chat/history", response_model=ChatHistoryResponse)
async def chat_history(
    user_id: str,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    try:
        conversation = ConversationService.get_by_user_id(session, user_id)
        if not conversation:
            return ChatHistoryResponse(conversation_id=None, messages=[])

        db_messages = MessageService.list_by_conversation(session, conversation.id)
        messages = [
            MessageInfo(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at,
            )
            for msg in db_messages
        ]

        return ChatHistoryResponse(
            conversation_id=conversation.id,
            messages=messages,
        )

    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Chat history error: {str(e)}", extra={"user_id": user_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
