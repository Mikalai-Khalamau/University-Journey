from decimal import Decimal
from typing import Dict


class MultiLocationWeather:
    def __init__(self, temperatures: Dict[str, Decimal]):
        self.temperatures = temperatures

    def to_dict(self):
        return {
            location: float(temp)
            for location, temp in self.temperatures.items()
        }