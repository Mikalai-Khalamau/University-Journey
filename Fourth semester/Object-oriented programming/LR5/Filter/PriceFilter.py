from Filter.FilterStrategy import FilterStrategy
from typing import List, Dict, Any


class PriceFilter(FilterStrategy):
    """Фильтр по максимальной цене."""

    def __init__(self, max_price: float):
        self._max_price = max_price

    def filter(self, options: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [opt for opt in options if opt["cost"] <= self._max_price]