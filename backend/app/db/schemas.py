from datetime import datetime

from pydantic import BaseModel, Field


class DoctorOut(BaseModel):
    id: int
    name: str
    photo_url: str
    category: str
    city: str
    state: str
    country: str
    qualification: str
    college: str
    experience_years: int
    rating: float
    reviews_count: int
    consultation_fee: float
    total_patients_served: int
    response_time_minutes: int
    verified_status: bool
    availability_status: str
    languages: str
    whatsapp_link: str
    phone_number: str
    ai_score: float

    class Config:
        from_attributes = True


class AmbulanceOut(BaseModel):
    id: int
    provider_name: str
    city: str
    state: str
    vehicle_type: str
    response_time_minutes: int
    cost_per_km: float
    base_price: float
    availability_status: str
    rating: float
    verified_status: bool
    total_cases_handled: int
    equipment_list: str
    phone_number: str
    whatsapp_link: str
    ai_score: float

    class Config:
        from_attributes = True


class CompareRequest(BaseModel):
    entity_type: str
    ids: list[int]
    city: str | None = None
    category: str | None = None
    budget: float | None = None


class CompareResponse(BaseModel):
    winner_id: int
    winner_name: str
    score: float
    reason: str


class EmergencyRecommendRequest(BaseModel):
    location: str
    problem: str
    budget: float = Field(ge=0)
    service_preference: str = "both"  # doctor / ambulance / both
    min_rating: float | None = Field(default=None, ge=0, le=5)
    suggestion_count: int = Field(default=20, ge=1, le=100)


class EmergencyRecommendResponse(BaseModel):
    doctors: list[DoctorOut]
    ambulances: list[AmbulanceOut]
    top_doctor_summary: str
    top_ambulance_summary: str
    final_recommendation: str
    compared_doctors: int = 0
    compared_ambulances: int = 0


class AnalyticsResponse(BaseModel):
    average_fee_per_city: list[dict]
    fastest_ambulance_per_city: list[dict]
    most_experienced_doctor_per_city: list[dict]
    demand_category_analysis: list[dict]
    demand_by_city: list[dict]


class ChatSessionCreate(BaseModel):
    doctor_id: int
    user_name: str = "Guest"


class ChatMessageCreate(BaseModel):
    sender_type: str
    message: str
    file_url: str = ""


class ChatSessionOut(BaseModel):
    id: int
    doctor_id: int
    user_name: str
    started_at: datetime
    last_message_at: datetime

    class Config:
        from_attributes = True


class ChatMessageOut(BaseModel):
    id: int
    session_id: int
    sender_type: str
    message: str
    file_url: str
    created_at: datetime

    class Config:
        from_attributes = True


class TrackingStartRequest(BaseModel):
    provider_type: str  # doctor / ambulance
    provider_id: int
    city: str


class TrackingStartResponse(BaseModel):
    tracking_id: int
    provider_type: str
    provider_id: int
    eta_seconds: int
    status: str


class TrackingStatusResponse(BaseModel):
    tracking_id: int
    status: str
    eta_seconds: int
    progress_percent: float
    simulated_location: dict


class MetaOptionsResponse(BaseModel):
    cities: list[str]
    countries: list[str]
    doctor_categories: list[str]
    ambulance_types: list[str]
    problem_suggestions: list[str]
    budget_suggestions: list[int]


class BookingCreate(BaseModel):
    provider_type: str
    provider_id: int
    city: str
    user_name: str = "Guest"
    user_phone: str = ""
    notes: str = ""
    payment_method: str = "COD"  # COD / UPI / RAZORPAY
    upi_id: str = ""
    distance_km: float = 8.0


class BookingOut(BaseModel):
    id: int
    provider_type: str
    provider_id: int
    user_name: str
    user_phone: str
    city: str
    status: str
    notes: str
    created_at: datetime

    class Config:
        from_attributes = True


class BookingCheckoutResponse(BaseModel):
    booking: BookingOut
    tracking_id: int
    eta_seconds: int
    payment_method: str
    payment_status: str
    payment_amount: float
    razorpay_checkout_url: str = ""


class BookingTrackingResponse(BaseModel):
    booking_id: int
    booking_status: str
    tracking_id: int
    eta_seconds: int
    progress_percent: float
    timeline: list[dict]
    simulated_location: dict
