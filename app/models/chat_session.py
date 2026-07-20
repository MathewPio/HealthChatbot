from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    
    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )
    
    title = Column(
        String(150),
        nullable=False,
        default="New Conversation",
        server_default="New Conversation",
    )
    
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    
    user = relationship(
        "User",
        back_populates="chat_sessions",
    )
    
    messages = relationship(
        "ChatMessage",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="ChatMessage.created_at",
    )