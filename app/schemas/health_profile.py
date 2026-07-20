from pydantic import BaseModel, Field

class HealthProfileBase(BaseModel):
    age: int | None = Field(
        default=None,
        ge=0,
        le=120,
    )
    
    gender: str | None = Field(
        default=None,
        max_length=20
    )
    
    height_cm: float | None = Field(
        default=None,
        gt=0,
        le=300,
    )
    
    weight_kg: float | None = Field(
        default=None,
        gt=0,
        le=500,
    )
    
    blood_group: str | None = Field(
        default=None,
        max_length=10,
    )
    
    allergies: str | None = None
    
    medical_conditions: str | None = None
    
    current_medications: str | None = None
    
    smoker: bool | None = None
    
    alcohol_use: str | None = Field(
        default=None,
        max_length=50,
    )
    
    exercise_frequency: str | None = Field(
        default=None,
        max_length=50,
    )
    
    sleep_hours: float | None = Field(
        default=None,
        ge=0,
        le=24,
    )
    
    
class HealthProfileCreate(HealthProfileBase):
    pass


class HealthProfileUpdate(HealthProfileBase):
    pass


class HealthProfileResponse(HealthProfileBase):
    id: int
    user_id: int
    bmi: float | None = None
    
    model_config = {
        "from_attributes": True
    }


