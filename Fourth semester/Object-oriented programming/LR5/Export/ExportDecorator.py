from Export.ExportStrategy import ExportStrategy
from typing import Dict, Any

class ExportDecorator(ExportStrategy):
    """Базовый класс декоратора экспорта."""

    def __init__(self, export_strategy: ExportStrategy):
        self._export_strategy = export_strategy

    def export(self, data: Dict[str, Any]) -> str:
        return self._export_strategy.export(data)

    def get_extension(self) -> str:
        return self._export_strategy.get_extension()

    def write_to_file(self, data: Dict[str, Any], file_path: str) -> None:
        """Делегируем запись базовому экспортеру."""
        self._export_strategy.write_to_file(data, file_path)