from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_admin
from app.database.connection import get_db
from app.models.user import User
from app.schemas.auth import UserResponse

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