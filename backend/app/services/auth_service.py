from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token, 
    )
from app.models.user import User
from app.schemas.auth import UserRegister


def get_user_by_email(db: Session, email: str) -> User | None:
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )
    

def create_user(
    db: Session,
    user_data: UserRegister,
) -> User:
    hashed_password = hash_password(user_data.password)
    
    new_user = User(
        full_name = user_data.full_name,
        email=user_data.email,
        hashed_password = hashed_password,
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


def authenticate_user(
    db: Session,
    email: str,
    password: str
):
    user = get_user_by_email(db, email)
    
    if not user:
        return None
    
    if not verify_password(
        password,
        user.hashed_password,
    ):
        return None
    
    return user


