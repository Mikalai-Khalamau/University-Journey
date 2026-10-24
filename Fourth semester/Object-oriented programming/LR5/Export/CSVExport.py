import csv
import io
from Export.ExportStrategy import ExportStrategy


class CSVExport(ExportStrategy):
    """Стратегия экспорта в CSV."""

    def export(self, data: dict) -> str:
        output = io.StringIO()

        if "options" in data and data["options"]:
            # Экспорт списка вариантов транспорта
            writer = csv.DictWriter(output, fieldnames=["transport", "cost", "time", "mass"])
            writer.writeheader()
            for option in data["options"]:
                writer.writerow({
                    "transport": option["transport"],
                    "cost": option["cost"],
                    "time": option["time"],
                    "mass": option["mass"]
                })
        else:
            # Экспорт одного результата
            writer = csv.DictWriter(output, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)

        return output.getvalue()

    def get_extension(self) -> str:
        return ".csv"