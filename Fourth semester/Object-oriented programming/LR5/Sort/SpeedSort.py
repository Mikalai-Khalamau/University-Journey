from Sort.SortStrategy import SortStrategy
from typing import List, Dict, Any, Callable

class SpeedSort(SortStrategy):
    def __init__(self, reverse: bool = False):
        self._reverse = reverse

    def sort(self, options: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return sorted(options, key=self.get_key_func(), reverse=self._reverse)

    def get_key_func(self) -> Callable[[Dict[str, Any]], Any]:
        return lambda x: x["time"]

    def is_reverse(self) -> bool:
        return self._reverse