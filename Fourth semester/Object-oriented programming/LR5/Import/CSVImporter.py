import csv
from Import.DataImporter import DataImporter
from typing import Dict, Any, List


class CSVImporter(DataImporter):
    """Адаптер для импорта CSV файлов."""

    def import_data(self, file_path: str) -> Dict[str, Any]:
        data = {"cargo": [], "distance": 0, "transport": ""}

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'type' in row and 'qty' in row:
                    data["cargo"].append({
                        "type": row["type"],
                        "qty": int(row["qty"])
                    })
                if 'distance' in row:
                    data["distance"] = float(row["distance"])
                if 'transport' in row:
                    data["transport"] = row["transport"]

        return data