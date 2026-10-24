from typing import Optional
from Models.Cargo import Cargo


class CargoItem:
    """
    Класс-агрегат груза и количества.
    GRASP Information Expert: знает свою массу и стоимость.
    """

    def __init__(self, cargo: Cargo, quantity: int):
        self.__cargo = cargo
        self.__quantity = quantity

    def get_total_mass(self) -> float:
        return self.__cargo.get_weight_per_unit() * self.__quantity

    def get_total_cost(self) -> float:
        return self.get_total_mass() * self.__cargo.get_cost_per_kg()

    def get_cargo_name(self) -> str:
        return self.__cargo.get_name()