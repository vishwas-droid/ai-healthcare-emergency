from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import Ambulance, Doctor, SearchEvent
from app.db.schemas import AnalyticsForecastResponse, AnalyticsResponse
from app.db.session import get_db
from app.services.analytics_engine import forecast

router = APIRouter(prefix="", tags=["Analytics"])


@router.get("/analytics", response_model=AnalyticsResponse)
def get_analytics(db: Session = Depends(get_db)):
    avg_fee_rows = db.execute(
        select(Doctor.city, func.avg(Doctor.consultation_fee)).group_by(Doctor.city)
    ).all()
    avg_fee = [{"city": city, "average_fee": round(float(val), 2)} for city, val in avg_fee_rows]

    ambulances = db.scalars(select(Ambulance)).all()
    fastest_map: dict[str, Ambulance] = {}
    for ambulance in ambulances:
        current = fastest_map.get(ambulance.city)
        if current is None or ambulance.response_time_minutes < current.response_time_minutes:
            fastest_map[ambulance.city] = ambulance
    fastest = [
        {
            "city": city,
            "provider_name": item.provider_name,
            "response_time_minutes": item.response_time_minutes,
        }
        for city, item in fastest_map.items()
    ]

    doctors = db.scalars(select(Doctor)).all()
    experienced_map: dict[str, Doctor] = {}
    for doctor in doctors:
        current = experienced_map.get(doctor.city)
        if current is None or doctor.experience_years > current.experience_years:
            experienced_map[doctor.city] = doctor
    experienced = [
        {
            "city": city,
            "doctor_name": item.name,
            "experience_years": item.experience_years,
        }
        for city, item in experienced_map.items()
    ]

    demand_rows = db.execute(select(SearchEvent.problem, func.count(SearchEvent.id)).group_by(SearchEvent.problem)).all()
    demand_problem = [{"category": c, "demand_count": cnt} for c, cnt in demand_rows]

    demand_city_rows = db.execute(select(SearchEvent.city, func.count(SearchEvent.id)).group_by(SearchEvent.city)).all()
    demand_city = [{"city": city, "demand_count": count} for city, count in demand_city_rows]

    return AnalyticsResponse(
        average_fee_per_city=avg_fee,
        fastest_ambulance_per_city=fastest,
        most_experienced_doctor_per_city=experienced,
        demand_category_analysis=demand_problem,
        demand_by_city=demand_city,
    )


@router.get("/analytics/forecast", response_model=AnalyticsForecastResponse)
def get_forecast(db: Session = Depends(get_db)):
    data = forecast(db)
    return AnalyticsForecastResponse(**data)
