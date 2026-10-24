from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Tuple, Optional

class WeatherDataClient(ABC):
    @abstractmethod
    def location_current_temperature(self, lat: Decimal, lon: Decimal) -> Tuple[Decimal, Optional[Exception]]:
        pass
