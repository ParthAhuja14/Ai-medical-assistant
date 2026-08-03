from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


def utcnow():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=utcnow)

    sessions = relationship("DiagnosisSession", back_populates="owner", cascade="all, delete-orphan")


class DiagnosisSession(Base):
    __tablename__ = "diagnosis_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    reported_symptoms = Column(JSON, nullable=False, default=list)
    unmatched_symptoms = Column(JSON, nullable=False, default=list)
    age = Column(Integer, nullable=True)
    sex = Column(String(20), nullable=True)
    duration_days = Column(Integer, nullable=True)
    severity = Column(String(20), nullable=True)  # mild/moderate/severe
    free_text_notes = Column(Text, nullable=True)

    predictions = Column(JSON, nullable=False, default=list)   # ranked ML output
    llm_explanation = Column(Text, nullable=True)
    red_flags = Column(JSON, nullable=False, default=list)
    is_emergency = Column(Boolean, default=False)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    created_at = Column(DateTime, default=utcnow)

    owner = relationship("User", back_populates="sessions")
