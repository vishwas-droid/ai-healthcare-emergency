from __future__ import annotations

from datetime import datetime
import uuid

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, JSON
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
    response_time_seconds: Mapped[int] = mapped_column(Integer, default=0)
    verified_status: Mapped[bool] = mapped_column(Boolean, default=False)
    availability_status: Mapped[str] = mapped_column(String(40), default="Online")
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    languages: Mapped[str] = mapped_column(String(200), default="English")
    whatsapp_link: Mapped[str] = mapped_column(String(255), default="")
    phone_number: Mapped[str] = mapped_column(String(30), default="")
    ai_score: Mapped[float] = mapped_column(Float, default=0)
    rating_count: Mapped[int] = mapped_column(Integer, default=0)
    success_rate: Mapped[float] = mapped_column(Float, default=85.0)
    latitude: Mapped[float] = mapped_column(Float, default=0.0)
    longitude: Mapped[float] = mapped_column(Float, default=0.0)

    specialties = relationship("DoctorSpecialty", back_populates="doctor", cascade="all,delete-orphan")


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
    driver_score: Mapped[float] = mapped_column(Float, default=85.0)
    has_icu: Mapped[bool] = mapped_column(Boolean, default=False)
    has_oxygen: Mapped[bool] = mapped_column(Boolean, default=True)
    has_ventilator: Mapped[bool] = mapped_column(Boolean, default=False)
    response_time_seconds: Mapped[int] = mapped_column(Integer, default=0)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    latitude: Mapped[float] = mapped_column(Float, default=0.0)
    longitude: Mapped[float] = mapped_column(Float, default=0.0)


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    role: Mapped[str] = mapped_column(String(20), default="PATIENT")
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(30), unique=True, default="")
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Hospital(Base):
    __tablename__ = "hospitals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    city: Mapped[str] = mapped_column(String(80), index=True)
    state: Mapped[str] = mapped_column(String(80), default="")
    country: Mapped[str] = mapped_column(String(80), default="India")
    icu_beds_available: Mapped[int] = mapped_column(Integer, default=0)
    emergency_wait_minutes: Mapped[int] = mapped_column(Integer, default=30)
    success_rate: Mapped[float] = mapped_column(Float, default=85.0)
    avg_cost_index: Mapped[float] = mapped_column(Float, default=1.0)
    distance_km_estimate: Mapped[float] = mapped_column(Float, default=0.0)
    latitude: Mapped[float] = mapped_column(Float, default=0.0)
    longitude: Mapped[float] = mapped_column(Float, default=0.0)
    phone_number: Mapped[str] = mapped_column(String(30), default="")
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    ai_score: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    specializations = relationship("HospitalSpecialization", back_populates="hospital", cascade="all,delete-orphan")


class Emergency(Base):
    __tablename__ = "emergencies"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_user_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    complaint_text: Mapped[str] = mapped_column(Text, default="")
    complaint_text_encrypted: Mapped[str] = mapped_column(Text, default="")
    severity: Mapped[str] = mapped_column(String(20), default="LOW")
    severity_score: Mapped[int] = mapped_column(Integer, default=0)
    emergency_type: Mapped[str] = mapped_column(String(40), default="Other")
    status: Mapped[str] = mapped_column(String(20), default="OPEN")
    latitude: Mapped[float] = mapped_column(Float, default=0.0)
    longitude: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class TriageLog(Base):
    __tablename__ = "triage_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    emergency_id: Mapped[str] = mapped_column(String(36), ForeignKey("emergencies.id"))
    entities: Mapped[dict] = mapped_column(JSON, default=dict)
    risk_flags: Mapped[list] = mapped_column(JSON, default=list)
    llm_output: Mapped[dict] = mapped_column(JSON, default=dict)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class RankingScore(Base):
    __tablename__ = "ranking_scores"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    emergency_id: Mapped[str] = mapped_column(String(36), ForeignKey("emergencies.id"))
    target_type: Mapped[str] = mapped_column(String(40), index=True)
    target_id: Mapped[int] = mapped_column(Integer, index=True)
    score_total: Mapped[float] = mapped_column(Float, default=0.0)
    breakdown: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    emergency_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("emergencies.id"), nullable=True)
    event_type: Mapped[str] = mapped_column(String(80), index=True)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class FeedbackOutcome(Base):
    __tablename__ = "feedback_outcomes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    emergency_id: Mapped[str] = mapped_column(String(36), ForeignKey("emergencies.id"))
    outcome: Mapped[str] = mapped_column(String(60), default="")
    response_time_seconds: Mapped[int] = mapped_column(Integer, default=0)
    satisfaction_score: Mapped[int] = mapped_column(Integer, default=0)
    survival: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class DoctorSpecialty(Base):
    __tablename__ = "doctor_specialties"

    doctor_id: Mapped[int] = mapped_column(Integer, ForeignKey("doctors.id"), primary_key=True)
    specialty: Mapped[str] = mapped_column(String(80), primary_key=True)

    doctor = relationship("Doctor", back_populates="specialties")


class HospitalSpecialization(Base):
    __tablename__ = "hospital_specializations"

    hospital_id: Mapped[int] = mapped_column(Integer, ForeignKey("hospitals.id"), primary_key=True)
    specialization: Mapped[str] = mapped_column(String(80), primary_key=True)

    hospital = relationship("Hospital", back_populates="specializations")


class EmergencyAssignment(Base):
    __tablename__ = "emergency_assignments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    emergency_id: Mapped[str] = mapped_column(String(36), ForeignKey("emergencies.id"))
    doctor_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("doctors.id"), nullable=True)
    ambulance_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("ambulances.id"), nullable=True)
    hospital_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("hospitals.id"), nullable=True)
    mode: Mapped[str | None] = mapped_column(String(40), default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


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
