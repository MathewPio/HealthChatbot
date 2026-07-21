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
            fitness_goal=profile.fitness_goal,
            activity_level=profile.activity_level,
            training_experience=profile.training_experience,
        )
    

@router.post(
    "",
    response_model=HealthProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_my_health_profile(
    profile_data: HealthProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing_profile = get_health_profile_by_user_id(
        db,
        current_user.id,
    )
    
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Health Profile already exists",
        )
        
    profile = create_health_profile(
        db,
        current_user.id,
        profile_data
    )
    
    return build_profile_response(profile)


@router.get(
    "",
    response_model = HealthProfileResponse
)
def get_my_health_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = get_health_profile_by_user_id(
        db,
        current_user.id,
    )
    
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health profile is not found.",
        )
        
    return build_profile_response(profile)


@router.patch(
    "",
    response_model=HealthProfileResponse,
)
def update_my_health_profile(
    profile_data: HealthProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = get_health_profile_by_user_id(
        db,
        current_user.id,
    )
    
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health profile is not found"
        )
    
    updated_profile = update_health_profile(
        db,
        profile,
        profile_data,
    )
    
    return build_profile_response(updated_profile)


