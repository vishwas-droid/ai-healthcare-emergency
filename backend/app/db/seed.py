import random
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.models import Ambulance, Doctor, Hospital, HospitalSpecialization, User


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

CITY_GEO = {
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.7041, 77.1025),
    "Bengaluru": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Chennai": (13.0827, 80.2707),
    "Pune": (18.5204, 73.8567),
    "Kolkata": (22.5726, 88.3639),
    "Ahmedabad": (23.0225, 72.5714),
    "Jaipur": (26.9124, 75.7873),
    "Lucknow": (26.8467, 80.9462),
    "Dubai": (25.2048, 55.2708),
    "Abu Dhabi": (24.4539, 54.3773),
    "London": (51.5074, -0.1278),
    "Manchester": (53.4808, -2.2426),
    "New York": (40.7128, -74.0060),
    "San Francisco": (37.7749, -122.4194),
    "Toronto": (43.6532, -79.3832),
    "Sydney": (-33.8688, 151.2093),
    "Singapore": (1.3521, 103.8198),
    "Kuala Lumpur": (3.1390, 101.6869),
}

AMBULANCE_TYPES = ["BLS", "ALS", "ICU", "Ventilator", "Neonatal"]
AMBULANCE_EQUIPMENT = {
    "BLS": "Oxygen Cylinder,Suction Machine,Trained Paramedic,GPS Tracking",
    "ALS": "Oxygen Cylinder,Cardiac Monitor,Defibrillator,Trained Paramedic,GPS Tracking",
    "ICU": "Oxygen Cylinder,Ventilator,Cardiac Monitor,Defibrillator,Suction Machine,Infusion Pump,Trained Paramedic,GPS Tracking",
    "Ventilator": "Oxygen Cylinder,Ventilator,Cardiac Monitor,Defibrillator,Trained Paramedic,GPS Tracking",
    "Neonatal": "Oxygen Cylinder,Ventilator,Neonatal Support,Infusion Pump,Trained Paramedic,GPS Tracking",
}

DOCTOR_SEED = [
    Doctor(
        name="Dr. Aditi Sharma",
        photo_url="https://i.pravatar.cc/150?img=1",
        category="Cardiologist",
        city="Mumbai",
        state="Maharashtra",
        country="India",
        qualification="MBBS, MD, DM",
        college="AIIMS",
        experience_years=14,
        rating=4.8,
        reviews_count=420,
        consultation_fee=1200,
        total_patients_served=7600,
        response_time_minutes=6,
        response_time_seconds=360,
        verified_status=True,
        availability_status="Online",
        is_available=True,
        languages="English,Hindi",
        whatsapp_link="https://wa.me/919999000001",
        phone_number="+91-9999000001",
        rating_count=420,
        success_rate=94.0,
        latitude=19.0812,
        longitude=72.8826,
    ),
    Doctor(
        name="Dr. Neha Rao",
        photo_url="https://i.pravatar.cc/150?img=47",
        category="Pediatrician",
        city="Mumbai",
        state="Maharashtra",
        country="India",
        qualification="MBBS, MD",
        college="AIIMS",
        experience_years=12,
        rating=4.9,
        reviews_count=510,
        consultation_fee=950,
        total_patients_served=8400,
        response_time_minutes=4,
        response_time_seconds=240,
        verified_status=True,
        availability_status="Online",
        is_available=True,
        languages="English,Hindi,Marathi",
        whatsapp_link="https://wa.me/919999000004",
        phone_number="+91-9999000004",
        rating_count=510,
        success_rate=96.0,
        latitude=19.0768,
        longitude=72.8770,
    ),
]

