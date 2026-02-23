from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    photo_url: Mapped[str] = mapped_column(String(255), default="")
    category: Mapped[str] = mapped_column(String(80), index=True)
    city: Mapped[str] = mapped_column(String(80), index=True)
    state: Mapped[str] = mapped_column(String(80), default="")
    country: Mapped[str] = mapped_column(String(80), default="India")
    qualification: Mapped[str] = mapped_column(String(120), default="")
    college: Mapped[str] = mapped_column(String(120), default="")
    experience_years: Mapped[int] = mapped_column(Integer, default=0)
    rating: Mapped[float] = mapped_column(Float, default=0)
    reviews_count: Mapped[int] = mapped_column(Integer, default=0)
    consultation_fee: Mapped[float] = mapped_column(Float, default=0)
    total_patients_served: Mapped[int] = mapped_column(Integer, default=0)
    response_time_minutes: Mapped[int] = mapped_column(Integer, default=30)
    verified_status: Mapped[bool] = mapped_column(Boolean, default=False)
    availability_status: Mapped[str] = mapped_column(String(40), default="Online")
    languages: Mapped[str] = mapped_column(String(200), default="English")
    whatsapp_link: Mapped[str] = mapped_column(String(255), default="")
    phone_number: Mapped[str] = mapped_column(String(30), default="")
    ai_score: Mapped[float] = mapped_column(Float, default=0)


class Ambulance(Base):
    __tablename__ = "ambulances"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    provider_name: Mapped[str] = mapped_column(String(120), nullable=False)
    city: Mapped[str] = mapped_column(String(80), index=True)
    state: Mapped[str] = mapped_column(String(80), default="")
    vehicle_type: Mapped[str] = mapped_column(String(40), index=True)
    response_time_minutes: Mapped[int] = mapped_column(Integer, default=20)
    cost_per_km: Mapped[float] = mapped_column(Float, default=0)
    base_price: Mapped[float] = mapped_column(Float, default=0)
    availability_status: Mapped[str] = mapped_column(String(40), default="AVAILABLE")
    rating: Mapped[float] = mapped_column(Float, default=0)
    verified_status: Mapped[bool] = mapped_column(Boolean, default=False)
    total_cases_handled: Mapped[int] = mapped_column(Integer, default=0)
    equipment_list: Mapped[str] = mapped_column(Text, default="")
    phone_number: Mapped[str] = mapped_column(String(30), default="")
    whatsapp_link: Mapped[str] = mapped_column(String(255), default="")
    ai_score: Mapped[float] = mapped_column(Float, default=0)


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    doctor_id: Mapped[int] = mapped_column(Integer, ForeignKey("doctors.id"), index=True)
    user_name: Mapped[str] = mapped_column(String(100), default="Guest")
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_message_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    doctor = relationship("Doctor")
    messages = relationship("ChatMessage", back_populates="session", cascade="all,delete-orphan")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(Integer, ForeignKey("chat_sessions.id"), index=True)
    sender_type: Mapped[str] = mapped_column(String(20))
    message: Mapped[str] = mapped_column(Text, default="")
    file_url: Mapped[str] = mapped_column(String(255), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")


class SearchEvent(Base):
    __tablename__ = "search_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    city: Mapped[str] = mapped_column(String(80), index=True)
    problem: Mapped[str] = mapped_column(String(120), index=True)
    budget: Mapped[float] = mapped_column(Float, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class TrackingSession(Base):
    __tablename__ = "tracking_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    provider_type: Mapped[str] = mapped_column(String(20), index=True)  # DOCTOR / AMBULANCE
    provider_id: Mapped[int] = mapped_column(Integer, index=True)
    city: Mapped[str] = mapped_column(String(80), index=True)
    eta_seconds_initial: Mapped[int] = mapped_column(Integer)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(20), default="EN_ROUTE")


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    provider_type: Mapped[str] = mapped_column(String(20), index=True)  # DOCTOR / AMBULANCE
    provider_id: Mapped[int] = mapped_column(Integer, index=True)
    user_name: Mapped[str] = mapped_column(String(120), default="Guest")
    user_phone: Mapped[str] = mapped_column(String(30), default="")
    city: Mapped[str] = mapped_column(String(80), index=True)
    status: Mapped[str] = mapped_column(String(20), default="CONFIRMED")
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class BookingPayment(Base):
    __tablename__ = "booking_payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    booking_id: Mapped[int] = mapped_column(Integer, ForeignKey("bookings.id"), index=True)
    method: Mapped[str] = mapped_column(String(20), default="COD")  # COD / UPI / RAZORPAY
    amount: Mapped[float] = mapped_column(Float, default=0)
    status: Mapped[str] = mapped_column(String(20), default="PENDING")  # PENDING / PAID / COD_DUE
    upi_id: Mapped[str] = mapped_column(String(120), default="")
    transaction_ref: Mapped[str] = mapped_column(String(120), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
