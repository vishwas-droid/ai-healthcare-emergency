import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Ambulance, Booking, BookingPayment, Doctor, TrackingSession
from app.db.schemas import (
    BookingCheckoutResponse,
    BookingCreate,
    BookingOut,
    BookingTrackingResponse,
)
from app.db.session import get_db

router = APIRouter(prefix="", tags=["Bookings"])


def _provider_eta_and_amount(payload: BookingCreate, db: Session) -> tuple[int, float]:
    ptype = payload.provider_type.upper()
    if ptype == "DOCTOR":
        doctor = db.get(Doctor, payload.provider_id)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        eta = doctor.response_time_seconds or doctor.response_time_minutes * 60
        return max(180, eta), float(doctor.consultation_fee)
    if ptype == "AMBULANCE":
        ambulance = db.get(Ambulance, payload.provider_id)
        if not ambulance:
            raise HTTPException(status_code=404, detail="Ambulance not found")
        amount = float(ambulance.base_price + (ambulance.cost_per_km * payload.distance_km))
        eta = ambulance.response_time_seconds or ambulance.response_time_minutes * 60
        return max(180, eta), amount
    raise HTTPException(status_code=400, detail="provider_type must be doctor or ambulance")


def _payment_status(method: str) -> str:
    m = method.upper()
    if m == "COD":
        return "COD_DUE"
    if m == "UPI":
        return "PAID"
    if m == "RAZORPAY":
        return "PENDING"
    raise HTTPException(status_code=400, detail="payment_method must be COD, UPI, or RAZORPAY")


@router.post("/bookings", response_model=BookingCheckoutResponse)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    eta_seconds, amount = _provider_eta_and_amount(payload, db)
    provider_type = payload.provider_type.upper()
    payment_method = payload.payment_method.upper()

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
    db.flush()

    payment = BookingPayment(
        booking_id=booking.id,
        method=payment_method,
        amount=amount,
        status=_payment_status(payment_method),
        upi_id=payload.upi_id,
        transaction_ref=f"TXN-{uuid.uuid4().hex[:10].upper()}",
    )
    db.add(payment)

    tracking = TrackingSession(
        provider_type=provider_type,
        provider_id=payload.provider_id,
        city=payload.city,
        eta_seconds_initial=eta_seconds,
        status="EN_ROUTE",
    )
    db.add(tracking)

    db.commit()
    db.refresh(booking)
    db.refresh(tracking)
    db.refresh(payment)

    razorpay_url = ""
    if payment_method == "RAZORPAY":
        razorpay_url = "https://razorpay.com/"  # Replace with actual order checkout URL when keys are configured.

    return BookingCheckoutResponse(
        booking=booking,
        tracking_id=tracking.id,
        eta_seconds=tracking.eta_seconds_initial,
        payment_method=payment.method,
        payment_status=payment.status,
        payment_amount=payment.amount,
        razorpay_checkout_url=razorpay_url,
    )


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


@router.get("/bookings/{booking_id}/track", response_model=BookingTrackingResponse)
def booking_tracking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    tracking = db.scalars(
        select(TrackingSession)
        .where(TrackingSession.provider_type == booking.provider_type)
        .where(TrackingSession.provider_id == booking.provider_id)
        .where(TrackingSession.city == booking.city)
        .order_by(TrackingSession.started_at.desc())
        .limit(1)
    ).first()

    if not tracking:
        raise HTTPException(status_code=404, detail="Tracking session not found for booking")

    elapsed = int((datetime.utcnow() - tracking.started_at).total_seconds())
    remaining = max(0, tracking.eta_seconds_initial - elapsed)
    progress = round(100 * (1 - (remaining / tracking.eta_seconds_initial)), 2)

    if remaining == 0 and tracking.status != "ARRIVED":
        tracking.status = "ARRIVED"
        booking.status = "COMPLETED"
        db.add(tracking)
        db.add(booking)
        db.commit()

    timeline = [
        {"step": "Booked", "done": True},
        {"step": "Confirmed", "done": True},
        {"step": "Assigned", "done": progress >= 20},
        {"step": "En Route", "done": progress >= 40},
        {"step": "Arriving", "done": progress >= 80},
        {"step": "Completed", "done": progress >= 100},
    ]

    simulated_location = {
        "lat": round(20.5937 + (0.02 * (1 - progress / 100)), 6),
        "lng": round(78.9629 + (0.02 * (1 - progress / 100)), 6),
    }

    return BookingTrackingResponse(
        booking_id=booking.id,
        booking_status=booking.status,
        tracking_id=tracking.id,
        eta_seconds=remaining,
        progress_percent=progress,
        timeline=timeline,
        simulated_location=simulated_location,
    )
