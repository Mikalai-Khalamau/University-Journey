from typing import List, Dict, Any, Optional
from Import.DataImporter import DataImporter
from Export.ExportStrategy import ExportStrategy
from Filter.FilterStrategy import FilterStrategy
from Sort.SortStrategy import SortStrategy
from Controller import LogisticsController
from Factory import MyLogisticsFactory

class LogisticsFacade:
    """
    Фасад для упрощения работы с логистической системой.
    """
    def __init__(self):
        self._factory = MyLogisticsFactory()
        self._controller = LogisticsController(self._factory)
        self._importer: Optional[DataImporter] = None
        self._exporter: Optional[ExportStrategy] = None
        self._filters: List[FilterStrategy] = []
        self._sorters: List[SortStrategy] = []

    def set_importer(self, importer: DataImporter) -> None:
        self._importer = importer

    def set_exporter(self, exporter: ExportStrategy) -> None:
        self._exporter = exporter

    def add_filter(self, filter_strategy: FilterStrategy) -> None:
        self._filters.append(filter_strategy)

    def add_sorter(self, sort_strategy: SortStrategy) -> None:
        self._sorters.append(sort_strategy)

    def clear_filters(self) -> None:
        self._filters = []

    def clear_sorters(self) -> None:
        self._sorters = []

    def import_from_file(self, file_path: str) -> Dict[str, Any]:
        if self._importer is None:
            raise ValueError("Импортер не установлен")
        return self._importer.import_data(file_path)

    def calculate_all_options(self, cargo_list: List[Dict[str, Any]],
                              distance: float) -> List[Dict[str, Any]]:
        """
        Рассчитать все варианты доставки.
        Использует динамический список транспорта из Фабрики.
        """
        transport_types = self._factory.get_available_transport_types()
        options = []

        for transport in transport_types:
            result = self._controller.process_request(cargo_list, distance, transport)
            if result["success"]:
                options.append({
                    "transport": result["transport"],
                    "cost": result["total_cost"],
                    "time": result["time_hours"],
                    "mass": result["total_mass"]
                })

        # Применяем фильтры последовательно
        for filter_strategy in self._filters:
            options = filter_strategy.filter(options)

        # Применяем сортировки с поддержкой мульти-ключа
        if self._sorters:
            # Если все сортировки в одном направлении — используем кортеж-ключ
            if all(not s.is_reverse() for s in self._sorters) or all(s.is_reverse() for s in self._sorters):
                def composite_key(item: Dict[str, Any]) -> tuple:
                    return tuple(sorter.get_key_func()(item) for sorter in self._sorters)
                options = sorted(options, key=composite_key, reverse=self._sorters[0].is_reverse())
            else:
                # Смешанные направления: стабильная сортировка от вторичного к главному
                for sorter in reversed(self._sorters):
                    options = sorted(options, key=sorter.get_key_func(), reverse=sorter.is_reverse())

        return options

    def export_to_file(self, data: Dict[str, Any], file_path: str) -> None:
        """Экспортировать данные в файл как единый интерфейс."""
        if self._exporter is None:
            raise ValueError("Экспортер не установлен")
        self._exporter.write_to_file(data, file_path)

    def process_with_all_options(self, cargo_list: List[Dict[str, Any]],
                                 distance: float) -> Dict[str, Any]:
        options = self.calculate_all_options(cargo_list, distance)
        return {
            "success": True,
            "distance": distance,
            "cargo_count": len(cargo_list),
            "options_count": len(options),
            "options": options
        }