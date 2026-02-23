from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.security import require_roles
from app.db.models import Ambulance, Doctor, Emergency, Hospital
from app.db.session import get_db

router = APIRouter(prefix="", tags=["Admin"])


@router.get("/admin/overview")
def admin_overview(db: Session = Depends(get_db), _user=Depends(require_roles("ADMIN"))):
    doctors = db.scalar(select(func.count(Doctor.id))) or 0
    ambulances = db.scalar(select(func.count(Ambulance.id))) or 0
    hospitals = db.scalar(select(func.count(Hospital.id))) or 0
    emergencies = db.scalar(select(func.count(Emergency.id))) or 0

    return {
        "doctors": doctors,
        "ambulances": ambulances,
        "hospitals": hospitals,
        "emergencies": emergencies,
    }
