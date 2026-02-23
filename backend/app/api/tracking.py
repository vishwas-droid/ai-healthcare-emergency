from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import Ambulance, Doctor, TrackingSession
from app.db.schemas import (
    TrackingStartRequest,
    TrackingStartResponse,
    TrackingStatusResponse,
)
from app.db.session import get_db

router = APIRouter(prefix="", tags=["Tracking"])

CITY_BASE_COORDS = {
    "mumbai": {"lat": 19.0760, "lng": 72.8777},
    "delhi": {"lat": 28.6139, "lng": 77.2090},
    "bengaluru": {"lat": 12.9716, "lng": 77.5946},
}


def _base_eta_seconds(provider_type: str, provider_id: int, db: Session) -> int:
    p = provider_type.upper()
    if p == "DOCTOR":
        doctor = db.get(Doctor, provider_id)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return max(180, doctor.response_time_minutes * 60)

    if p == "AMBULANCE":
        ambulance = db.get(Ambulance, provider_id)
        if not ambulance:
            raise HTTPException(status_code=404, detail="Ambulance not found")
        return max(180, ambulance.response_time_minutes * 60)

    raise HTTPException(status_code=400, detail="provider_type must be doctor or ambulance")


@router.post("/tracking/start", response_model=TrackingStartResponse)
def start_tracking(payload: TrackingStartRequest, db: Session = Depends(get_db)):
    eta = _base_eta_seconds(payload.provider_type, payload.provider_id, db)
    session = TrackingSession(
        provider_type=payload.provider_type.upper(),
        provider_id=payload.provider_id,
        city=payload.city,
        eta_seconds_initial=eta,
        status="EN_ROUTE",
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return TrackingStartResponse(
        tracking_id=session.id,
        provider_type=session.provider_type,
        provider_id=session.provider_id,
        eta_seconds=session.eta_seconds_initial,
        status=session.status,
    )


@router.get("/tracking/{tracking_id}", response_model=TrackingStatusResponse)
def get_tracking_status(tracking_id: int, db: Session = Depends(get_db)):
    session = db.get(TrackingSession, tracking_id)
    if not session:
        raise HTTPException(status_code=404, detail="Tracking session not found")

    elapsed = int((datetime.utcnow() - session.started_at).total_seconds())
    remaining = max(0, session.eta_seconds_initial - elapsed)
    progress = round(100 * (1 - (remaining / session.eta_seconds_initial)), 2)

    if remaining == 0 and session.status != "ARRIVED":
        session.status = "ARRIVED"
        db.add(session)
        db.commit()

    base = CITY_BASE_COORDS.get(session.city.strip().lower(), {"lat": 20.5937, "lng": 78.9629})
    simulated = {
        "lat": round(base["lat"] + (0.02 * (1 - progress / 100)), 6),
        "lng": round(base["lng"] + (0.02 * (1 - progress / 100)), 6),
    }

    return TrackingStatusResponse(
        tracking_id=session.id,
        status=session.status,
        eta_seconds=remaining,
        progress_percent=progress,
        simulated_location=simulated,
    )
