from abc import ABC, abstractmethod
from typing import Dict, Any


class DataImporter(ABC):
    """Интерфейс адаптера для импорта данных."""

    @abstractmethod
    def import_data(self, file_path: str) -> Dict[str, Any]:
        """Импортировать данные из файла."""
        pass