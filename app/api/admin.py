from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_admin
from app.database.connection import get_db
from app.models.user import User
from app.schemas.auth import UserResponse
from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage
from app.schemas.admin import AdminStatsResponse
from app.schemas.admin import UserRoleUpdate
from app.models.user import User

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

@router.get(
    "/users",
    response_model = list[UserResponse],
)
def get_all_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    return db.query(User).all()




@router.get(
    "/users/recent",
    response_model=list[UserResponse],
)
def get_recent_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
): 
    return (
        db.query(User)
        .order_by(User.created_at.desc())
        .limit(5)
        .all()
    )




@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    user = db.get(
        User,
        user_id,
    )
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
        
    return user


@router.get(
    "/stats",
    response_model=AdminStatsResponse,
)
def get_admin_stats(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    total_users = db.query(User).count()
    
    total_admins = (
        db.query(User)
        .filter(User.role == "admin")
        .count()
    )
    
    total_regular_users = (
        db.query(User)
        .filter(User.role == "user")
        .count()
    )
    
    total_chat_sessions = db.query(ChatSession).count()
    total_messages = db.query(ChatMessage).count()
    
    return AdminStatsResponse(
        total_users=total_users,
        total_admins=total_admins,
        total_regular_users=total_regular_users,
        total_chat_sessions=total_chat_sessions,
        total_messages=total_messages,
    )
    
    
@router.patch(
    "/users/{user_id}/role",
    response_model=UserResponse
)
def update_user_role(
    user_id: int,
    role_data: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    user = db.get(
        User,
        user_id,
    )
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
        
    if role_data.role not in ["user", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role must be either 'user' or 'admin'.",
        )
    
    user.role = role_data.role
    
    db.commit()
    db.refresh(user)
    
    return user


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    user = db.get(
        User,
        user_id,
    )
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot delete your own account"
        )
    
    db.delete(user)
    db.commit()
    
    return None
    
    
