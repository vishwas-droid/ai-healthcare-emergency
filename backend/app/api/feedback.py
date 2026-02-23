from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import Emergency, FeedbackOutcome
from app.db.schemas import FeedbackRequest
from app.db.session import get_db
from app.services.feedback_loop import update_adjustments

router = APIRouter(prefix="", tags=["Feedback"])


@router.post("/feedback")
def record_feedback(payload: FeedbackRequest, db: Session = Depends(get_db)):
    emergency = db.get(Emergency, payload.emergency_id)
    if not emergency:
        raise HTTPException(status_code=404, detail="Emergency not found")

    outcome = FeedbackOutcome(
        emergency_id=payload.emergency_id,
        outcome=payload.outcome,
        response_time_seconds=payload.response_time_seconds,
        satisfaction_score=payload.satisfaction_score,
        survival=payload.survival,
        notes=payload.notes or "",
    )
    db.add(outcome)
    if payload.survival is not None:
        emergency.status = "RESOLVED"
        db.add(emergency)
    db.commit()

    adjustments = update_adjustments(db, outcome)
    return {"status": "ok", "adjustments": adjustments}
