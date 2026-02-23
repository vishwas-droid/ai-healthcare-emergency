from fastapi import APIRouter, Depends
from sqlalchemy import distinct, select
from sqlalchemy.orm import Session

from app.db.models import Ambulance, Doctor
from app.db.schemas import MetaOptionsResponse
from app.db.session import get_db

router = APIRouter(prefix="", tags=["Meta"])


@router.get("/meta/options", response_model=MetaOptionsResponse)
def get_meta_options(db: Session = Depends(get_db)):
    cities = sorted(
        {
            *[c for c in db.scalars(select(distinct(Doctor.city)).limit(500)).all() if c],
            *[c for c in db.scalars(select(distinct(Ambulance.city)).limit(500)).all() if c],
        }
    )
    countries = sorted([c for c in db.scalars(select(distinct(Doctor.country)).limit(100)).all() if c])
    doctor_categories = sorted([c for c in db.scalars(select(distinct(Doctor.category)).limit(100)).all() if c])
    ambulance_types = sorted([c for c in db.scalars(select(distinct(Ambulance.vehicle_type)).limit(100)).all() if c])

    return MetaOptionsResponse(
        cities=cities,
        countries=countries,
        doctor_categories=doctor_categories,
        ambulance_types=ambulance_types,
        problem_suggestions=[
            "chest pain",
            "heart attack symptoms",
            "high fever",
            "stroke signs",
            "child emergency",
            "accident trauma",
            "breathing problem",
            "pregnancy emergency",
        ],
        budget_suggestions=[800, 1200, 2000, 3000, 5000, 8000],
    )
