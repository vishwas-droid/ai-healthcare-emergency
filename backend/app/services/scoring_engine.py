from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple
import math

from app.db.models import Ambulance, Doctor, Hospital


@dataclass
class ScoringWeights:
    experience: float
    bayesian: float
    distance: float
    response: float
    availability: float
    emergency_match: float
    budget: float
    success: float


SEVERITY_WEIGHTS_DOCTOR: Dict[str, ScoringWeights] = {
    "LOW": ScoringWeights(0.10, 0.15, 0.10, 0.10, 0.20, 0.10, 0.20, 0.05),
    "MODERATE": ScoringWeights(0.12, 0.15, 0.12, 0.12, 0.15, 0.15, 0.10, 0.09),
    "HIGH": ScoringWeights(0.12, 0.18, 0.18, 0.15, 0.10, 0.18, 0.04, 0.05),
    "CRITICAL": ScoringWeights(0.10, 0.18, 0.22, 0.18, 0.08, 0.20, 0.01, 0.03),
}

SEVERITY_WEIGHTS_AMBULANCE: Dict[str, Dict[str, float]] = {
    "LOW": {"distance": 0.20, "response": 0.20, "availability": 0.20, "equipment": 0.10, "driver": 0.15, "cost": 0.15},
    "MODERATE": {"distance": 0.22, "response": 0.22, "availability": 0.18, "equipment": 0.14, "driver": 0.14, "cost": 0.10},
    "HIGH": {"distance": 0.25, "response": 0.25, "availability": 0.18, "equipment": 0.18, "driver": 0.10, "cost": 0.04},
    "CRITICAL": {"distance": 0.28, "response": 0.26, "availability": 0.16, "equipment": 0.22, "driver": 0.06, "cost": 0.02},
}

SEVERITY_WEIGHTS_HOSPITAL: Dict[str, Dict[str, float]] = {
    "LOW": {"icu": 0.15, "wait": 0.20, "success": 0.20, "distance": 0.20, "specialty": 0.10, "cost": 0.15},
    "MODERATE": {"icu": 0.18, "wait": 0.20, "success": 0.22, "distance": 0.18, "specialty": 0.12, "cost": 0.10},
    "HIGH": {"icu": 0.25, "wait": 0.18, "success": 0.22, "distance": 0.18, "specialty": 0.12, "cost": 0.05},
    "CRITICAL": {"icu": 0.30, "wait": 0.15, "success": 0.25, "distance": 0.18, "specialty": 0.10, "cost": 0.02},
}

EMERGENCY_SPECIALTY_MAP = {
    "Cardiac": ["Cardiologist"],
    "Neuro": ["Neurologist"],
    "Trauma": ["Orthopedic", "General Physician"],
    "Respiratory": ["Pulmonologist", "General Physician"],
    "Toxicology": ["General Physician"],
    "ObGyn": ["Gynecologist"],
    "Psych": ["Psychiatrist"],
    "Other": ["General Physician"],
}


def clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, value))


def _range(items: Iterable[float]) -> Tuple[float, float]:
    values = list(items)
    if not values:
        return 0.0, 1.0
    return float(min(values)), float(max(values))


def _norm(value: float, min_v: float, max_v: float, reverse: bool = False) -> float:
    if max_v == min_v:
        return 1.0
    raw = (value - min_v) / (max_v - min_v)
    return 1 - raw if reverse else raw


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    if lat1 == 0.0 and lon1 == 0.0:
        return 0.0
    if lat2 == 0.0 and lon2 == 0.0:
        return 0.0
    r = 6371.0
    p = math.pi / 180.0
    a = 0.5 - math.cos((lat2 - lat1) * p) / 2 + math.cos(lat1 * p) * math.cos(lat2 * p) * (1 - math.cos((lon2 - lon1) * p)) / 2
    return 2 * r * math.asin(math.sqrt(a))


def bayesian_rating(avg: float, count: int, m: int = 50, prior: float = 4.2) -> float:
    return (count / (count + m)) * avg + (m / (count + m)) * prior


def distance_score_km(km: float, max_km: float = 30.0) -> float:
    if km <= 0:
        return 60.0
    return clamp(100.0 * (1.0 - min(km, max_km) / max_km))


def response_time_score(seconds: int, target: int = 180) -> float:
    if seconds <= 0:
        return 60.0
    return clamp(100.0 * (target / max(seconds, 30)))


def availability_score(is_available: bool, status: str | None = None) -> float:
    if is_available:
        return 100.0
    if status and status.lower() in {"online", "available", "on_call", "24x7"}:
        return 80.0
    return 20.0


def budget_score(cost: float, budget: float) -> float:
    if budget <= 0:
        return 50.0
    ratio = budget / max(cost, 1.0)
    return clamp(100.0 * min(1.0, ratio))


def experience_score(years: int, max_years: int = 20) -> float:
    return clamp(100.0 * min(years, max_years) / max_years)