AMBULANCE_SEED = [
    Ambulance(
        provider_name="LifeLine ICU Ambulance",
        city="Mumbai",
        state="Maharashtra",
        vehicle_type="ICU",
        response_time_minutes=8,
        response_time_seconds=480,
        cost_per_km=35,
        base_price=1200,
        availability_status="AVAILABLE",
        rating=4.9,
        verified_status=True,
        total_cases_handled=9800,
        equipment_list=AMBULANCE_EQUIPMENT["ICU"],
        phone_number="+91-9888800001",
        whatsapp_link="https://wa.me/919888800001",
        driver_score=92.0,
        has_icu=True,
        has_oxygen=True,
        has_ventilator=True,
        is_available=True,
        latitude=19.0786,
        longitude=72.8754,
    ),
    Ambulance(
        provider_name="Rapid ALS Care",
        city="Delhi",
        state="Delhi",
        vehicle_type="ALS",
        response_time_minutes=10,
        response_time_seconds=600,
        cost_per_km=28,
        base_price=900,
        availability_status="ON_CALL",
        rating=4.6,
        verified_status=True,
        total_cases_handled=6400,
        equipment_list=AMBULANCE_EQUIPMENT["ALS"],
        phone_number="+91-9888800002",
        whatsapp_link="https://wa.me/919888800002",
        driver_score=88.0,
        has_icu=False,
        has_oxygen=True,
        has_ventilator=False,
        is_available=True,
        latitude=28.7062,
        longitude=77.1043,
    ),
]

HOSPITAL_SEED = [
    Hospital(
        name="Apex Heart & Trauma Center",
        city="Mumbai",
        state="Maharashtra",
        country="India",
        icu_beds_available=16,
        emergency_wait_minutes=12,
        success_rate=94.0,
        avg_cost_index=1.2,
        distance_km_estimate=4.2,
        latitude=19.0821,
        longitude=72.8821,
        phone_number="+91-9888800101",
        is_available=True,
    ),
    Hospital(
        name="Nova Neuro Institute",
        city="Delhi",
        state="Delhi",
        country="India",
        icu_beds_available=12,
        emergency_wait_minutes=18,
        success_rate=92.0,
        avg_cost_index=1.4,
        distance_km_estimate=5.1,
        latitude=28.7046,
        longitude=77.1020,
        phone_number="+91-9888800102",
        is_available=True,
    ),
    Hospital(
        name="RapidCare Trauma Hospital",
        city="Bengaluru",
        state="Karnataka",
        country="India",
        icu_beds_available=20,
        emergency_wait_minutes=14,
        success_rate=90.0,
        avg_cost_index=1.1,
        distance_km_estimate=3.8,
        latitude=12.9722,
        longitude=77.5940,
        phone_number="+91-9888800103",
        is_available=True,
    ),
]

HOSPITAL_SPECIALTIES = {
    "Apex Heart & Trauma Center": ["Cardiac", "Trauma", "General"],
    "Nova Neuro Institute": ["Neuro", "Respiratory"],
    "RapidCare Trauma Hospital": ["Trauma", "General", "Respiratory"],
}


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

    lat, lng = CITY_GEO.get(city, (19.0760, 72.8777))
    lat += rng.uniform(-0.08, 0.08)
    lng += rng.uniform(-0.08, 0.08)
    rating_count = reviews
    success_rate = round(min(98.0, 70 + rating * 6 + rng.uniform(-4, 4)), 1)

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
        response_time_seconds=response * 60,
        verified_status=verified,
        availability_status=availability,
        is_available=availability.lower() in {"online", "24x7"},
        languages=rng.choice(LANGUAGE_SETS),
        whatsapp_link=f"https://wa.me/{phone.replace('+', '')}",
        phone_number=phone,
        rating_count=rating_count,
        success_rate=success_rate,
        latitude=round(lat, 6),
        longitude=round(lng, 6),
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

    lat, lng = CITY_GEO.get(city, (19.0760, 72.8777))
    lat += rng.uniform(-0.1, 0.1)
    lng += rng.uniform(-0.1, 0.1)
    has_icu = vehicle_type in {"ICU"}
    has_ventilator = vehicle_type in {"ICU", "Ventilator", "Neonatal"}
    has_oxygen = True
    driver_score = round(min(98.0, 70 + rating * 6 + rng.uniform(-5, 5)), 1)

    return Ambulance(
        provider_name=f"{provider_prefix} {vehicle_type} Ambulance {idx}",
        city=city,
        state=state,
        vehicle_type=vehicle_type,
        response_time_minutes=response,
        response_time_seconds=response * 60,
        cost_per_km=cost_per_km,
        base_price=base,
        availability_status=status,
        rating=rating,
        verified_status=verified,
        total_cases_handled=cases,
        equipment_list=AMBULANCE_EQUIPMENT[vehicle_type],
        phone_number=phone,
        whatsapp_link=f"https://wa.me/{phone.replace('+', '')}",
        driver_score=driver_score,
        has_icu=has_icu,
        has_oxygen=has_oxygen,
        has_ventilator=has_ventilator,
        is_available=status in {"AVAILABLE", "ON_CALL"},
        latitude=round(lat, 6),
        longitude=round(lng, 6),
    )


