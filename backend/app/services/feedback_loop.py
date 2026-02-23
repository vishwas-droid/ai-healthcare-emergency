from __future__ import annotations

from datetime import datetime
from typing import Dict

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import AnalyticsEvent, FeedbackOutcome

DEFAULT_ADJUSTMENTS: Dict[str, float] = {
    "experience": 1.0,
    "bayesian": 1.0,
    "distance": 1.0,
    "response": 1.0,
    "availability": 1.0,
    "emergency_match": 1.0,
    "budget": 1.0,
    "success": 1.0,
    "equipment": 1.0,
    "driver": 1.0,
    "cost": 1.0,
    "icu": 1.0,
    "wait": 1.0,
    "specialty": 1.0,
}


def load_adjustments(db: Session) -> Dict[str, float]:
    event = db.scalars(
        select(AnalyticsEvent)
        .where(AnalyticsEvent.event_type == "weight_update")
        .order_by(AnalyticsEvent.created_at.desc())
    ).first()
    if event and isinstance(event.payload, dict):
        return {**DEFAULT_ADJUSTMENTS, **event.payload}
    return DEFAULT_ADJUSTMENTS.copy()


def update_adjustments(db: Session, feedback: FeedbackOutcome) -> Dict[str, float]:
    adjustments = load_adjustments(db)

    if feedback.satisfaction_score >= 8 and feedback.survival:
        adjustments["response"] = min(1.25, adjustments["response"] + 0.03)
        adjustments["availability"] = min(1.25, adjustments["availability"] + 0.03)
        adjustments["success"] = min(1.25, adjustments["success"] + 0.02)
    elif feedback.satisfaction_score <= 4:
        adjustments["budget"] = min(1.25, adjustments["budget"] + 0.04)
        adjustments["distance"] = min(1.25, adjustments["distance"] + 0.03)
        adjustments["wait"] = min(1.25, adjustments["wait"] + 0.03)
    else:
        adjustments["emergency_match"] = min(1.20, adjustments["emergency_match"] + 0.01)

    event = AnalyticsEvent(
        event_type="weight_update",
        payload=adjustments,
        created_at=datetime.utcnow(),
    )
    db.add(event)
    db.commit()
    return adjustments
