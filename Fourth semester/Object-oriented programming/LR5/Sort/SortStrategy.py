from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, options: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_key_func(self) -> Callable[[Dict[str, Any]], Any]:
        pass

    @abstractmethod
    def is_reverse(self) -> bool:
        pass