from app.db.models import Ambulance, Doctor


def doctor_recommendation(doctor: Doctor, category: str | None = None) -> str:
    cat_text = f" {category}" if category else ""
    return (
        f"Based on affordability, {doctor.experience_years} years of experience, and "
        f"{doctor.response_time_minutes}-minute response time, {doctor.name} is the most optimal"
        f"{cat_text} specialist in {doctor.city}."
    )


def ambulance_recommendation(ambulance: Ambulance, budget: float | None = None) -> str:
    budget_text = " within your budget" if budget is not None else ""
    return (
        f"{ambulance.provider_name} offers a fast {ambulance.response_time_minutes}-minute response and "
        f"critical-care equipment{budget_text} in {ambulance.city}."
    )


def final_recommendation(doctor: Doctor | None, ambulance: Ambulance | None, problem: str, budget: float) -> str:
    if doctor and ambulance:
        return (
            f"For {problem}, choose {doctor.name} for specialist care and {ambulance.provider_name} "
            f"for transport. This combination balances speed, quality, and budget around INR {budget:.0f}."
        )
    if doctor:
        return f"For {problem}, {doctor.name} is your best doctor choice within INR {budget:.0f}."
    if ambulance:
        return f"For {problem}, {ambulance.provider_name} is your best ambulance choice within INR {budget:.0f}."
    return "No providers found for the selected criteria."
