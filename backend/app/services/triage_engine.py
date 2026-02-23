from __future__ import annotations

import re
from typing import Dict, List

import httpx

from app.core.config import settings

HIGH_RISK_PHRASES = [
    "chest pain",
    "shortness of breath",
    "loss of consciousness",
    "severe bleeding",
    "stroke symptoms",
    "not breathing",
    "seizure",
    "cyanosis",
    "slurred speech",
    "left arm weakness",
    "severe headache",
]

EMERGENCY_TYPE_KEYWORDS = {
    "Cardiac": ["chest pain", "heart", "palpitations", "cardiac"],
    "Neuro": ["stroke", "seizure", "slurred speech", "weakness", "numbness"],
    "Trauma": ["accident", "bleeding", "fracture", "injury", "trauma"],
    "Respiratory": ["breath", "wheezing", "asthma", "respiratory", "oxygen"],
    "Toxicology": ["poison", "overdose", "toxic", "chemical"],
    "ObGyn": ["pregnant", "pregnancy", "labor", "bleeding"],
    "Psych": ["self harm", "suicidal", "panic", "psych"],
}

SPECIALTY_MAP = {
    "Cardiac": "Cardiologist",
    "Neuro": "Neurologist",
    "Trauma": "Orthopedic",
    "Respiratory": "Pulmonologist",
    "Toxicology": "General Physician",
    "ObGyn": "Gynecologist",
    "Psych": "Psychiatrist",
    "Other": "General Physician",
}

HOSPITAL_TYPE_MAP = {
    "Cardiac": "Cardiac",
    "Neuro": "Neuro",
    "Trauma": "Trauma",
    "Respiratory": "Respiratory",
    "Toxicology": "General",
    "ObGyn": "General",
    "Psych": "General",
    "Other": "General",
}


def _find_risk_flags(text: str) -> List[str]:
    flags = []
    lowered = text.lower()
    for phrase in HIGH_RISK_PHRASES:
        if phrase in lowered:
            flags.append(phrase)
    return flags


def _detect_emergency_type(text: str) -> str:
    lowered = text.lower()
    for emergency_type, keywords in EMERGENCY_TYPE_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return emergency_type
    return "Other"


def _extract_entities(text: str) -> Dict:
    lowered = text.lower()
    symptoms = [s.strip() for s in re.split(r"[,;]", lowered) if s.strip()]
    duration_match = re.search(r"(\d+)\s*(minutes|minute|hours|hour|days|day|weeks|week)", lowered)
    duration = duration_match.group(0) if duration_match else "unknown"

    vitals = {
        "bp": None,
        "hr": None,
        "spo2": None,
    }
    bp_match = re.search(r"(\d{2,3})\s*/\s*(\d{2,3})", lowered)
    if bp_match:
        vitals["bp"] = f"{bp_match.group(1)}/{bp_match.group(2)}"

    hr_match = re.search(r"hr\s*(\d{2,3})", lowered)
    if hr_match:
        vitals["hr"] = hr_match.group(1)

    spo2_match = re.search(r"spo2\s*(\d{2,3})", lowered)
    if spo2_match:
        vitals["spo2"] = spo2_match.group(1)

    risk_factors = [rf for rf in ["diabetes", "hypertension", "smoker", "obese"] if rf in lowered]
    medications = [med for med in ["aspirin", "insulin", "metformin", "statin"] if med in lowered]

    return {
        "symptoms": symptoms[:8],
        "duration": duration,
        "vitals": vitals,
        "risk_factors": risk_factors,
        "medications": medications,
    }


def _severity_from_text(text: str, risk_flags: List[str]) -> tuple[str, int]:
    lowered = text.lower()
    score = 20
    if any(word in lowered for word in ["severe", "unconscious", "bleeding", "breathing", "stroke", "heart"]):
        score += 35
    if any(word in lowered for word in ["sudden", "intense", "unbearable", "collapse"]):
        score += 20
    if risk_flags:
        score += 30
    score = min(100, score)
    if score >= 85:
        return "CRITICAL", score
    if score >= 65:
        return "HIGH", score
    if score >= 40:
        return "MODERATE", score
    return "LOW", score


def _recommendations(emergency_type: str, severity: str) -> Dict:
    return {
        "doctor_specialty": SPECIALTY_MAP.get(emergency_type, "General Physician"),
        "ambulance_priority": "CRITICAL" if severity == "CRITICAL" else "HIGH" if severity == "HIGH" else "NORMAL",
        "hospital_type": HOSPITAL_TYPE_MAP.get(emergency_type, "General"),
    }


def _call_llm_service(text: str) -> Dict | None:
    if not settings.ai_service_url or not settings.enable_llm_triage:
        return None
    try:
        with httpx.Client(timeout=8.0) as client:
            res = client.post(f"{settings.ai_service_url}/triage", json={"complaint_text": text})
            res.raise_for_status()
            return res.json()
    except Exception:
        return None


def triage(text: str) -> Dict:
    llm = _call_llm_service(text)
    if llm:
        return llm

    risk_flags = _find_risk_flags(text)
    emergency_type = _detect_emergency_type(text)
    severity, score = _severity_from_text(text, risk_flags)
    entities = _extract_entities(text)
    recommended = _recommendations(emergency_type, severity)

    escalation = {
        "triggered": bool(risk_flags) or severity in {"HIGH", "CRITICAL"},
        "reason": ", ".join(risk_flags) if risk_flags else "Severity threshold",
    }

    confidence = 0.72 if risk_flags else 0.62

    return {
        "severity": severity,
        "severity_score": score,
        "emergency_type": emergency_type,
        "entities": entities,
        "recommended": recommended,
        "risk_flags": risk_flags,
        "escalation": escalation,
        "confidence": confidence,
    }
