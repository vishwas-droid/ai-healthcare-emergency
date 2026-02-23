from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Ambulance
from app.db.schemas import AmbulanceOut
from app.db.session import get_db
from app.services.scoring_service import score_ambulances

router = APIRouter(prefix="", tags=["Ambulances"])


@router.get("/ambulances", response_model=list[AmbulanceOut])
def get_ambulances(
    city: str | None = Query(default=None),
    vehicle_type: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    stmt = select(Ambulance)
    if city:
        stmt = stmt.where(Ambulance.city.ilike(f"%{city}%"))
    if vehicle_type:
        stmt = stmt.where(Ambulance.vehicle_type.ilike(f"%{vehicle_type}%"))

    ambulances = db.scalars(stmt).all()
    ranked = score_ambulances(ambulances)
    for ambulance in ranked:
        db.add(ambulance)
    db.commit()
    return ranked


@router.get("/ambulance/{ambulance_id}", response_model=AmbulanceOut)
def get_ambulance(ambulance_id: int, db: Session = Depends(get_db)):
    ambulance = db.get(Ambulance, ambulance_id)
    if not ambulance:
        raise HTTPException(status_code=404, detail="Ambulance not found")
    return ambulance
