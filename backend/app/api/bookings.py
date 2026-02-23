from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Ambulance, Booking, Doctor
from app.db.schemas import BookingCreate, BookingOut
from app.db.session import get_db

router = APIRouter(prefix="", tags=["Bookings"])


@router.post("/bookings", response_model=BookingOut)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    provider_type = payload.provider_type.upper()
    if provider_type == "DOCTOR":
        if not db.get(Doctor, payload.provider_id):
            raise HTTPException(status_code=404, detail="Doctor not found")
    elif provider_type == "AMBULANCE":
        if not db.get(Ambulance, payload.provider_id):
            raise HTTPException(status_code=404, detail="Ambulance not found")
    else:
        raise HTTPException(status_code=400, detail="provider_type must be doctor or ambulance")

    booking = Booking(
        provider_type=provider_type,
        provider_id=payload.provider_id,
        user_name=payload.user_name,
        user_phone=payload.user_phone,
        city=payload.city,
        status="CONFIRMED",
        notes=payload.notes,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.get("/bookings", response_model=list[BookingOut])
def list_bookings(
    provider_type: str | None = Query(default=None),
    city: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    stmt = select(Booking)
    if provider_type:
        stmt = stmt.where(Booking.provider_type == provider_type.upper())
    if city:
        stmt = stmt.where(Booking.city.ilike(f"%{city}%"))
    return db.scalars(stmt.order_by(Booking.created_at.desc()).limit(limit)).all()
