from __future__ import annotations

from typing import Tuple

import httpx

from app.core.config import settings
from app.services.scoring_engine import haversine_km


def _fallback_eta_seconds(km: float) -> int:
    avg_speed_kmh = 32.0
    return max(240, int((km / max(avg_speed_kmh, 1.0)) * 3600))


def estimate_eta_seconds(origin: Tuple[float, float], dest: Tuple[float, float]) -> int:
    km = haversine_km(origin[0], origin[1], dest[0], dest[1])
    if not settings.google_maps_api_key:
        return _fallback_eta_seconds(km)

    try:
        url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            "origin": f"{origin[0]},{origin[1]}",
            "destination": f"{dest[0]},{dest[1]}",
            "key": settings.google_maps_api_key,
        }
        with httpx.Client(timeout=5.0) as client:
            res = client.get(url, params=params)
            res.raise_for_status()
            data = res.json()
        routes = data.get("routes") or []
        if not routes:
            return _fallback_eta_seconds(km)
        legs = routes[0].get("legs") or []
        if not legs:
            return _fallback_eta_seconds(km)
        duration = legs[0].get("duration", {}).get("value")
        if duration:
            return int(duration)
    except Exception:
        return _fallback_eta_seconds(km)

    return _fallback_eta_seconds(km)
