from controllers.weather import CurrentWeatherController
from decimal import Decimal
from unittest.mock import Mock, patch
from clients.openweather import OpenWeatherClient
from clients.google_weather import GoogleWeatherClient
import requests
class TestCurrentWeatherController:

    def test_get_current_weather_success(self):
        mock_client = Mock()
        mock_client.location_current_temperature.return_value = (Decimal('20.5'), None)

        controller = CurrentWeatherController(mock_client)
        result, err = controller.get_current_weather(Decimal('53.9'), Decimal('27.5'))

        assert err is None
        assert result.temperature == Decimal('20.5')

    def test_get_weather_by_city_minsk(self):
        mock_client = Mock()
        mock_client.location_current_temperature.return_value = (Decimal('15.0'), None)

        controller = CurrentWeatherController(mock_client)
        result, err = controller.get_weather_by_city("Минск")

        assert err is None
        assert result.temperature == Decimal('15.0')

    def test_get_weather_by_invalid_city(self):
        mock_client = Mock()
        controller = CurrentWeatherController(mock_client)

        result, err = controller.get_weather_by_city("InvalidCity")

        assert err is not None

class TestOpenWeatherAdvanced:
    def test_forecast_success(self):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            'list': [
                {'dt_txt': '2026-05-13 12:00:00', 'main': {'temp': 18, 'humidity': 60}, 'weather': [{'description': 'clouds'}], 'pop': 0.2},
                {'dt_txt': '2026-05-13 15:00:00', 'main': {'temp': 20, 'humidity': 55}, 'weather': [{'description': 'clouds'}], 'pop': 0.1}
            ]
        }
        with patch('clients.openweather.requests.get', return_value=mock_resp):
            client = OpenWeatherClient("k", "u")
            forecast, err = client.get_forecast(Decimal('53.9'), Decimal('27.5'), days=1)
            assert err is None
            assert len(forecast) == 1
            assert forecast[0]['temp_max'] == Decimal('20')

    def test_network_error(self):
        with patch('clients.openweather.requests.get', side_effect=requests.exceptions.ConnectionError("timeout")):
            client = OpenWeatherClient("k", "u")
            temp, err = client.location_current_temperature(Decimal('1'), Decimal('1'))
            assert temp == Decimal('0')
            assert "network error" in str(err).lower() or "failed to call" in str(err).lower()

class TestGoogleAdvanced:
    def test_forecast_success(self):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            'forecast': {
                'forecastPeriod': [
                    {'startTime': '2026-05-13T00:00:00Z', 'minTemperature': {'degrees': 10}, 'maxTemperature': {'degrees': 18}, 'weatherCondition': {'description': {'text': 'Rain'}}}
                ]
            }
        }
        with patch('clients.google_weather.requests.get', return_value=mock_resp):
            client = GoogleWeatherClient("k", "u")
            forecast, err = client.get_forecast(Decimal('53.9'), Decimal('27.5'), days=1)
            assert err is None
            assert forecast[0]['temp_min'] == Decimal('10')

    def test_decode_error(self):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.side_effect = ValueError("bad json")
        with patch('clients.google_weather.requests.get', return_value=mock_resp):
            client = GoogleWeatherClient("k", "u")
            temp, err = client.location_current_temperature(Decimal('1'), Decimal('1'))
            assert "decode error" in str(err).lower()