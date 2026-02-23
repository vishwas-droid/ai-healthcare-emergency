from __future__ import annotations

from collections.abc import Iterable

from app.db.models import Ambulance, Doctor


PROBLEM_TO_CATEGORY = {
    "heart": ["Cardiologist"],
    "chest pain": ["Cardiologist", "General Physician"],
    "brain": ["Neurologist"],
    "stroke": ["Neurologist"],
    "child": ["Pediatrician"],
    "fever": ["General Physician"],
    "injury": ["Orthopedic"],
}


def _norm(value: float, min_v: float, max_v: float, reverse: bool = False) -> float:
    if max_v == min_v:
        return 1.0
    raw = (value - min_v) / (max_v - min_v)
    return 1 - raw if reverse else raw


def _range(items: Iterable[float]) -> tuple[float, float]:
    vals = list(items)
    if not vals:
        return 0.0, 1.0
    return float(min(vals)), float(max(vals))


def _specialization_boost(problem: str, category: str) -> float:
    p = problem.strip().lower()
    cat = category.strip().lower()
    for keyword, categories in PROBLEM_TO_CATEGORY.items():
        if keyword in p and any(cat == c.lower() for c in categories):
            return 0.08
    return 0.0


def score_doctors(doctors: list[Doctor]) -> list[Doctor]:
    r_min, r_max = _range(d.rating for d in doctors)
    e_min, e_max = _range(d.experience_years for d in doctors)
    rt_min, rt_max = _range(d.response_time_minutes for d in doctors)
    f_min, f_max = _range(d.consultation_fee for d in doctors)
    rev_min, rev_max = _range(d.reviews_count for d in doctors)
    p_min, p_max = _range(d.total_patients_served for d in doctors)

    for d in doctors:
        score = (
            0.30 * _norm(d.rating, r_min, r_max)
            + 0.20 * _norm(d.experience_years, e_min, e_max)
            + 0.15 * _norm(d.response_time_minutes, rt_min, rt_max, reverse=True)
            + 0.15 * _norm(d.consultation_fee, f_min, f_max, reverse=True)
            + 0.10 * _norm(d.reviews_count, rev_min, rev_max)
            + 0.05 * _norm(d.total_patients_served, p_min, p_max)
            + 0.05 * (1.0 if d.verified_status else 0.0)
        ) * 100
        d.ai_score = round(score, 2)

    return sorted(doctors, key=lambda x: x.ai_score, reverse=True)


def score_ambulances(ambulances: list[Ambulance]) -> list[Ambulance]:
    rt_min, rt_max = _range(a.response_time_minutes for a in ambulances)
    r_min, r_max = _range(a.rating for a in ambulances)
    c_min, c_max = _range(a.cost_per_km for a in ambulances)
    b_min, b_max = _range(a.base_price for a in ambulances)

    for a in ambulances:
        affordability = 0.6 * _norm(a.cost_per_km, c_min, c_max, reverse=True) + 0.4 * _norm(
            a.base_price, b_min, b_max, reverse=True
        )
        score = (
            0.35 * _norm(a.response_time_minutes, rt_min, rt_max, reverse=True)
            + 0.25 * _norm(a.rating, r_min, r_max)
            + 0.20 * affordability
            + 0.10 * (1.0 if a.availability_status in {"AVAILABLE", "ON_CALL"} else 0.0)
            + 0.10 * (1.0 if a.verified_status else 0.0)
        ) * 100
        a.ai_score = round(score, 2)

    return sorted(ambulances, key=lambda x: x.ai_score, reverse=True)


def score_doctors_contextual(doctors: list[Doctor], city: str, problem: str, budget: float) -> list[Doctor]:
    ranked = score_doctors(doctors)
    city_lower = city.strip().lower()
    for d in ranked:
        context_boost = 0.0
        if d.city.strip().lower() == city_lower:
            context_boost += 0.07
        context_boost += _specialization_boost(problem, d.category)
        if d.consultation_fee <= budget:
            context_boost += 0.05
        d.ai_score = round(min(100.0, d.ai_score + context_boost * 100), 2)
    return sorted(ranked, key=lambda x: x.ai_score, reverse=True)


def score_ambulances_contextual(
    ambulances: list[Ambulance], city: str, budget: float, urgency: str = "high"
) -> list[Ambulance]:
    ranked = score_ambulances(ambulances)
    city_lower = city.strip().lower()
    urgency_boost = 0.04 if urgency.lower() in {"critical", "high"} else 0.02

    for a in ranked:
        context_boost = 0.0
        if a.city.strip().lower() == city_lower:
            context_boost += 0.08
        if a.base_price <= budget:
            context_boost += 0.05
        if a.vehicle_type in {"ICU", "ALS", "Ventilator"}:
            context_boost += urgency_boost
        a.ai_score = round(min(100.0, a.ai_score + context_boost * 100), 2)

    return sorted(ranked, key=lambda x: x.ai_score, reverse=True)
