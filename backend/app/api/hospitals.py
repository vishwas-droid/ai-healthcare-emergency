from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Hospital
from app.db.schemas import HospitalOut
from app.db.session import get_db

router = APIRouter(prefix="", tags=["Hospitals"])


@router.get("/hospitals", response_model=list[HospitalOut])
def list_hospitals(city: str | None = None, min_icu: int | None = None, db: Session = Depends(get_db)):
    stmt = select(Hospital)
    if city:
        stmt = stmt.where(Hospital.city == city)
    if min_icu is not None:
        stmt = stmt.where(Hospital.icu_beds_available >= min_icu)
    return db.scalars(stmt).all()


@router.get("/hospitals/{hospital_id}", response_model=HospitalOut)
def get_hospital(hospital_id: int, db: Session = Depends(get_db)):
    hospital = db.get(Hospital, hospital_id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital
