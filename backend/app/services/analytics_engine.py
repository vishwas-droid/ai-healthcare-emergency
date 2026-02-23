from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta
import random
from typing import Dict, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import AnalyticsEvent, Emergency


def _default_forecast() -> Dict[str, List[dict]]:
    rng = random.Random(20260223)
    peak_hours = [{"hour": h, "score": rng.randint(60, 95)} for h in [8, 12, 18, 22]]
    cardiac = [{"hour": h, "probability": round(rng.uniform(0.12, 0.35), 2)} for h in range(0, 24, 3)]
    demand = [{"hour": (datetime.utcnow() + timedelta(hours=i)).hour, "forecast": rng.randint(40, 120)} for i in range(1, 7)]
    zones = [
        {"zone": "Mumbai South", "risk": rng.randint(70, 90)},
        {"zone": "Delhi NCR", "risk": rng.randint(65, 88)},
        {"zone": "Bengaluru Central", "risk": rng.randint(60, 85)},
    ]
    return {
        "peak_hours": peak_hours,
        "cardiac_spike_probability": cardiac,
        "demand_forecast": demand,
        "high_risk_zones": zones,
    }


def forecast(db: Session) -> Dict[str, List[dict]]:
    cutoff = datetime.utcnow() - timedelta(days=7)
    emergencies = db.scalars(select(Emergency).where(Emergency.created_at >= cutoff)).all()
    if not emergencies:
        return _default_forecast()

    hours = [e.created_at.hour for e in emergencies]
    counter = Counter(hours)
    peak_hours = [{"hour": hour, "score": min(100, count * 8)} for hour, count in counter.most_common(4)]

    cardiac = [
        {
            "hour": h,
            "probability": round(
                sum(1 for e in emergencies if e.created_at.hour == h and e.emergency_type == "Cardiac")
                / max(1, sum(1 for e in emergencies if e.created_at.hour == h)),
                2,
            ),
        }
        for h in range(0, 24, 3)
    ]

    demand = []
    for i in range(1, 7):
        hour = (datetime.utcnow() + timedelta(hours=i)).hour
        base = counter.get(hour, 5)
        demand.append({"hour": hour, "forecast": int(base * 10)})

    events = db.scalars(select(AnalyticsEvent).where(AnalyticsEvent.created_at >= cutoff)).all()
    zone_counter = Counter()
    for event in events:
        zone = event.payload.get("zone") if isinstance(event.payload, dict) else None
        if zone:
            zone_counter[zone] += 1

    zones = [{"zone": z, "risk": min(100, c * 5)} for z, c in zone_counter.most_common(5)]
    if not zones:
        zones = _default_forecast()["high_risk_zones"]

    return {
        "peak_hours": peak_hours,
        "cardiac_spike_probability": cardiac,
        "demand_forecast": demand,
        "high_risk_zones": zones,
    }
