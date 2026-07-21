import app.services.health_profile_service
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import httpx
from app.api.dependencies import get_current_user
from app.database.connection import get_db
from app.models.user import User
from app.schemas.chat import (
    ChatMessageCreate,
    ChatMessageResponse,
    ChatSessionCreate,
    ChatSessionDetailResponse,
    ChatSessionResponse,
    ChatExchangeResponse, 
)
from app.services.ollama_service import generate_ai_response

from app.services.chat_service import (
    add_chat_message,
    create_chat_session,
    get_chat_session_by_id,
    get_user_chat_sessions,
    get_chat_messages,
)
from app.services.health_profile_service import (
    get_health_profile_by_user_id,
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
    response_model=ChatExchangeResponse,
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
    
    chat_history = get_chat_messages(
        db,
        session.id
    )
    
    profile = get_health_profile_by_user_id(
        db,
        current_user.id
    )
    
    profile_context = "No health profile is available for this user."
    
    if profile is not None:
        profile_context = (
            f"Age: {profile.age}\n"
            f"Gender: {profile.gender}\n"
            f"Height: {profile.height_cm} cm\n"
            f"Weight: {profile.weight_kg} kg\n"
            f"Medical conditions: {profile.medical_conditions}\n"
            f"Current medications: {profile.current_medications}\n"
            f"Exercise frequency: {profile.exercise_frequency}\n"
            f"Sleep hours: {profile.sleep_hours}\n"
            f"Smoker: {profile.smoker}\n"
            f"Alcohol use: {profile.alcohol_use}"
            f"Fitness goal: {profile.fitness_goal}\n"
            f"Activity level: {profile.activity_level}\n"
            f"Training experience: {profile.training_experience}"
        )
    
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful fitness and wellness assistant. "
                "Your primary role is to provide practical guidance about exercise, "
                "workout planning, fitness goals, recovery, sleep, and healthy habits. "
                "Use the user's profile and previous conversation to personalise your responses. "
                "Do not invent information that is not present in the user's profile or conversation. "
                "Do not diagnose medical conditions or present yourself as a doctor. "
                "If the user describes a potentially serious medical issue, encourage them to seek "
                "appropriate professional medical help. "
                "Keep your advice clear, supportive, and appropriate for the user's training experience.\n\n"
                "Here is the user's health and fitness profile:\n"
                f"{profile_context}"
            ),
        },
    ]
    
    for message in chat_history:
        messages.append(
            {
                "role": message.role,
                "content": message.content,
            }
        )
    
    try:
        ai_response = generate_ai_response(messages)
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="The AI assistant took too long to respond.",
        )
    
    except httpx.HTTPError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The AI assistant is currently unavailable.",
        )
    
    assistant_message = add_chat_message(
        db, 
        session.id,
        "assistant",
        ai_response,
    )
    
    return {
        "user_message": user_message,
        "assistant_message": assistant_message,
    }
        
     
     
  
        
        
        
        
        
        
        
        