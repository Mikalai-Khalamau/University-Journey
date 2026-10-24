from abc import ABC

class Transport(ABC):
    """Базовый класс транспорта (Information Expert для данных о доставке)."""

    def __init__(self, name: str, cost_per_km: float, speed_km_h: float):
        self.__name = name
        self.__cost_per_km = cost_per_km
        self.__speed_km_h = speed_km_h

    def get_name(self) -> str:
        return self.__name

    def get_cost_per_km(self) -> float:
        return self.__cost_per_km

    def get_speed_km_h(self) -> float:
        return self.__speed_km_h


class Truck(Transport):
    def __init__(self) -> None:
        super().__init__("Грузовик (Земля)", 15.0, 80)


class Train(Transport):
    def __init__(self) -> None:
        super().__init__("Поезд (Земля)", 5.0, 60)


class Tanker(Transport):
    def __init__(self) -> None:
        super().__init__("Танкер (Вода)", 2.0, 35)


class Airplane(Transport):
    def __init__(self) -> None:
        super().__init__("Самолет (Воздух)", 150.0, 850)


class Helicopter(Transport):
    def __init__(self) -> None:
        super().__init__("Вертолет (Воздух)", 200.0, 250)