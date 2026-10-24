import pytest
from decimal import Decimal
from unittest.mock import Mock, patch
from clients.openweather import OpenWeatherClient
from clients.google_weather import GoogleWeatherClient


class TestOpenWeatherClient:
    def test_location_current_temperature_success(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'main': {'temp': 20.5}}

        with patch('clients.openweather.requests.get', return_value=mock_response):
            client = OpenWeatherClient("test_key", "http://test.url")
            temp, err = client.location_current_temperature(Decimal('53.9'), Decimal('27.5'))
            assert err is None
            assert temp == Decimal('20.5')

    def test_location_current_temperature_error(self):
        mock_response = Mock()
        mock_response.status_code = 401
        with patch('clients.openweather.requests.get', return_value=mock_response):
            client = OpenWeatherClient("bad_key", "http://test.url")
            temp, err = client.location_current_temperature(Decimal('53.9'), Decimal('27.5'))
            assert temp == Decimal('0')
            assert err is not None


class TestGoogleWeatherClient:
    def test_location_current_temperature_success(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'temperature': {'degrees': 15.7, 'unit': 'CELSIUS'}}

        with patch('clients.google_weather.requests.get', return_value=mock_response):
            client = GoogleWeatherClient("test_key", "https://weather.googleapis.com/v1")
            temp, err = client.location_current_temperature(Decimal('53.9'), Decimal('27.8'))
            assert err is None
            assert temp == Decimal('15.7')

    def test_location_current_temperature_404(self):
        mock_response = Mock()
        mock_response.status_code = 404
        with patch('clients.google_weather.requests.get', return_value=mock_response):
            client = GoogleWeatherClient("test_key", "https://weather.googleapis.com/v1")
            temp, err = client.location_current_temperature(Decimal('0'), Decimal('0'))
            assert temp == Decimal('0')
            assert err is not None
            assert "not found" in str(err).lower()

    def test_get_forecast_success(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'forecast': {
                'forecastPeriod': [
                    {
                        'startTime': '2026-05-13T00:00:00Z',
                        'minTemperature': {'degrees': 12, 'unit': 'CELSIUS'},
                        'maxTemperature': {'degrees': 20, 'unit': 'CELSIUS'},
                        'weatherCondition': {'description': {'text': 'Partly sunny'}},
                        'precipitation': {'probability': {'percent': 10}}
                    }
                ]
            }
        }

        with patch('clients.google_weather.requests.get', return_value=mock_response):
            client = GoogleWeatherClient("test_key", "https://weather.googleapis.com/v1")
            forecast, err = client.get_forecast(Decimal('53.9'), Decimal('27.8'), days=1)

            assert err is None
            assert len(forecast) == 1
            assert forecast[0]['temp_min'] == Decimal('12')
            assert forecast[0]['temp_max'] == Decimal('20')