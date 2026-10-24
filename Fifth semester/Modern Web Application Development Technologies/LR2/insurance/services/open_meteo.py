"""Open-Meteo current weather (free, no API key)."""
from __future__ import annotations

import logging

from .http import http_get_json

log = logging.getLogger("insurance.external")

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def current_weather(lat: float, lon: float) -> dict:
    params = (
        f"latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
        "&timezone=auto"
    )
    url = f"{OPEN_METEO_URL}?{params}"
    try:
        data = http_get_json(url, timeout=8.0)
    except Exception as exc:
        log.warning("Open-Meteo failed lat=%s lon=%s: %s", lat, lon, exc)
        return {
            "temperature_c": None,
            "humidity_pct": None,
            "wind_kmh": None,
            "time": None,
            "demo_fallback": True,
        }
    cur = data.get("current") or {}
    out = {
        "temperature_c": cur.get("temperature_2m"),
        "humidity_pct": cur.get("relative_humidity_2m"),
        "wind_kmh": cur.get("wind_speed_10m"),
        "time": cur.get("time"),
        "demo_fallback": False,
    }
    log.info("Open-Meteo: lat=%s lon=%s temp=%s", lat, lon, out.get("temperature_c"))
    return out
