import xml.etree.ElementTree as ET
from Import.DataImporter import DataImporter
from typing import Dict, Any


class XMLImporter(DataImporter):
    """Адаптер для импорта XML файлов."""

    def import_data(self, file_path: str) -> Dict[str, Any]:
        tree = ET.parse(file_path)
        root = tree.getroot()

        data = {"cargo": [], "distance": 0, "transport": ""}

        for cargo_elem in root.findall('.//cargo'):
            data["cargo"].append({
                "type": cargo_elem.get("type"),
                "qty": int(cargo_elem.get("qty"))
            })

        distance_elem = root.find('.//distance')
        if distance_elem is not None:
            data["distance"] = float(distance_elem.text)

        transport_elem = root.find('.//transport')
        if transport_elem is not None:
            data["transport"] = transport_elem.text

        return data