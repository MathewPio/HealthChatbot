from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt 
import bcrypt

from app.core.config import settings

# Configures the password-hashing algorithm

# password_context = CryptContext(
#     schemes=["bcrypt"],
#     deprecated="auto",
# )


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    
    if len(password_bytes) > 72:
        raise ValueError("Password must not exceed 72 bytes.")
    
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    
    
    # Return hashed password
    return hashed_password.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except (ValueError, TypeError):
        return False
    

def create_access_token(
    subject: str | int,
    expires_delta: timedelta | None = None,
    additional_claims: dict[str, Any] | None = None,
) -> str:
    
    # Create a signed jwt token
    
    if expires_delta is None:
        expires_delta = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        
    expiration_time = datetime.now(timezone.utc) + expires_delta
    
    payload: dict[str, Any] = {
        "sub": str(subject),
        "exp": expiration_time,
        "iat": datetime.now(timezone.utc),
    }
    
    if additional_claims:
        payload.update(additional_claims)
        
    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    

def decode_access_token(token: str) -> dict[str, Any] | None:
    try: 
        payload =jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    
    except JWTError:
        return None
    
    

