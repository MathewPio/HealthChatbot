from datetime import datetime

from pydantic import BaseModel, Field

class ChatSessionCreate(BaseModel):
    title:str = Field(
        default="New Conversation",
        min_length=1,
        max_length=150,
    )
    
class ChatMessageCreate(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=5000,
    )
    
class ChatMessageResponse(BaseModel):
    id: int
    session_id: int
    role: str
    content: str
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }
    
    
class ChatSessionResponse(BaseModel):
    id: int
    user_id: int
    title: str
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }
    
    
class ChatSessionDetailResponse(ChatSessionResponse):
    messages: list[ChatMessageResponse] = []