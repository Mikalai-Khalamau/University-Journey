from abc import ABC, abstractmethod
from typing import Dict, Any

class ExportStrategy(ABC):
    """Интерфейс стратегии экспорта."""

    @abstractmethod
    def export(self, data: Dict[str, Any]) -> str:
        """Экспортировать данные в строку."""
        pass

    @abstractmethod
    def get_extension(self) -> str:
        """Получить расширение файла."""
        pass

    def write_to_file(self, data: Dict[str, Any], file_path: str) -> None:
        """
        Базовая реализация записи в файл.
        Декораторы могут переопределить этот метод для бинарных данных.
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.export(data))