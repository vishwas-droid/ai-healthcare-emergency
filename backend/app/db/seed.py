import random
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import Ambulance, Doctor


FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Arjun", "Riya", "Anaya", "Kiara", "Ishaan", "Meera", "Karan",
    "Neha", "Priya", "Rahul", "Sanya", "Kabir", "Aditi", "Rohan", "Nisha", "Maya", "Ritika",
]
LAST_NAMES = [
    "Sharma", "Mehta", "Rao", "Iyer", "Singh", "Patel", "Nair", "Khan", "Arora", "Sen",
    "Gupta", "Jain", "Kapoor", "Malhotra", "Das", "Bose", "Yadav", "Roy", "Menon", "Verma",
]
SPECIALTIES = [
    "Cardiologist", "Neurologist", "Pediatrician", "General Physician", "Orthopedic", "Dermatologist",
    "Psychiatrist", "Oncologist", "Pulmonologist", "Gynecologist",
]
QUALIFICATIONS = [
    "MBBS, MD", "MBBS, MD, DM", "MBBS, MS", "MBBS, DNB", "MBBS, MD, MRCP",
]
COLLEGES = [
    "AIIMS", "CMC", "PGIMER", "MAMC", "NIMHANS", "KEM", "JIPMER", "King George Medical University",
]
LANGUAGE_SETS = [
    "English,Hindi", "English,Hindi,Marathi", "English,Hindi,Tamil", "English,Bengali,Hindi",
    "English,Hindi,Kannada", "English,Hindi,Telugu", "English,Spanish", "English,Arabic",
]

CITY_POOL = [
    ("Mumbai", "Maharashtra", "India"),
    ("Delhi", "Delhi", "India"),
    ("Bengaluru", "Karnataka", "India"),
    ("Hyderabad", "Telangana", "India"),
    ("Chennai", "Tamil Nadu", "India"),
    ("Pune", "Maharashtra", "India"),
    ("Kolkata", "West Bengal", "India"),
    ("Ahmedabad", "Gujarat", "India"),
    ("Jaipur", "Rajasthan", "India"),
    ("Lucknow", "Uttar Pradesh", "India"),
    ("Dubai", "Dubai", "UAE"),
    ("Abu Dhabi", "Abu Dhabi", "UAE"),
    ("London", "England", "UK"),
    ("Manchester", "England", "UK"),
    ("New York", "New York", "USA"),
    ("San Francisco", "California", "USA"),
    ("Toronto", "Ontario", "Canada"),
    ("Sydney", "NSW", "Australia"),
    ("Singapore", "Central", "Singapore"),
    ("Kuala Lumpur", "Kuala Lumpur", "Malaysia"),
]

AMBULANCE_TYPES = ["BLS", "ALS", "ICU", "Ventilator", "Neonatal"]
AMBULANCE_EQUIPMENT = {
    "BLS": "Oxygen Cylinder,Suction Machine,Trained Paramedic,GPS Tracking",
    "ALS": "Oxygen Cylinder,Cardiac Monitor,Defibrillator,Trained Paramedic,GPS Tracking",
    "ICU": "Oxygen Cylinder,Ventilator,Cardiac Monitor,Defibrillator,Suction Machine,Infusion Pump,Trained Paramedic,GPS Tracking",
    "Ventilator": "Oxygen Cylinder,Ventilator,Cardiac Monitor,Defibrillator,Trained Paramedic,GPS Tracking",
    "Neonatal": "Oxygen Cylinder,Ventilator,Neonatal Support,Infusion Pump,Trained Paramedic,GPS Tracking",
}


DOCTOR_SEED = [
    Doctor(name="Dr. Aditi Sharma", photo_url="https://i.pravatar.cc/150?img=1", category="Cardiologist", city="Mumbai", state="Maharashtra", country="India", qualification="MBBS, MD, DM", college="AIIMS", experience_years=14, rating=4.8, reviews_count=420, consultation_fee=1200, total_patients_served=7600, response_time_minutes=6, verified_status=True, availability_status="Online", languages="English,Hindi", whatsapp_link="https://wa.me/919999000001", phone_number="+91-9999000001"),
    Doctor(name="Dr. Neha Rao", photo_url="https://i.pravatar.cc/150?img=47", category="Pediatrician", city="Mumbai", state="Maharashtra", country="India", qualification="MBBS, MD", college="AIIMS", experience_years=12, rating=4.9, reviews_count=510, consultation_fee=950, total_patients_served=8400, response_time_minutes=4, verified_status=True, availability_status="Online", languages="English,Hindi,Marathi", whatsapp_link="https://wa.me/919999000004", phone_number="+91-9999000004"),
]

