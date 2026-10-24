from decimal import Decimal
from typing import Tuple, Optional, List
from clients.weather_data_client import WeatherDataClient
from models.weather.get import CurrentWeather
from models.weather.forecast import WeatherForecast, ForecastDay
from models.weather.multi_location import MultiLocationWeather
from shared.locations.cities import get_city_coordinates, is_city_name
from datetime import datetime


class CurrentWeatherController:
    def __init__(self, client: WeatherDataClient):
        self.client = client

    def get_current_weather(self, lat: Decimal, lon: Decimal) -> Tuple[CurrentWeather, Optional[Exception]]:
        temperature, err = self.client.location_current_temperature(lat, lon)
        if err:
            return CurrentWeather(Decimal('0')), err
        return CurrentWeather(temperature), None

    def get_weather_by_city(self, city_name: str) -> Tuple[CurrentWeather, Optional[Exception]]:
        try:
            lat, lon = get_city_coordinates(city_name)
            return self.get_current_weather(lat, lon)
        except ValueError as e:
            return CurrentWeather(Decimal('0')), e

    def get_forecast(self, lat: Decimal, lon: Decimal, days: int = 5) -> Tuple[WeatherForecast, Optional[Exception]]:
        if hasattr(self.client, 'get_forecast'):
            forecast_data, err = self.client.get_forecast(lat, lon, days)
            if err:
                return WeatherForecast("", []), err

            forecast_days = []
            for day_data in forecast_data:
                day = ForecastDay(
                    date=datetime.fromisoformat(day_data.get('date', datetime.now().isoformat())),
                    temp_min=Decimal(str(day_data.get('temp_min', 0))),
                    temp_max=Decimal(str(day_data.get('temp_max', 0))),
                    description=day_data.get('description', '')
                )
                forecast_days.append(day)

            return WeatherForecast(f"{lat},{lon}", forecast_days), None
        else:
            return WeatherForecast("", []), Exception("Provider does not support forecast")

    def get_multiple_locations(self, locations: List[str]) -> Tuple[MultiLocationWeather, Optional[Exception]]:
        temperatures = {}

        for location in locations:
            try:
                if is_city_name(location):
                    weather, err = self.get_weather_by_city(location)
                else:
                    lat_str, lon_str = location.split(',')
                    weather, err = self.get_current_weather(Decimal(lat_str), Decimal(lon_str))

                if err:
                    return MultiLocationWeather({}), err

                temperatures[location] = weather.temperature
            except Exception as e:
                return MultiLocationWeather({}), e

        return MultiLocationWeather(temperatures), None

    def get_forecast_by_city(self, city_name: str, days: int = 5) -> Tuple[WeatherForecast, Optional[Exception]]:
        try:
            lat, lon = get_city_coordinates(city_name)
            return self.get_forecast(lat, lon, days)
        except ValueError as e:
            return WeatherForecast("", []), e