from Filter.FilterStrategy import FilterStrategy
from typing import List, Dict, Any


class SpeedFilter(FilterStrategy):
    """Фильтр по минимальной скорости (максимальное время)."""

    def __init__(self, max_hours: float):
        self._max_hours = max_hours

    def filter(self, options: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [opt for opt in options if opt["time"] <= self._max_hours]