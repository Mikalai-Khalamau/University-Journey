from abc import ABC, abstractmethod
from typing import List, Dict, Any


class FilterStrategy(ABC):
    """Интерфейс стратегии фильтрации."""

    @abstractmethod
    def filter(self, options: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Отфильтровать список вариантов."""
        pass