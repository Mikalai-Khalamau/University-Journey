"""Nominatim (OpenStreetMap) geocoding — no API key."""
from __future__ import annotations

import logging
from urllib.parse import quote

from .geo_fallback import coords_for_city
from .http import http_get_json

log = logging.getLogger("insurance.external")

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


def geocode_city(city: str, country: str = "Belarus") -> tuple[float, float] | None:
    q = quote(f"{city}, {country}")
    url = f"{NOMINATIM_URL}?q={q}&format=json&limit=1"
    try:
        data = http_get_json(url, timeout=8.0)
    except Exception as exc:
        log.warning("Nominatim failed for %s: %s", city, exc)
        data = None
    if data:
        first = data[0]
        lat = float(first["lat"])
        lon = float(first["lon"])
        log.info("Nominatim: %s -> %s,%s", city, lat, lon)
        return lat, lon
    fallback = coords_for_city(city)
    if fallback:
        log.info("Nominatim: using fallback coords for %s", city)
        return fallback
    log.info("Nominatim: no results for %s", city)
    return None
