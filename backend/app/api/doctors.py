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
    max_fee: float | None = Query(default=None),
    min_rating: float | None = Query(default=None),
    db: Session = Depends(get_db),
):
    stmt = select(Doctor)
    if city:
        stmt = stmt.where(Doctor.city.ilike(f"%{city}%"))
    if category:
        stmt = stmt.where(Doctor.category.ilike(f"%{category}%"))
    if max_fee is not None:
        stmt = stmt.where(Doctor.consultation_fee <= max_fee)
    if min_rating is not None:
        stmt = stmt.where(Doctor.rating >= min_rating)

    doctors = db.scalars(stmt).all()
    ranked = score_doctors(doctors)
    for doctor in ranked:
        db.add(doctor)
    db.commit()
    return ranked


@router.get("/doctor/{doctor_id}", response_model=DoctorOut)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor
