from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import ChatMessage, ChatSession, Doctor
from app.db.schemas import (
    ChatMessageCreate,
    ChatMessageOut,
    ChatSessionCreate,
    ChatSessionOut,
)
from app.db.session import get_db

router = APIRouter(prefix="", tags=["Chat"])


class ConnectionManager:
    def __init__(self):
        self.active: dict[int, list[WebSocket]] = {}

    async def connect(self, session_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active.setdefault(session_id, []).append(websocket)

    def disconnect(self, session_id: int, websocket: WebSocket):
        if session_id in self.active and websocket in self.active[session_id]:
            self.active[session_id].remove(websocket)

    async def broadcast(self, session_id: int, payload: dict):
        for ws in self.active.get(session_id, []):
            await ws.send_json(payload)


manager = ConnectionManager()


@router.post("/chat/session", response_model=ChatSessionOut)
def create_chat_session(payload: ChatSessionCreate, db: Session = Depends(get_db)):
    doctor = db.get(Doctor, payload.doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    session = ChatSession(doctor_id=payload.doctor_id, user_name=payload.user_name)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.get("/chat/{session_id}/messages", response_model=list[ChatMessageOut])
def get_chat_messages(session_id: int, db: Session = Depends(get_db)):
    chat = db.get(ChatSession, session_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Session not found")
    return db.scalars(select(ChatMessage).where(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at)).all()


@router.post("/chat/{session_id}/message", response_model=ChatMessageOut)
def send_message(session_id: int, payload: ChatMessageCreate, db: Session = Depends(get_db)):
    chat = db.get(ChatSession, session_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Session not found")

    msg = ChatMessage(
        session_id=session_id,
        sender_type=payload.sender_type,
        message=payload.message,
        file_url=payload.file_url,
    )
    chat.last_message_at = datetime.utcnow()

    # Simulate dynamic response time improvements when doctor replies
    doctor = db.get(Doctor, chat.doctor_id)
    if payload.sender_type.upper() == "DOCTOR" and doctor:
        doctor.response_time_minutes = max(1, doctor.response_time_minutes - 1)
        db.add(doctor)

    db.add(chat)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


@router.websocket("/chat/ws/{session_id}")
async def chat_socket(websocket: WebSocket, session_id: int):
    await manager.connect(session_id, websocket)
    try:
        while True:
            raw = await websocket.receive_json()
            await manager.broadcast(
                session_id,
                {
                    "session_id": session_id,
                    "sender_type": raw.get("sender_type", "USER"),
                    "message": raw.get("message", ""),
                    "created_at": datetime.utcnow().isoformat(),
                },
            )
    except WebSocketDisconnect:
        manager.disconnect(session_id, websocket)
