from fastapi import APIRouter, Depends
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