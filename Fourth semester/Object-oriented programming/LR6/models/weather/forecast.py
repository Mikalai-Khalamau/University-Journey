from decimal import Decimal
from typing import List
from datetime import datetime


class ForecastDay:
    def __init__(self, date: datetime, temp_min: Decimal, temp_max: Decimal, description: str):
        self.date = date
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.description = description

    def to_dict(self):
        return {
            "date": self.date.isoformat(),
            "temp_min": float(self.temp_min),
            "temp_max": float(self.temp_max),
            "description": self.description
        }


class WeatherForecast:
    def __init__(self, location: str, forecast: List[ForecastDay]):
        self.location = location
        self.forecast = forecast

    def to_dict(self):
        return {
            "location": self.location,
            "forecast": [day.to_dict() for day in self.forecast]
        }