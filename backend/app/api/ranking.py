from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Ambulance, Doctor, Emergency, Hospital, RankingScore
from app.db.schemas import (
    AmbulanceRankingResponse,
    DoctorRankingResponse,
    HospitalRankingResponse,
    RankingExplainResponse,
    RankingRequest,
)
from app.db.session import get_db
from app.services.feedback_loop import load_adjustments
from app.services.scoring_engine import (
    SEVERITY_WEIGHTS_AMBULANCE,
    SEVERITY_WEIGHTS_DOCTOR,
    SEVERITY_WEIGHTS_HOSPITAL,
    ambulance_score,
    doctor_score,
    explain_top_factor,
    hospital_score,
)

router = APIRouter(prefix="", tags=["Ranking"])


def _apply_weighted_score(breakdown: dict, weights: dict, adjustments: dict) -> float:
    total = 0.0
    for key, weight in weights.items():
        if key in breakdown:
            total += breakdown[key] * weight * adjustments.get(key, 1.0)
    return min(100.0, total)


def _emergency_context(db: Session, emergency_id: str, fallback_severity: str):
    emergency = db.get(Emergency, emergency_id)
    if not emergency:
        raise HTTPException(status_code=404, detail="Emergency not found")
    severity = emergency.severity or fallback_severity
    emergency_type = emergency.emergency_type or "Other"
    patient_loc = (emergency.latitude or 0.0, emergency.longitude or 0.0)
    return emergency, severity, emergency_type, patient_loc


@router.post("/rank/doctors", response_model=DoctorRankingResponse)
def rank_doctors(payload: RankingRequest, db: Session = Depends(get_db)):
    emergency, severity, emergency_type, patient_loc = _emergency_context(db, payload.emergency_id, payload.severity)
    if payload.latitude is not None and payload.longitude is not None:
        patient_loc = (payload.latitude, payload.longitude)
    adjustments = load_adjustments(db)
    weights = SEVERITY_WEIGHTS_DOCTOR.get(severity, SEVERITY_WEIGHTS_DOCTOR["LOW"])
    weights_dict = weights.__dict__

    stmt = select(Doctor)
    if payload.location_city:
        stmt = stmt.where(Doctor.city == payload.location_city)

    doctors = db.scalars(stmt).all()
    scored = []
    explanations: list[RankingExplainResponse] = []

    for doctor in doctors:
        result = doctor_score(severity, doctor, patient_loc, payload.budget, emergency_type)
        adjusted_total = _apply_weighted_score(result["breakdown"], weights_dict, adjustments)
        doctor.ai_score = round(adjusted_total, 2)
        scored.append((doctor, result["breakdown"], result["distance_km"]))

    scored.sort(key=lambda x: x[0].ai_score, reverse=True)
    top = scored[: payload.max_results]

    for idx, (doctor, breakdown, _distance) in enumerate(top, start=1):
        why = explain_top_factor(breakdown) if idx == 1 else None
        explanations.append(
            RankingExplainResponse(
                target_id=doctor.id,
                target_type="doctor",
                score_total=doctor.ai_score,
                breakdown=breakdown,
                why_ranked_1=why,
            )
        )
        db.add(
            RankingScore(
                emergency_id=payload.emergency_id,
                target_type="doctor",
                target_id=doctor.id,
                score_total=doctor.ai_score,
                breakdown=breakdown,
            )
        )

    db.commit()
    return DoctorRankingResponse(doctors=[d for d, _b, _dist in top], explanations=explanations)


