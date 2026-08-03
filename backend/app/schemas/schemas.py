from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# ---------- Auth ----------
class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------- Symptom lookup ----------
class SymptomListOut(BaseModel):
    symptoms: List[str]


# ---------- Diagnosis ----------
class DiagnosisRequest(BaseModel):
    symptoms: List[str] = Field(..., min_length=1, description="Symptom names or free-text phrases")
    free_text: Optional[str] = Field(None, description="Optional free-text description, parsed by the LLM")
    age: Optional[int] = Field(None, ge=0, le=120)
    sex: Optional[str] = Field(None, pattern="^(male|female|other)$")
    duration_days: Optional[int] = Field(None, ge=0)
    severity: Optional[str] = Field(None, pattern="^(mild|moderate|severe)$")
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class DiseasePrediction(BaseModel):
    disease: str
    confidence: float
    specialist: str
    medicine_categories: List[str]
    summary: str
    emergency: bool


class DiagnosisResponse(BaseModel):
    id: int
    predictions: List[DiseasePrediction]
    llm_explanation: str
    red_flags: List[str]
    is_emergency: bool
    unmatched_symptoms: List[str]
    disclaimer: str = (
        "This tool provides general health information and is not a medical diagnosis. "
        "Always consult a licensed healthcare professional for any health concerns."
    )

    model_config = ConfigDict(from_attributes=True)


class SessionHistoryOut(BaseModel):
    id: int
    reported_symptoms: List[str]
    predictions: List[dict]
    is_emergency: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------- Specialists ----------
class SpecialistOut(BaseModel):
    name: str
    address: str
    rating: Optional[float] = None
    specialty: str
    distance_km: Optional[float] = None
    place_id: Optional[str] = None


class SpecialistSearchResponse(BaseModel):
    specialty_searched: str
    results: List[SpecialistOut]
    note: Optional[str] = None
