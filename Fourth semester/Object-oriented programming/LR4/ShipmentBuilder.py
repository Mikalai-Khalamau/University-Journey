from typing import List, Optional
from CargoItem import CargoItem
from Models.Transport import Transport
from Models.Cargo import Cargo
from Shipment import Shipment
from Factory import LogisticsFactory


class ShipmentBuilder:
    """
    Паттерн Builder. Отделяет конструирование сложного объекта (Shipment) от его представления.
    """

    def __init__(self, factory: LogisticsFactory):
        self.__factory: LogisticsFactory = factory
        self.__cargo_items: List[CargoItem] = []
        self.__distance: Optional[float] = None
        self.__transport: Optional[Transport] = None

    def add_cargo(self, cargo_type: str, quantity: int) -> 'ShipmentBuilder':
        cargo: Cargo = self.__factory.create_cargo(cargo_type)
        cargo_item: CargoItem = CargoItem(cargo, quantity)
        self.__cargo_items.append(cargo_item)
        return self

    def set_distance(self, distance: float) -> 'ShipmentBuilder':
        self.__distance = distance
        return self

    def set_transport(self, transport_type: str) -> 'ShipmentBuilder':
        self.__transport = self.__factory.create_transport(transport_type)
        return self

    def build(self) -> Shipment:
        if not self.__cargo_items:
            raise ValueError("Добавьте хотя бы один груз")
        if self.__distance is None:
            raise ValueError("Укажите расстояние")
        if self.__transport is None:
            raise ValueError("Выберите транспорт")

        return Shipment(self.__cargo_items, self.__distance, self.__transport)