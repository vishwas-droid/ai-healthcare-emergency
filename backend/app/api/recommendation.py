from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Ambulance, Doctor, SearchEvent
from app.db.schemas import EmergencyRecommendRequest, EmergencyRecommendResponse
from app.db.session import get_db
from app.services.recommendation_service import ambulance_recommendation, doctor_recommendation, final_recommendation
from app.services.scoring_service import score_ambulances_contextual, score_doctors_contextual

router = APIRouter(prefix="", tags=["Recommendation"])


@router.post("/recommend", response_model=EmergencyRecommendResponse)
def recommend(payload: EmergencyRecommendRequest, db: Session = Depends(get_db)):
    db.add(SearchEvent(city=payload.location, problem=payload.problem, budget=payload.budget))

    min_rating = payload.min_rating if payload.min_rating is not None else 0.0

    doctor_stmt = select(Doctor).where(Doctor.rating >= min_rating)
    ambulance_stmt = select(Ambulance)

    doctors = score_doctors_contextual(db.scalars(doctor_stmt).all(), payload.location, payload.problem, payload.budget)
    ambulances = score_ambulances_contextual(db.scalars(ambulance_stmt).all(), payload.location, payload.budget)

    if payload.service_preference == "doctor":
        ambulances = []
    elif payload.service_preference == "ambulance":
        doctors = []

    doctors = doctors[:5]
    ambulances = ambulances[:5]

    for doctor in doctors:
        db.add(doctor)
    for ambulance in ambulances:
        db.add(ambulance)
    db.commit()

    top_doctor = doctors[0] if doctors else None
    top_ambulance = ambulances[0] if ambulances else None

    return EmergencyRecommendResponse(
        doctors=doctors,
        ambulances=ambulances,
        top_doctor_summary=doctor_recommendation(top_doctor, payload.problem) if top_doctor else "No doctor match",
        top_ambulance_summary=ambulance_recommendation(top_ambulance, payload.budget) if top_ambulance else "No ambulance match",
        final_recommendation=final_recommendation(top_doctor, top_ambulance, payload.problem, payload.budget),
    )
