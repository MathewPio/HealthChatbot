from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base

class User(Base):
    __tablename__="users"
    
    id = Column(Integer, primary_key=True, index=True)
    
    full_name = Column(String(100), nullable=False)
    
    email = Column(String(100), unique=True, nullable=False)
    
    hashed_password = Column(String(255), nullable=False)
    
    role = Column(
        String(20),
        nullable=False,
        default="user",
        server_default="user",
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    health_profile = relationship(
        "HealthProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    
    chat_sessions = relationship(
        "ChatSession",
        back_populates="user",
        cascade="all, delete-orphan",
    )