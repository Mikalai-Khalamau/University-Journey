"""Nager.Date public holidays API (no key)."""
from __future__ import annotations

import logging

from .http import http_get_json

log = logging.getLogger("insurance.external")

NAGER_URL = "https://date.nager.at/api/v3/PublicHolidays"


_DEMO_BY_2026 = [
    {"date": "2026-01-01", "name": "New Year's Day", "localName": "Новый год"},
    {"date": "2026-01-07", "name": "Orthodox Christmas", "localName": "Рождество"},
    {"date": "2026-03-08", "name": "Women's Day", "localName": "8 марта"},
    {"date": "2026-05-01", "name": "Labour Day", "localName": "Праздник труда"},
    {"date": "2026-05-09", "name": "Victory Day", "localName": "День Победы"},
    {"date": "2026-07-03", "name": "Independence Day", "localName": "День Независимости"},
    {"date": "2026-11-07", "name": "October Revolution Day", "localName": "7 ноября"},
    {"date": "2026-12-25", "name": "Catholic Christmas", "localName": "Католическое Рождество"},
]


def public_holidays(year: int, country_code: str = "BY") -> list[dict]:
    url = f"{NAGER_URL}/{year}/{country_code.upper()}"
    try:
        data = http_get_json(url, timeout=8.0)
    except Exception as exc:
        log.warning("Nager failed %s/%s: %s", country_code, year, exc)
        if country_code.upper() == "BY" and year == 2026:
            return list(_DEMO_BY_2026)
        return []
    if not isinstance(data, list):
        log.warning("Nager: unexpected payload for %s", url)
        return []
    log.info("Nager: loaded %s holidays for %s/%s", len(data), country_code, year)
    return data
