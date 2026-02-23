from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Doctor
from app.db.schemas import DoctorOut
from app.db.session import get_db
from app.services.scoring_service import score_doctors

router = APIRouter(prefix="", tags=["Doctors"])


@router.get("/doctors", response_model=list[DoctorOut])
def get_doctors(
    city: str | None = Query(default=None),
    category: str | None = Query(default=None),
    country: str | None = Query(default=None),
    max_fee: float | None = Query(default=None),
    min_rating: float | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=300),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    stmt = select(Doctor)
    if city:
        stmt = stmt.where(Doctor.city.ilike(f"%{city}%"))
    if category:
        stmt = stmt.where(Doctor.category.ilike(f"%{category}%"))
    if country:
        stmt = stmt.where(Doctor.country.ilike(f"%{country}%"))
    if max_fee is not None:
        stmt = stmt.where(Doctor.consultation_fee <= max_fee)
    if min_rating is not None:
        stmt = stmt.where(Doctor.rating >= min_rating)

    doctors = db.scalars(stmt.limit(5000)).all()
    ranked = score_doctors(doctors)
    for doctor in ranked[:200]:
        db.add(doctor)
    db.commit()
    return ranked[offset : offset + limit]


@router.get("/doctor/{doctor_id}", response_model=DoctorOut)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor
