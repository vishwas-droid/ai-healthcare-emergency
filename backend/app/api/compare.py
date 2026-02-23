from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Ambulance, Doctor
from app.db.schemas import CompareRequest, CompareResponse
from app.db.session import get_db
from app.services.recommendation_service import ambulance_recommendation, doctor_recommendation
from app.services.scoring_service import (
    score_ambulances,
    score_ambulances_contextual,
    score_doctors,
    score_doctors_contextual,
)

router = APIRouter(prefix="", tags=["Compare"])


@router.post("/compare", response_model=CompareResponse)
def compare_entities(payload: CompareRequest, db: Session = Depends(get_db)):
    if payload.entity_type.lower() == "doctor":
        items = db.scalars(select(Doctor).where(Doctor.id.in_(payload.ids))).all()
        if not items:
            raise HTTPException(status_code=404, detail="Doctors not found")
        if payload.city and payload.budget is not None:
            ranked = score_doctors_contextual(items, payload.city, payload.category or "", payload.budget)
        else:
            ranked = score_doctors(items)
        winner = ranked[0]
        return CompareResponse(
            winner_id=winner.id,
            winner_name=winner.name,
            score=winner.ai_score,
            reason=doctor_recommendation(winner, payload.category),
        )

    if payload.entity_type.lower() == "ambulance":
        items = db.scalars(select(Ambulance).where(Ambulance.id.in_(payload.ids))).all()
        if not items:
            raise HTTPException(status_code=404, detail="Ambulances not found")
        if payload.city and payload.budget is not None:
            ranked = score_ambulances_contextual(items, payload.city, payload.budget)
        else:
            ranked = score_ambulances(items)
        winner = ranked[0]
        return CompareResponse(
            winner_id=winner.id,
            winner_name=winner.provider_name,
            score=winner.ai_score,
            reason=ambulance_recommendation(winner, payload.budget),
        )

    raise HTTPException(status_code=400, detail="entity_type must be doctor or ambulance")
