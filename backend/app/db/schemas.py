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
    response_time_seconds: int = 0
    verified_status: bool
    availability_status: str
    is_available: bool = True
    languages: str
    whatsapp_link: str
    phone_number: str
    ai_score: float
    rating_count: int = 0
    success_rate: float = 85.0
    latitude: float = 0.0
    longitude: float = 0.0

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
    driver_score: float = 85.0
    has_icu: bool = False
    has_oxygen: bool = True
    has_ventilator: bool = False
    response_time_seconds: int = 0
    is_available: bool = True
    latitude: float = 0.0
    longitude: float = 0.0

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


class TriageRequest(BaseModel):
    complaint_text: str = Field(min_length=3)
    location_city: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    user_id: str | None = None


class TriageResponse(BaseModel):
    emergency_id: str
    severity: str
    severity_score: int
    emergency_type: str
    entities: dict
    recommended: dict
    risk_flags: list[str]
    escalation: dict
    confidence: float


class RankingRequest(BaseModel):
    emergency_id: str
    budget: float = Field(ge=0)
    severity: str
    location_city: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    max_results: int = Field(default=20, ge=1, le=100)


class RankingExplainResponse(BaseModel):
    target_id: int
    target_type: str
    score_total: float
    breakdown: dict
    why_ranked_1: str | None = None


class DoctorRankingResponse(BaseModel):
    doctors: list[DoctorOut]
    explanations: list[RankingExplainResponse]


class AmbulanceRankingResponse(BaseModel):
    ambulances: list[AmbulanceOut]
    explanations: list[RankingExplainResponse]


class HospitalOut(BaseModel):
    id: int
    name: str
    city: str
    state: str
    country: str
    icu_beds_available: int
    emergency_wait_minutes: int
    success_rate: float
    avg_cost_index: float
    distance_km_estimate: float
    latitude: float
    longitude: float
    phone_number: str
    is_available: bool
    ai_score: float = 0.0

    class Config:
        from_attributes = True


class HospitalRankingResponse(BaseModel):
    hospitals: list[HospitalOut]
    explanations: list[RankingExplainResponse]


class DispatchRequest(BaseModel):
    emergency_id: str
    doctor_id: int | None = None
    ambulance_id: int | None = None
    hospital_id: int | None = None
    mode: str | None = None  # FASTEST / CHEAPEST / CRITICAL_CARE


class DispatchResponse(BaseModel):
    emergency_id: str
    assignment_id: str
    status: str
    eta_seconds: int
    tracking_id: int


class TrackingRealtimeUpdate(BaseModel):
    tracking_id: int
    status: str
    eta_seconds: int
    progress_percent: float
    location: dict
    updated_at: datetime


class AnalyticsForecastResponse(BaseModel):
    peak_hours: list[dict]
    cardiac_spike_probability: list[dict]
    demand_forecast: list[dict]
    high_risk_zones: list[dict]


class FeedbackRequest(BaseModel):
    emergency_id: str
    outcome: str
    response_time_seconds: int
    satisfaction_score: int = Field(ge=1, le=10)
    survival: bool | None = None
    notes: str | None = None


class UserOut(BaseModel):
    id: str
    role: str
    full_name: str
    email: str
    phone: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AuthRegisterRequest(BaseModel):
    full_name: str
    email: str
    phone: str | None = None
    password: str = Field(min_length=6)
    role: str = \"PATIENT\"


class AuthLoginRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = \"bearer\"
    user: UserOut


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
