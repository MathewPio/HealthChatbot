from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
) 

from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,    
)

from app.database.base import Base


class HealthProfile(Base):
    __tablename__="health_profiles"
    
    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    
    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
    )
    
    age = Column(
        Integer,
        nullable=True,
    )
    
    gender = Column(
        String(20),
        nullable=True,
    )
    
    height_cm = Column(
        Float,
        nullable=True,
    )
    
    weight_kg =Column(
        Float,
        nullable=True,
    )
    
    blood_group = Column(
        String(10),
        nullable=True,
    )
    
    allergies = Column(
        Text,
        nullable=True,
    )
    
    medical_conditions = Column(
        Text,
        nullable=True,
    )
    
    current_medications = Column(
        Text,
        nullable=True,
    )
    
    smoker = Column(
        Boolean,
        nullable=True,
    )
    
    alcohol_use = Column(
        String(50),
        nullable=True,
    )
    
    exercise_frequency = Column(
        String(50),
        nullable=True,
    )
    
    sleep_hours = Column(
        Float,
        nullable=True,
    )
    
    user = relationship(
        "User",
        back_populates="health_profile",
    )


    fitness_goal: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    
    activity_level: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    
    training_experience: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )




