from __future__ import annotations

from typing import Dict, List
from fastapi import WebSocket


class TrackingConnectionManager:
    def __init__(self) -> None:
        self.active: Dict[int, List[WebSocket]] = {}

    async def connect(self, tracking_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active.setdefault(tracking_id, []).append(websocket)

    def disconnect(self, tracking_id: int, websocket: WebSocket) -> None:
        if tracking_id in self.active and websocket in self.active[tracking_id]:
            self.active[tracking_id].remove(websocket)

    async def broadcast(self, tracking_id: int, payload: dict) -> None:
        for ws in self.active.get(tracking_id, []):
            await ws.send_json(payload)