def emergency_match_score(emergency_type: str, category: str) -> float:
    desired = EMERGENCY_SPECIALTY_MAP.get(emergency_type, ["General Physician"])
    cat = category.strip().lower()
    return 95.0 if any(cat == d.lower() for d in desired) else 55.0


def equipment_score(ambulance: Ambulance) -> float:
    score = 50.0
    if ambulance.has_icu:
        score += 20.0
    if ambulance.has_ventilator:
        score += 20.0
    if ambulance.has_oxygen:
        score += 10.0
    return clamp(score)


def doctor_score(
    severity: str,
    doctor: Doctor,
    patient_loc: Tuple[float, float],
    budget: float,
    emergency_type: str,
) -> Dict:
    weights = SEVERITY_WEIGHTS_DOCTOR.get(severity, SEVERITY_WEIGHTS_DOCTOR["LOW"])
    km = haversine_km(patient_loc[0], patient_loc[1], doctor.latitude, doctor.longitude)

    components = {
        "experience": experience_score(doctor.experience_years),
        "bayesian": bayesian_rating(doctor.rating, doctor.rating_count or doctor.reviews_count) * 20.0,
        "distance": distance_score_km(km),
        "response": response_time_score(doctor.response_time_seconds or doctor.response_time_minutes * 60),
        "availability": availability_score(doctor.is_available, doctor.availability_status),
        "emergency_match": emergency_match_score(emergency_type, doctor.category),
        "budget": budget_score(doctor.consultation_fee, budget),
        "success": clamp(doctor.success_rate),
    }

    total = (
        components["experience"] * weights.experience
        + components["bayesian"] * weights.bayesian
        + components["distance"] * weights.distance
        + components["response"] * weights.response
        + components["availability"] * weights.availability
        + components["emergency_match"] * weights.emergency_match
        + components["budget"] * weights.budget
        + components["success"] * weights.success
    )

    return {
        "score_total": round(total, 2),
        "breakdown": {k: round(v, 2) for k, v in components.items()},
        "distance_km": round(km, 2),
    }


def ambulance_score(
    severity: str,
    ambulance: Ambulance,
    patient_loc: Tuple[float, float],
    budget: float,
) -> Dict:
    weights = SEVERITY_WEIGHTS_AMBULANCE.get(severity, SEVERITY_WEIGHTS_AMBULANCE["LOW"])
    km = haversine_km(patient_loc[0], patient_loc[1], ambulance.latitude, ambulance.longitude)

    response = response_time_score(ambulance.response_time_seconds or ambulance.response_time_minutes * 60)
    distance = distance_score_km(km)
    availability = availability_score(ambulance.is_available, ambulance.availability_status)
    equipment = equipment_score(ambulance)
    driver = clamp(ambulance.driver_score)
    cost = budget_score(ambulance.base_price + ambulance.cost_per_km * max(km, 3), budget)

    total = (
        distance * weights["distance"]
        + response * weights["response"]
        + availability * weights["availability"]
        + equipment * weights["equipment"]
        + driver * weights["driver"]
        + cost * weights["cost"]
    )

    return {
        "score_total": round(total, 2),
        "breakdown": {
            "distance": round(distance, 2),
            "response": round(response, 2),
            "availability": round(availability, 2),
            "equipment": round(equipment, 2),
            "driver": round(driver, 2),
            "cost": round(cost, 2),
        },
        "distance_km": round(km, 2),
    }


def hospital_score(
    severity: str,
    hospital: Hospital,
    patient_loc: Tuple[float, float],
    budget: float,
    emergency_type: str,
) -> Dict:
    weights = SEVERITY_WEIGHTS_HOSPITAL.get(severity, SEVERITY_WEIGHTS_HOSPITAL["LOW"])
    km = haversine_km(patient_loc[0], patient_loc[1], hospital.latitude, hospital.longitude)

    icu = clamp(hospital.icu_beds_available * 4)
    wait = clamp(100.0 - hospital.emergency_wait_minutes * 2)
    success = clamp(hospital.success_rate)
    distance = distance_score_km(km, max_km=40)
    cost = clamp(100.0 / max(hospital.avg_cost_index, 0.6))
    specialty = 60.0
    if hospital.specializations:
        specialty_names = {spec.specialization.lower() for spec in hospital.specializations}
        if emergency_type.lower() in specialty_names:
            specialty = 95.0
    total = (
        icu * weights["icu"]
        + wait * weights["wait"]
        + success * weights["success"]
        + distance * weights["distance"]
        + specialty * weights["specialty"]
        + cost * weights["cost"]
    )
    if not hospital.is_available:
        total *= 0.85

    return {
        "score_total": round(total, 2),
        "breakdown": {
            "icu": round(icu, 2),
            "wait": round(wait, 2),
            "success": round(success, 2),
            "distance": round(distance, 2),
            "specialty": round(specialty, 2),
            "cost": round(cost, 2),
        },
        "distance_km": round(km, 2),
    }


def explain_top_factor(breakdown: Dict[str, float]) -> str:
    top = max(breakdown.items(), key=lambda x: x[1])
    return f"Top factor was {top[0]} with score {top[1]}"
