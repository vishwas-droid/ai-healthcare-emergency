from __future__ import annotations

from typing import Dict, List

HIGH_RISK_PHRASES = [
    "chest pain",
    "shortness of breath",
    "loss of consciousness",
    "severe bleeding",
    "stroke symptoms",
    "not breathing",
    "seizure",
    "cyanosis",
]

EMERGENCY_TYPE_KEYWORDS = {
    "Cardiac": ["chest pain", "heart", "cardiac"],
    "Neuro": ["stroke", "seizure", "slurred speech", "weakness"],
    "Trauma": ["accident", "bleeding", "fracture", "injury"],
    "Respiratory": ["breath", "asthma", "respiratory", "oxygen"],
}

SPECIALTY_MAP = {
    "Cardiac": "Cardiologist",
    "Neuro": "Neurologist",
    "Trauma": "Orthopedic",
    "Respiratory": "Pulmonologist",
    "Other": "General Physician",
}

HOSPITAL_MAP = {
    "Cardiac": "Cardiac",
    "Neuro": "Neuro",
    "Trauma": "Trauma",
    "Respiratory": "Respiratory",
    "Other": "General",
}


def _risk_flags(text: str) -> List[str]:
    lowered = text.lower()
    return [phrase for phrase in HIGH_RISK_PHRASES if phrase in lowered]


def _emergency_type(text: str) -> str:
    lowered = text.lower()
    for key, keywords in EMERGENCY_TYPE_KEYWORDS.items():
        if any(k in lowered for k in keywords):
            return key
    return "Other"


def triage_llm(text: str) -> Dict:
    flags = _risk_flags(text)
    emergency_type = _emergency_type(text)
    severity = "CRITICAL" if flags else "HIGH" if "severe" in text.lower() else "MODERATE"
    score = 90 if flags else 70 if severity == "HIGH" else 50

    return {
        "severity": severity,
        "severity_score": score,
        "emergency_type": emergency_type,
        "entities": {
            "symptoms": [t.strip() for t in text.split(",")][:6],
            "duration": "unknown",
            "vitals": {"bp": None, "hr": None, "spo2": None},
            "risk_factors": [],
            "medications": [],
        },
        "recommended": {
            "doctor_specialty": SPECIALTY_MAP.get(emergency_type, "General Physician"),
            "ambulance_priority": "CRITICAL" if severity == "CRITICAL" else "HIGH",
            "hospital_type": HOSPITAL_MAP.get(emergency_type, "General"),
        },
        "risk_flags": flags,
        "escalation": {"triggered": bool(flags), "reason": ", ".join(flags) if flags else "Severity threshold"},
        "confidence": 0.78 if flags else 0.66,
    }
