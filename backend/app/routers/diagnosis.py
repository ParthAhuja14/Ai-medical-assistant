from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.config import settings
from app.models.models import User, DiagnosisSession
from app.schemas.schemas import (
    DiagnosisRequest, DiagnosisResponse, SessionHistoryOut,
    SymptomListOut, SpecialistSearchResponse,
)
from app.ml.predict import predict_diseases, get_all_symptoms, get_unmatched_symptoms
from app.services.gemini_service import parse_free_text_symptoms, generate_explanation
from app.services.places_service import find_nearby_specialists

router = APIRouter(prefix="/api/diagnosis", tags=["diagnosis"])


@router.get("/symptoms", response_model=SymptomListOut)
def list_symptoms():
    """Returns the full vocabulary of symptoms the model recognizes, for the frontend picker."""
    return SymptomListOut(symptoms=get_all_symptoms())


@router.post("/", response_model=DiagnosisResponse, status_code=201)
def run_diagnosis(
    payload: DiagnosisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    known_symptoms = get_all_symptoms()

    all_symptoms = list(payload.symptoms)
    if payload.free_text:
        extracted = parse_free_text_symptoms(payload.free_text, known_symptoms)
        all_symptoms.extend(extracted)

    if not all_symptoms:
        raise HTTPException(status_code=400, detail="Please provide at least one symptom.")

    predictions = predict_diseases(all_symptoms, top_k=settings.TOP_K_PREDICTIONS)
    unmatched = get_unmatched_symptoms(all_symptoms)

    if not predictions:
        raise HTTPException(
            status_code=422,
            detail="None of the reported symptoms matched our recognized symptom list. "
                   "Try selecting symptoms from the suggested list.",
        )

    patient_context = {
        "age": payload.age,
        "sex": payload.sex,
        "duration_days": payload.duration_days,
        "severity": payload.severity,
        "symptoms": all_symptoms,
    }
    llm_result = generate_explanation(predictions, patient_context)

    is_emergency = any(p["emergency"] for p in predictions) or bool(llm_result.get("red_flags"))

    session = DiagnosisSession(
        user_id=current_user.id,
        reported_symptoms=all_symptoms,
        unmatched_symptoms=unmatched,
        age=payload.age,
        sex=payload.sex,
        duration_days=payload.duration_days,
        severity=payload.severity,
        free_text_notes=payload.free_text,
        predictions=predictions,
        llm_explanation=llm_result.get("explanation", ""),
        red_flags=llm_result.get("red_flags", []),
        is_emergency=is_emergency,
        latitude=payload.latitude,
        longitude=payload.longitude,
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return DiagnosisResponse(
        id=session.id,
        predictions=predictions,
        llm_explanation=session.llm_explanation,
        red_flags=session.red_flags,
        is_emergency=session.is_emergency,
        unmatched_symptoms=unmatched,
    )


@router.get("/history", response_model=list[SessionHistoryOut])
def get_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(DiagnosisSession).filter(
        DiagnosisSession.user_id == current_user.id
    ).order_by(DiagnosisSession.created_at.desc()).all()


@router.get("/{session_id}/specialists", response_model=SpecialistSearchResponse)
def get_nearby_specialists(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = db.query(DiagnosisSession).filter(
        DiagnosisSession.id == session_id, DiagnosisSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Diagnosis session not found.")
    if session.latitude is None or session.longitude is None:
        raise HTTPException(status_code=400, detail="No location was provided for this session.")
    if not session.predictions:
        raise HTTPException(status_code=400, detail="This session has no predictions to base a search on.")

    top_specialty = session.predictions[0]["specialist"]
    result = find_nearby_specialists(top_specialty, session.latitude, session.longitude)
    return result
