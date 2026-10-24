"""Aggregate stats helpers (lab stage 7)."""
from __future__ import annotations

from datetime import date
from statistics import StatisticsError, mean, median, multimode


def age_years(birth: date, today: date | None = None) -> int:
    if today is None:
        today = date.today()
    return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))


def stats_triplet(values: list[float]) -> dict[str, float | None]:
    """Mean, median, mode for numeric samples (lab requirement)."""
    if not values:
        return {"mean": None, "median": None, "mode": None}
    vals = sorted(values)
    try:
        m_mode = multimode(vals)
        mode_val = float(m_mode[0]) if len(m_mode) == 1 else float(sum(m_mode) / len(m_mode))
    except StatisticsError:
        mode_val = None
    return {
        "mean": float(mean(vals)),
        "median": float(median(vals)),
        "mode": mode_val,
    }
