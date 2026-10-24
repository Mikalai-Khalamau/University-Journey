from clients.weather_provider_factory import WeatherProviderFactory
from clients.openweather import OpenWeatherClient
from clients.google_weather import GoogleWeatherClient
import pytest

class TestWeatherProviderFactory:
    def test_create_openweather(self):
        client = WeatherProviderFactory.create_client("openweather", "key1", "url1")
        assert isinstance(client, OpenWeatherClient)
        assert client.api_key == "key1"

    def test_create_google(self):
        client = WeatherProviderFactory.create_client("google", "key2", "url2")
        assert isinstance(client, GoogleWeatherClient)

    def test_create_unknown_provider(self):
        client = WeatherProviderFactory.create_client("yandex", "key", "url")
        assert client is None

    @pytest.mark.parametrize("provider", ["OPENWEATHER", "OpenWeather", "openweather"])
    def test_case_insensitive(self, provider):
        client = WeatherProviderFactory.create_client(provider, "k", "u")
        assert client is not None