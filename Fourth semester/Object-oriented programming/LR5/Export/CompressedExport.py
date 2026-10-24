import zipfile
from Export.ExportDecorator import ExportDecorator
from Export.ExportStrategy import ExportStrategy
from typing import Dict, Any


class CompressedExport(ExportDecorator):
    """Декоратор сжатия экспорта (ZIP архив)."""

    def __init__(self, export_strategy: ExportStrategy, filename: str = "export"):
        super().__init__(export_strategy)
        self._filename = filename

    def export(self, data: Dict[str, Any]) -> str:
        """Возвращает base64-строку для совместимости с интерфейсом."""
        original_data = self._export_strategy.export(data)
        extension = self._export_strategy.get_extension()

        import io
        import base64
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(f"{self._filename}{extension}", original_data)
        return base64.b64encode(zip_buffer.getvalue()).decode('utf-8')

    def get_extension(self) -> str:
        return self._export_strategy.get_extension() + ".zip"

    def write_to_file(self, data: Dict[str, Any], file_path: str) -> None:
        """Переопределяем для прямой записи бинарного ZIP-архива."""
        original_data = self._export_strategy.export(data)
        base_ext = self._export_strategy.get_extension()

        with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(f"{self._filename}{base_ext}", original_data)