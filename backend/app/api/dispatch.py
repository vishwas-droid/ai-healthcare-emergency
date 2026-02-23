from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import Ambulance, Doctor, Emergency, EmergencyAssignment, Hospital, TrackingSession
from app.db.schemas import DispatchRequest, DispatchResponse
from app.db.session import get_db
from app.services.dispatch_engine import estimate_eta_seconds

router = APIRouter(prefix="", tags=["Dispatch"])


@router.post("/dispatch", response_model=DispatchResponse)
def dispatch_emergency(payload: DispatchRequest, db: Session = Depends(get_db)):
    emergency = db.get(Emergency, payload.emergency_id)
    if not emergency:
        raise HTTPException(status_code=404, detail="Emergency not found")

    provider_type = None
    provider_id = None
    dest_lat = 0.0
    dest_lng = 0.0
    city = ""

    if payload.ambulance_id:
        ambulance = db.get(Ambulance, payload.ambulance_id)
        if not ambulance:
            raise HTTPException(status_code=404, detail="Ambulance not found")
        provider_type = "AMBULANCE"
        provider_id = ambulance.id
        dest_lat, dest_lng = ambulance.latitude, ambulance.longitude
        city = ambulance.city
    elif payload.doctor_id:
        doctor = db.get(Doctor, payload.doctor_id)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        provider_type = "DOCTOR"
        provider_id = doctor.id
        dest_lat, dest_lng = doctor.latitude, doctor.longitude
        city = doctor.city
    elif payload.hospital_id:
        hospital = db.get(Hospital, payload.hospital_id)
        if not hospital:
            raise HTTPException(status_code=404, detail="Hospital not found")
        provider_type = "HOSPITAL"
        provider_id = hospital.id
        dest_lat, dest_lng = hospital.latitude, hospital.longitude
        city = hospital.city
    else:
        raise HTTPException(status_code=400, detail="No provider selected")

    origin = (emergency.latitude or 0.0, emergency.longitude or 0.0)
    dest = (dest_lat or 0.0, dest_lng or 0.0)
    eta_seconds = estimate_eta_seconds(origin, dest)

    assignment = EmergencyAssignment(
        emergency_id=payload.emergency_id,
        doctor_id=payload.doctor_id,
        ambulance_id=payload.ambulance_id,
        hospital_id=payload.hospital_id,
        mode=payload.mode,
    )
    db.add(assignment)

    tracking = TrackingSession(
        provider_type=provider_type,
        provider_id=provider_id,
        city=city,
        eta_seconds_initial=eta_seconds,
        status="EN_ROUTE",
    )
    db.add(tracking)

    emergency.status = "DISPATCHED"
    db.add(emergency)
    db.commit()
    db.refresh(assignment)
    db.refresh(tracking)

    return DispatchResponse(
        emergency_id=payload.emergency_id,
        assignment_id=assignment.id,
        status=emergency.status,
        eta_seconds=eta_seconds,
        tracking_id=tracking.id,
    )
