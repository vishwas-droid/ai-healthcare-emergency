from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_current_user, get_password_hash, verify_password
from app.db.models import User
from app.db.schemas import AuthLoginRequest, AuthRegisterRequest, AuthResponse, UserOut
from app.db.session import get_db

router = APIRouter(prefix="", tags=["Auth"])


@router.post("/auth/register", response_model=AuthResponse)
def register(payload: AuthRegisterRequest, db: Session = Depends(get_db)):
    existing = db.scalar(select(User).where(User.email == payload.email))
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    role = payload.role.upper()
    if role not in {"ADMIN", "DOCTOR", "HOSPITAL", "AMBULANCE", "PATIENT"}:
        raise HTTPException(status_code=400, detail="Invalid role")

    user = User(
        role=role,
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone or "",
        password_hash=get_password_hash(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.id, "role": user.role})
    return AuthResponse(access_token=token, user=user)


@router.post("/auth/login", response_model=AuthResponse)
def login(payload: AuthLoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": user.id, "role": user.role})
    return AuthResponse(access_token=token, user=user)


@router.get("/auth/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
