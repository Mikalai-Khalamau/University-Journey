from abc import ABC, abstractmethod
from typing import Type, Dict, List
from Models.Cargo import Cargo, Electronics, Clothes, Foods, Equipment
from Models.Transport import Transport, Truck, Train, Tanker, Airplane, Helicopter


class LogisticsFactory(ABC):
    """Интерфейс Абстрактной Фабрики."""

    @abstractmethod
    def create_cargo(self, cargo_type: str) -> Cargo:
        pass

    @abstractmethod
    def create_transport(self, transport_type: str) -> Transport:
        pass

    @abstractmethod
    def get_available_transport_types(self) -> List[str]:
        """Возвращает список доступных типов транспорта."""
        pass


class MyLogisticsFactory(LogisticsFactory):
    """Конкретная реализация фабрики."""

    def __init__(self) -> None:
        self._cargo_map: Dict[str, Type[Cargo]] = {
            "electronics": Electronics,
            "clothes": Clothes,
            "foods": Foods,
            "equipment": Equipment
        }
        self._transport_map: Dict[str, Type[Transport]] = {
            "truck": Truck,
            "train": Train,
            "tanker": Tanker,
            "airplane": Airplane,
            "helicopter": Helicopter,
        }

    def create_cargo(self, cargo_type: str) -> Cargo:
        if cargo_type not in self._cargo_map:
            raise ValueError(f"Unknown cargo type: {cargo_type}")
        return self._cargo_map[cargo_type]()

    def create_transport(self, transport_type: str) -> Transport:
        if transport_type not in self._transport_map:
            raise ValueError(f"Unknown transport type: {transport_type}")
        return self._transport_map[transport_type]()

    def get_available_transport_types(self) -> List[str]:
        """Возвращает ключи из мапы транспорта — динамический список."""
        return list(self._transport_map.keys())