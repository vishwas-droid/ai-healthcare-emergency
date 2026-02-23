from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import (
    admin,
    ambulances,
    analytics,
    auth,
    bookings,
    chat,
    compare,
    dispatch,
    doctors,
    feedback,
    hospitals,
    meta,
    ranking,
    recommendation,
    tracking,
    triage,
)
from app.core.config import settings
from app.db.models import Base
from app.db.seed import seed_if_empty
from app.db.session import SessionLocal, engine

Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    seed_if_empty(db)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def healthcheck():
    return {"status": "ok", "service": settings.app_name}


app.include_router(doctors.router)
app.include_router(ambulances.router)
app.include_router(compare.router)
app.include_router(analytics.router)
app.include_router(chat.router)
app.include_router(recommendation.router)
app.include_router(tracking.router)
app.include_router(meta.router)
app.include_router(bookings.router)
app.include_router(triage.router)
app.include_router(ranking.router)
app.include_router(dispatch.router)
app.include_router(hospitals.router)
app.include_router(feedback.router)
app.include_router(auth.router)
app.include_router(admin.router)
