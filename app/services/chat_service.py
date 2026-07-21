from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage
from app.models.chat_session import ChatSession

def create_chat_session(
    db: Session,
    user_id: int,
    title: str,
) -> ChatSession:
    
    session = ChatSession(
        user_id = user_id,
        title=title,
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return session


def get_user_chat_sessions(
    db: Session,
    user_id: int,
) -> list[ChatSession]:
    
    return (
        db.query(ChatSession)
        .filter(ChatSession.user_id == user_id)
        .order_by(ChatSession.created_at.desc())
        .all()
    )
    
    
def get_chat_session_by_id(
    db: Session,
    session_id: int,
) -> ChatSession | None:
    
    return db.get(
        ChatSession,
        session_id,
    )
    
    
def add_chat_message(
    db: Session,
    session_id: int,
    role: str,
    content: str,
) -> ChatMessage:
    
    message = ChatMessage(
        session_id = session_id,
        role = role,
        content = content,
    )
    
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return message


def get_chat_messages(
    db: Session,
    session_id: int,
) -> list[ChatMessage]:
    
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )
    
    