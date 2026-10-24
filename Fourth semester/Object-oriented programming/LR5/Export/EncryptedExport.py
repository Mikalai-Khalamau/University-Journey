import base64
from Export.ExportDecorator import ExportDecorator


class EncryptedExport(ExportDecorator):
    """Декоратор шифрования экспорта (Base64 для демонстрации)."""

    def export(self, data: dict) -> str:
        # Получаем данные от базового экспортера
        original_data = self._export_strategy.export(data)
        # Шифруем (для лабы используем Base64, в продакшене - cryptography)
        encrypted = base64.b64encode(original_data.encode('utf-8')).decode('utf-8')
        return encrypted

    def get_extension(self) -> str:
        return self._export_strategy.get_extension() + ".enc"