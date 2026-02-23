from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import encrypt_text
from app.db.models import Emergency, TriageLog
from app.db.schemas import TriageRequest, TriageResponse
from app.db.session import get_db
from app.services.triage_engine import triage

router = APIRouter(prefix="", tags=["Triage"])


@router.post("/triage", response_model=TriageResponse)
def run_triage(payload: TriageRequest, db: Session = Depends(get_db)):
    result = triage(payload.complaint_text)

    emergency = Emergency(
        patient_user_id=payload.user_id,
        complaint_text="REDACTED",
        complaint_text_encrypted=encrypt_text(payload.complaint_text),
        severity=result["severity"],
        severity_score=result["severity_score"],
        emergency_type=result["emergency_type"],
        status="OPEN",
        latitude=payload.latitude or 0.0,
        longitude=payload.longitude or 0.0,
    )
    db.add(emergency)
    db.commit()
    db.refresh(emergency)

    log = TriageLog(
        emergency_id=emergency.id,
        entities=result["entities"],
        risk_flags=result["risk_flags"],
        llm_output=result,
        confidence=result["confidence"],
    )
    db.add(log)
    db.commit()

    return TriageResponse(emergency_id=emergency.id, **result)
