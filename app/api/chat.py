from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.connection import get_db
from app.models.user import User
from app.schemas.chat import (
    ChatMessageCreate,
    ChatMessageResponse,
    ChatSessionCreate,
    ChatSessionDetailResponse,
    ChatSessionResponse,
)
from app.services.ollama_service import generate_ai_response

from app.services.chat_service import (
    add_chat_message,
    create_chat_session,
    get_chat_session_by_id,
    get_user_chat_sessions,
)

router = APIRouter(
    prefix="/chats",
    tags=["Chats"],
)


@router.post(
    "",
    response_model = ChatSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_session(
    session_data: ChatSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_chat_session(
        db,
        current_user.id,
        session_data.title,
    )
    
    
@router.get(
    "",
    response_model=list[ChatSessionResponse],
)
def list_my_chatsessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
): 
    return get_user_chat_sessions(
        db,
        current_user.id,
    )
    

@router.get(
    "/{session_id}",
    response_model=ChatSessionDetailResponse,
)
def get_my_chat_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = get_chat_session_by_id(
        db,
        session_id,
    )
    
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found",
        )
        
    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this chat session"
        )
        
    return session


@router.post(
    "/{session_id}/messages",
    response_model=ChatMessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def send_message(
    session_id: int,
    message_data: ChatMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    
    # Find the chat session
    session = get_chat_session_by_id(
        db,
        session_id,
    )
    
    # Check that the chat session exists
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found.",
        )
    
    # Check that the logged-in user owns this chat
    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this chat session."
        )
    
    
    # Save the user's message
    # return add_chat_message(
    #     db,
    #     session.id,
    #     "user",
    #     message_data.content
    # )
    
    user_message = add_chat_message(
        db,
        session.id,
        "user",
        message_data.content,
    )
    
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful fitness and wellness assistant."
                "Focus on exercise, training, recovery, sleep, healthy habits, "
                "and general fitness guidance. Do not diagnose medical conditions."
            ),
        },
        {
            "role": "user",
            "content": message_data.content,
        },
    ]
    
    ai_response = generate_ai_response(messages)
    
    assistant_message = add_chat_message(
        db, 
        session.id,
        "assistant",
        ai_response,
    )
    
    return assistant_message
        
     
     
  
        
        
        
        
        
        
        
        