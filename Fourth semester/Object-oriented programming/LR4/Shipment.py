from typing import List
from CargoItem import CargoItem
from Models.Transport import Transport

class Shipment:
    """
    Information Expert: содержит все данные для расчета стоимости и времени.
    """

    def __init__(self, cargo_items: List[CargoItem], distance: float, transport: Transport):
        self.__cargo_items: List[CargoItem] = cargo_items
        self.__distance: float = distance
        self.__transport: Transport = transport

    def calculate_total_mass(self) -> float:
        total_mass: float = 0.0
        for cargo_item in self.__cargo_items:
            total_mass += cargo_item.get_total_mass()
        return total_mass

    def calculate_delivery_cost(self) -> float:
        # Формула: sum(c_i * m_i) + r * p_delivery
        cargo_cost: float = sum(item.get_total_cost() for item in self.__cargo_items)
        transport_cost: float = self.__distance * self.__transport.get_cost_per_km()
        return cargo_cost + transport_cost

    def calculate_delivery_time(self) -> float:
        return self.__distance / self.__transport.get_speed_km_h()

    def get_transport_name(self) -> str:
        return self.__transport.get_name()

    def get_distance(self) -> float:
        return self.__distance