"""Combine geocode + weather for a branch city."""
from __future__ import annotations

import logging

from .. import models
from .nominatim import geocode_city
from .open_meteo import current_weather

log = logging.getLogger("insurance.external")


def weather_for_branch(branch: models.Branch) -> dict:
    coords = geocode_city(branch.city)
    if not coords:
        return {"ok": False, "error": "geocode_failed", "city": branch.city}
    lat, lon = coords
    w = current_weather(lat, lon)
    return {
        "ok": True,
        "city": branch.city,
        "lat": lat,
        "lon": lon,
        "weather": w,
        "weather_live": not w.get("demo_fallback"),
    }