def seed_if_empty(db: Session, min_doctors: int = 1500, min_ambulances: int = 1200, min_hospitals: int = 120) -> None:
    doctor_count = db.scalar(select(func.count(Doctor.id))) or 0
    amb_count = db.scalar(select(func.count(Ambulance.id))) or 0
    hospital_count = db.scalar(select(func.count(Hospital.id))) or 0
    user_count = db.scalar(select(func.count(User.id))) or 0

    if doctor_count == 0:
        db.add_all(DOCTOR_SEED)
    if amb_count == 0:
        db.add_all(AMBULANCE_SEED)
    if hospital_count == 0:
        db.add_all(HOSPITAL_SEED)
    if user_count == 0:
        db.add(
            User(
                role="ADMIN",
                full_name="System Admin",
                email="admin@medai.com",
                phone="+91-9000000000",
                password_hash=get_password_hash("admin123"),
            )
        )
    db.commit()

    doctor_count = db.scalar(select(func.count(Doctor.id))) or 0
    amb_count = db.scalar(select(func.count(Ambulance.id))) or 0
    hospital_count = db.scalar(select(func.count(Hospital.id))) or 0

    rng = random.Random(20260223)

    if doctor_count < min_doctors:
        to_add = min_doctors - doctor_count
        db.add_all([_doctor_random(doctor_count + i + 1, rng) for i in range(to_add)])

    if amb_count < min_ambulances:
        to_add = min_ambulances - amb_count
        db.add_all([_ambulance_random(amb_count + i + 1, rng) for i in range(to_add)])

    if hospital_count < min_hospitals:
        to_add = min_hospitals - hospital_count
        for i in range(to_add):
            city, state, country = rng.choice(CITY_POOL)
            lat, lng = CITY_GEO.get(city, (19.0760, 72.8777))
            lat += rng.uniform(-0.12, 0.12)
            lng += rng.uniform(-0.12, 0.12)
            hospital = Hospital(
                name=f"CityCare Emergency Hospital {hospital_count + i + 1}",
                city=city,
                state=state,
                country=country,
                icu_beds_available=rng.randint(4, 28),
                emergency_wait_minutes=rng.randint(6, 40),
                success_rate=round(rng.uniform(78.0, 97.0), 1),
                avg_cost_index=round(rng.uniform(0.8, 1.6), 2),
                distance_km_estimate=round(rng.uniform(1.2, 18.0), 1),
                latitude=round(lat, 6),
                longitude=round(lng, 6),
                phone_number=f"+91-988880{1000 + i:04d}",
                is_available=rng.random() > 0.1,
            )
            db.add(hospital)
        db.commit()

    hospitals = db.scalars(select(Hospital)).all()
    if hospitals:
        for hospital in hospitals:
            if hospital.name in HOSPITAL_SPECIALTIES:
                for spec in HOSPITAL_SPECIALTIES[hospital.name]:
                    exists = db.scalar(
                        select(func.count(HospitalSpecialization.hospital_id)).where(
                            HospitalSpecialization.hospital_id == hospital.id,
                            HospitalSpecialization.specialization == spec,
                        )
                    )
                    if not exists:
                        db.add(HospitalSpecialization(hospital_id=hospital.id, specialization=spec))

    db.commit()
