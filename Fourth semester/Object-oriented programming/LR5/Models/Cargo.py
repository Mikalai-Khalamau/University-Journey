from abc import ABC


class Cargo(ABC):
    """Базовый класс груза (Information Expert для данных о грузе)."""

    def __init__(self, name: str, weight_per_unit: float, cost_per_kg: float):
        self.__name = name
        self.__weight_per_unit = weight_per_unit
        self.__cost_per_kg = cost_per_kg

    def get_name(self) -> str:
        return self.__name

    def get_weight_per_unit(self) -> float:
        return self.__weight_per_unit

    def get_cost_per_kg(self) -> float:
        return self.__cost_per_kg


class Clothes(Cargo):
    def __init__(self) -> None:
        super().__init__("Одежда", 0.8, 20)


class Electronics(Cargo):
    def __init__(self) -> None:
        super().__init__("Электроника", 1.5, 50)


class Equipment(Cargo):
    def __init__(self) -> None:
        super().__init__("Оборудование", 120.0, 15)


class Foods(Cargo):
    def __init__(self) -> None:
        super().__init__("Скоропортящиеся продукты", 10.0, 100)