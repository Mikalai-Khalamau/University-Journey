from decimal import Decimal
from models.weather.get import CurrentWeather
from models.weather.forecast import ForecastDay
from datetime import datetime

class TestModels:
    def test_current_weather_to_dict(self):
        w = CurrentWeather(Decimal('15.5'))
        assert w.to_dict() == {"temperature": 15.5}

    def test_forecast_day_to_dict(self):
        day = ForecastDay(datetime(2026, 5, 13), Decimal('10'), Decimal('20'), "Sunny")
        assert day.to_dict() == {
            "date": "2026-05-13T00:00:00",
            "temp_min": 10.0,
            "temp_max": 20.0,
            "description": "Sunny"
        }

    def test_multi_location_to_dict(self):
        from models.weather.multi_location import MultiLocationWeather
        m = MultiLocationWeather({"Минск": Decimal('15'), "Лондон": Decimal('12')})
        assert m.to_dict() == {"Минск": 15.0, "Лондон": 12.0}