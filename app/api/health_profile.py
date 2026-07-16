from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.connection import get_db
from app.models.user import User
from app.schemas.health_profile import (
    HealthProfileCreate,
    HealthProfileResponse,
    HealthProfileUpdate
)
from app.services.health_profile_service import (
    create_health_profile,
    get_health_profile_by_user_id,
    update_health_profile,
)
from app.utils.health import calculate_bmi


router = APIRouter(
    prefix="/health-profile",
    tags=["Health Profile"]
)


def build_profile_response(profile):
    bmi = calculate_bmi(
        profile.weight_kg,
        profile.height_cm,
    )
    
    
    return HealthProfileResponse(
            id=profile.id,
            user_id=profile.user_id,
            age=profile.age,
            gender=profile.gender,
            height_cm=profile.height_cm,
            weight_kg=profile.weight_kg,
            blood_group=profile.blood_group,
            allergies=profile.allergies,
            medical_conditions=profile.medical_conditions,
            current_medications=profile.current_medications,
            smoker=profile.smoker,
            alcohol_use=profile.alcohol_use,
            exercise_frequency=profile.exercise_frequency,
            sleep_hours=profile.sleep_hours,
            bmi=bmi,
        )