AMBULANCE_SEED = [
    Ambulance(provider_name="LifeLine ICU Ambulance", city="Mumbai", state="Maharashtra", vehicle_type="ICU", response_time_minutes=8, cost_per_km=35, base_price=1200, availability_status="AVAILABLE", rating=4.9, verified_status=True, total_cases_handled=9800, equipment_list=AMBULANCE_EQUIPMENT["ICU"], phone_number="+91-9888800001", whatsapp_link="https://wa.me/919888800001"),
    Ambulance(provider_name="Rapid ALS Care", city="Delhi", state="Delhi", vehicle_type="ALS", response_time_minutes=10, cost_per_km=28, base_price=900, availability_status="ON_CALL", rating=4.6, verified_status=True, total_cases_handled=6400, equipment_list=AMBULANCE_EQUIPMENT["ALS"], phone_number="+91-9888800002", whatsapp_link="https://wa.me/919888800002"),
]


def _doctor_random(idx: int, rng: random.Random) -> Doctor:
    first = rng.choice(FIRST_NAMES)
    last = rng.choice(LAST_NAMES)
    city, state, country = rng.choice(CITY_POOL)
    spec = rng.choice(SPECIALTIES)
    rating = round(rng.uniform(3.3, 5.0), 1)
    fee = round(rng.uniform(800, 5000), 0)
    exp = rng.randint(2, 35)
    reviews = rng.randint(20, 5000)
    patients = rng.randint(500, 50000)
    response = rng.randint(2, 30)
    verified = rng.random() > 0.35
    availability = rng.choice(["Online", "Clinic", "24x7"])
    phone = f"+91-9{idx:09d}"[-13:]

    return Doctor(
        name=f"Dr. {first} {last}",
        photo_url=f"https://i.pravatar.cc/150?img={(idx % 70) + 1}",
        category=spec,
        city=city,
        state=state,
        country=country,
        qualification=rng.choice(QUALIFICATIONS),
        college=rng.choice(COLLEGES),
        experience_years=exp,
        rating=rating,
        reviews_count=reviews,
        consultation_fee=fee,
        total_patients_served=patients,
        response_time_minutes=response,
        verified_status=verified,
        availability_status=availability,
        languages=rng.choice(LANGUAGE_SETS),
        whatsapp_link=f"https://wa.me/{phone.replace('+', '')}",
        phone_number=phone,
    )


def _ambulance_random(idx: int, rng: random.Random) -> Ambulance:
    city, state, _country = rng.choice(CITY_POOL)
    vehicle_type = rng.choice(AMBULANCE_TYPES)
    response = rng.randint(4, 35)
    cost_per_km = round(rng.uniform(12, 80), 1)
    base = round(rng.uniform(500, 8000), 0)
    rating = round(rng.uniform(3.2, 5.0), 1)
    cases = rng.randint(200, 60000)
    verified = rng.random() > 0.4
    status = rng.choice(["AVAILABLE", "ON_CALL", "BUSY"])
    provider_prefix = rng.choice(["LifeLine", "Rapid", "City", "Prime", "CarePlus", "MediFleet", "RescueOne"])
    phone = f"+91-8{idx:09d}"[-13:]

    return Ambulance(
        provider_name=f"{provider_prefix} {vehicle_type} Ambulance {idx}",
        city=city,
        state=state,
        vehicle_type=vehicle_type,
        response_time_minutes=response,
        cost_per_km=cost_per_km,
        base_price=base,
        availability_status=status,
        rating=rating,
        verified_status=verified,
        total_cases_handled=cases,
        equipment_list=AMBULANCE_EQUIPMENT[vehicle_type],
        phone_number=phone,
        whatsapp_link=f"https://wa.me/{phone.replace('+', '')}",
    )


def seed_if_empty(db: Session, min_doctors: int = 1500, min_ambulances: int = 1200) -> None:
    doctor_count = db.scalar(select(func.count(Doctor.id))) or 0
    amb_count = db.scalar(select(func.count(Ambulance.id))) or 0

    if doctor_count == 0:
        db.add_all(DOCTOR_SEED)
    if amb_count == 0:
        db.add_all(AMBULANCE_SEED)
    db.commit()

    doctor_count = db.scalar(select(func.count(Doctor.id))) or 0
    amb_count = db.scalar(select(func.count(Ambulance.id))) or 0

    rng = random.Random(20260223)

    if doctor_count < min_doctors:
        to_add = min_doctors - doctor_count
        db.add_all([_doctor_random(doctor_count + i + 1, rng) for i in range(to_add)])

    if amb_count < min_ambulances:
        to_add = min_ambulances - amb_count
        db.add_all([_ambulance_random(amb_count + i + 1, rng) for i in range(to_add)])

    db.commit()
