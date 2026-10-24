import json
from Export.ExportStrategy import ExportStrategy


class JSONExport(ExportStrategy):
    """Стратегия экспорта в JSON."""

    def export(self, data: dict) -> str:
        return json.dumps(data, ensure_ascii=False, indent=2)

    def get_extension(self) -> str:
        return ".json"