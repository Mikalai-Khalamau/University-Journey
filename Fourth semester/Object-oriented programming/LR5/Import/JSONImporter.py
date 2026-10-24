import json
from Import.DataImporter import DataImporter
from typing import Dict, Any


class JSONImporter(DataImporter):
    """Адаптер для импорта JSON файлов."""

    def import_data(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)