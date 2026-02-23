from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Ambulance, Doctor


DOCTOR_SEED = [
    Doctor(name="Dr. Aditi Sharma", photo_url="https://i.pravatar.cc/150?img=1", category="Cardiologist", city="Mumbai", state="Maharashtra", qualification="MBBS, MD, DM", college="AIIMS", experience_years=14, rating=4.8, reviews_count=420, consultation_fee=1200, total_patients_served=7600, response_time_minutes=6, verified_status=True, availability_status="Online", languages="English,Hindi", whatsapp_link="https://wa.me/919999000001", phone_number="+91-9999000001"),
    Doctor(name="Dr. Neha Rao", photo_url="https://i.pravatar.cc/150?img=47", category="Pediatrician", city="Mumbai", state="Maharashtra", qualification="MBBS, MD", college="AIIMS", experience_years=12, rating=4.9, reviews_count=510, consultation_fee=950, total_patients_served=8400, response_time_minutes=4, verified_status=True, availability_status="Online", languages="English,Hindi,Marathi", whatsapp_link="https://wa.me/919999000004", phone_number="+91-9999000004"),
    Doctor(name="Dr. Rohit Mehta", photo_url="https://i.pravatar.cc/150?img=11", category="Neurologist", city="Delhi", state="Delhi", qualification="MBBS, MD, DM", college="PGIMER", experience_years=11, rating=4.6, reviews_count=320, consultation_fee=1400, total_patients_served=5200, response_time_minutes=9, verified_status=True, availability_status="Clinic", languages="English,Hindi", whatsapp_link="https://wa.me/919999000002", phone_number="+91-9999000002"),
    Doctor(name="Dr. Sahil Arora", photo_url="https://i.pravatar.cc/150?img=12", category="Orthopedic", city="Delhi", state="Delhi", qualification="MBBS, MS", college="MAMC", experience_years=10, rating=4.5, reviews_count=270, consultation_fee=1100, total_patients_served=4700, response_time_minutes=11, verified_status=False, availability_status="Clinic", languages="English,Hindi", whatsapp_link="https://wa.me/919999000005", phone_number="+91-9999000005"),
    Doctor(name="Dr. Kavya Iyer", photo_url="https://i.pravatar.cc/150?img=32", category="General Physician", city="Bengaluru", state="Karnataka", qualification="MBBS, MD", college="CMC", experience_years=9, rating=4.7, reviews_count=220, consultation_fee=700, total_patients_served=4300, response_time_minutes=5, verified_status=False, availability_status="24x7", languages="English,Hindi,Tamil", whatsapp_link="https://wa.me/919999000003", phone_number="+91-9999000003"),
    Doctor(name="Dr. Priya Nair", photo_url="https://i.pravatar.cc/150?img=33", category="Cardiologist", city="Bengaluru", state="Karnataka", qualification="MBBS, MD, DM", college="NIMHANS", experience_years=13, rating=4.8, reviews_count=390, consultation_fee=1300, total_patients_served=6500, response_time_minutes=7, verified_status=True, availability_status="Online", languages="English,Kannada,Hindi", whatsapp_link="https://wa.me/919999000006", phone_number="+91-9999000006"),
    Doctor(name="Dr. Arjun Sen", photo_url="https://i.pravatar.cc/150?img=36", category="General Physician", city="Kolkata", state="West Bengal", qualification="MBBS, MD", college="IPGMER", experience_years=8, rating=4.4, reviews_count=180, consultation_fee=650, total_patients_served=3100, response_time_minutes=8, verified_status=False, availability_status="24x7", languages="English,Bengali,Hindi", whatsapp_link="https://wa.me/919999000007", phone_number="+91-9999000007"),
]

AMBULANCE_SEED = [
    Ambulance(provider_name="LifeLine ICU Ambulance", city="Mumbai", state="Maharashtra", vehicle_type="ICU", response_time_minutes=8, cost_per_km=35, base_price=1200, availability_status="AVAILABLE", rating=4.9, verified_status=True, total_cases_handled=9800, equipment_list="Oxygen Cylinder,Ventilator,Cardiac Monitor,Defibrillator,Suction Machine,Infusion Pump,Trained Paramedic,GPS Tracking", phone_number="+91-9888800001", whatsapp_link="https://wa.me/919888800001"),
    Ambulance(provider_name="NeoCare Neonatal Ambulance", city="Mumbai", state="Maharashtra", vehicle_type="Neonatal", response_time_minutes=9, cost_per_km=38, base_price=1400, availability_status="AVAILABLE", rating=4.8, verified_status=True, total_cases_handled=2500, equipment_list="Oxygen Cylinder,Ventilator,Neonatal Support,Infusion Pump,Trained Paramedic,GPS Tracking", phone_number="+91-9888800004", whatsapp_link="https://wa.me/919888800004"),
    Ambulance(provider_name="Rapid ALS Care", city="Delhi", state="Delhi", vehicle_type="ALS", response_time_minutes=10, cost_per_km=28, base_price=900, availability_status="ON_CALL", rating=4.6, verified_status=True, total_cases_handled=6400, equipment_list="Oxygen Cylinder,Cardiac Monitor,Defibrillator,Trained Paramedic,GPS Tracking", phone_number="+91-9888800002", whatsapp_link="https://wa.me/919888800002"),
    Ambulance(provider_name="Metro Ventilator Response", city="Delhi", state="Delhi", vehicle_type="Ventilator", response_time_minutes=12, cost_per_km=32, base_price=1000, availability_status="AVAILABLE", rating=4.5, verified_status=True, total_cases_handled=4200, equipment_list="Oxygen Cylinder,Ventilator,Cardiac Monitor,Defibrillator,Trained Paramedic,GPS Tracking", phone_number="+91-9888800005", whatsapp_link="https://wa.me/919888800005"),
    Ambulance(provider_name="City BLS Emergency", city="Bengaluru", state="Karnataka", vehicle_type="BLS", response_time_minutes=12, cost_per_km=20, base_price=700, availability_status="AVAILABLE", rating=4.5, verified_status=False, total_cases_handled=7200, equipment_list="Oxygen Cylinder,Suction Machine,Trained Paramedic,GPS Tracking", phone_number="+91-9888800003", whatsapp_link="https://wa.me/919888800003"),
    Ambulance(provider_name="South ICU Rescue", city="Bengaluru", state="Karnataka", vehicle_type="ICU", response_time_minutes=11, cost_per_km=30, base_price=1100, availability_status="ON_CALL", rating=4.7, verified_status=True, total_cases_handled=5300, equipment_list="Oxygen Cylinder,Ventilator,Cardiac Monitor,Defibrillator,Suction Machine,Infusion Pump,Trained Paramedic,GPS Tracking", phone_number="+91-9888800006", whatsapp_link="https://wa.me/919888800006"),
]


def seed_if_empty(db: Session) -> None:
    doctor_exists = db.scalar(select(Doctor.id).limit(1))
    amb_exists = db.scalar(select(Ambulance.id).limit(1))
    if not doctor_exists:
        db.add_all(DOCTOR_SEED)
    if not amb_exists:
        db.add_all(AMBULANCE_SEED)
    db.commit()
