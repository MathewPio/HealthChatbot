from pydantic import BaseModel

class AdminStatsResponse(BaseModel):
    total_users: int
    total_admins: int
    total_regular_users: int
    total_chat_sessions: int
    total_messages: int
    

class UserRoleUpdate(BaseModel):
    role: str
    
