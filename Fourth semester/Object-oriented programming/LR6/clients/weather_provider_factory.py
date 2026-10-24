from typing import Optional
from clients.weather_data_client import WeatherDataClient
from clients.openweather import OpenWeatherClient
from clients.google_weather import GoogleWeatherClient


class WeatherProviderFactory:
    PROVIDERS = {
        'openweather': OpenWeatherClient,
        'google': GoogleWeatherClient,
    }

    @classmethod
    def create_client(cls, provider_name: str, api_key: str, base_url: str) -> Optional[WeatherDataClient]:
        client_class = cls.PROVIDERS.get(provider_name.lower())
        if not client_class:
            return None
        return client_class(api_key, base_url)