@router.post("/rank/ambulances", response_model=AmbulanceRankingResponse)
def rank_ambulances(payload: RankingRequest, db: Session = Depends(get_db)):
    emergency, severity, _emergency_type, patient_loc = _emergency_context(db, payload.emergency_id, payload.severity)
    if payload.latitude is not None and payload.longitude is not None:
        patient_loc = (payload.latitude, payload.longitude)
    adjustments = load_adjustments(db)
    weights = SEVERITY_WEIGHTS_AMBULANCE.get(severity, SEVERITY_WEIGHTS_AMBULANCE["LOW"])

    stmt = select(Ambulance)
    if payload.location_city:
        stmt = stmt.where(Ambulance.city == payload.location_city)

    ambulances = db.scalars(stmt).all()
    scored = []
    explanations: list[RankingExplainResponse] = []

    for ambulance in ambulances:
        result = ambulance_score(severity, ambulance, patient_loc, payload.budget)
        adjusted_total = _apply_weighted_score(result["breakdown"], weights, adjustments)
        ambulance.ai_score = round(adjusted_total, 2)
        scored.append((ambulance, result["breakdown"], result["distance_km"]))

    scored.sort(key=lambda x: x[0].ai_score, reverse=True)
    top = scored[: payload.max_results]

    for idx, (ambulance, breakdown, _distance) in enumerate(top, start=1):
        why = explain_top_factor(breakdown) if idx == 1 else None
        explanations.append(
            RankingExplainResponse(
                target_id=ambulance.id,
                target_type="ambulance",
                score_total=ambulance.ai_score,
                breakdown=breakdown,
                why_ranked_1=why,
            )
        )
        db.add(
            RankingScore(
                emergency_id=payload.emergency_id,
                target_type="ambulance",
                target_id=ambulance.id,
                score_total=ambulance.ai_score,
                breakdown=breakdown,
            )
        )

    db.commit()
    return AmbulanceRankingResponse(ambulances=[a for a, _b, _dist in top], explanations=explanations)


@router.post("/rank/hospitals", response_model=HospitalRankingResponse)
def rank_hospitals(payload: RankingRequest, db: Session = Depends(get_db)):
    emergency, severity, emergency_type, patient_loc = _emergency_context(db, payload.emergency_id, payload.severity)
    if payload.latitude is not None and payload.longitude is not None:
        patient_loc = (payload.latitude, payload.longitude)
    adjustments = load_adjustments(db)
    weights = SEVERITY_WEIGHTS_HOSPITAL.get(severity, SEVERITY_WEIGHTS_HOSPITAL["LOW"])

    stmt = select(Hospital)
    if payload.location_city:
        stmt = stmt.where(Hospital.city == payload.location_city)

    hospitals = db.scalars(stmt).all()
    scored = []
    explanations: list[RankingExplainResponse] = []

    for hospital in hospitals:
        result = hospital_score(severity, hospital, patient_loc, payload.budget, emergency_type)
        adjusted_total = _apply_weighted_score(result["breakdown"], weights, adjustments)
        hospital.ai_score = round(adjusted_total, 2)
        scored.append((hospital, result["breakdown"], result["distance_km"]))

    scored.sort(key=lambda x: x[0].ai_score, reverse=True)
    top = scored[: payload.max_results]

    for idx, (hospital, breakdown, _distance) in enumerate(top, start=1):
        why = explain_top_factor(breakdown) if idx == 1 else None
        explanations.append(
            RankingExplainResponse(
                target_id=hospital.id,
                target_type="hospital",
                score_total=hospital.ai_score,
                breakdown=breakdown,
                why_ranked_1=why,
            )
        )
        db.add(
            RankingScore(
                emergency_id=payload.emergency_id,
                target_type="hospital",
                target_id=hospital.id,
                score_total=hospital.ai_score,
                breakdown=breakdown,
            )
        )

    db.commit()
    return HospitalRankingResponse(hospitals=[h for h, _b, _dist in top], explanations=explanations)


@router.get("/why-ranked/{emergency_id}/{target_type}/{target_id}", response_model=RankingExplainResponse)
def why_ranked(emergency_id: str, target_type: str, target_id: int, db: Session = Depends(get_db)):
    score = db.scalars(
        select(RankingScore)
        .where(RankingScore.emergency_id == emergency_id)
        .where(RankingScore.target_type == target_type)
        .where(RankingScore.target_id == target_id)
        .order_by(RankingScore.created_at.desc())
    ).first()
    if score:
        return RankingExplainResponse(
            target_id=score.target_id,
            target_type=score.target_type,
            score_total=score.score_total,
            breakdown=score.breakdown,
            why_ranked_1=explain_top_factor(score.breakdown),
        )
    raise HTTPException(status_code=404, detail="Ranking explanation not found")
