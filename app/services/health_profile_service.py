from sqlalchemy.orm import Session 

from app.models.health_profile import HealthProfile
from app.schemas.health_profile import (
    HealthProfileCreate,
    HealthProfileUpdate,
)

def get_health_profile_by_user_id(
    db: Session,
    user_id: int,
) -> HealthProfile | None:
    
    return (
        db.query(HealthProfile)
        .filter(HealthProfile.user_id == user_id)
        .first()
    )
    

def create_health_profile(
    db: Session,
    user_id: int,
    profile_data: HealthProfileCreate,
) -> HealthProfile:
    
    profile = HealthProfile(
        user_id=user_id,
        **profile_data.model_dump(),
    )
    
    db.add(profile)
    db.commit()
    db.refresh(profile)
    
    return profile


def update_health_profile(
    db: Session,
    profile: HealthProfile,
    profile_data: HealthProfileUpdate,
) -> HealthProfile:
    
    update_data = profile_data.model_dump(
        exclude_unset=True
    )
    
    for field, value in update_data.items():
        setattr(
            profile,
            field,
            value,
        )
        
    db.commit()
    db.refresh(profile)