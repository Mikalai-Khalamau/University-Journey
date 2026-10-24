import pytest
from flask import Flask
from unittest.mock import Mock, patch
from api.weather import WeatherHandler
from decimal import Decimal


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True

    handler = WeatherHandler()
    handler.clients = {
        'openweather': Mock(),
        'google': Mock()
    }

    app.add_url_rule('/api/v1/weather', view_func=handler.handle_get_current_weather)
    app.add_url_rule('/api/v1/weather/city', view_func=handler.handle_get_weather_by_city)
    app.add_url_rule('/api/v1/weather/forecast', view_func=handler.handle_get_forecast)
    app.add_url_rule('/api/v1/weather/multiple', view_func=handler.handle_get_multiple_locations)

    return app


class TestApiHandler:

    def test_missing_coordinates(self, app):
        with app.test_client() as client:
            resp = client.get('/api/v1/weather')
            assert resp.status_code == 400

    def test_invalid_coordinate_format(self, app):
        with app.test_client() as client:
            resp = client.get('/api/v1/weather?lat=abc&lon=12.3')
            assert resp.status_code == 400

    def test_provider_selection_openweather(self, app):
        with patch('api.weather.CurrentWeatherController') as MockCtrl:
            mock_ctrl = Mock()

            mock_model = Mock()
            mock_model.to_dict.return_value = {"temperature": 20.0}

            mock_ctrl.get_current_weather.return_value = (mock_model, None)
            MockCtrl.return_value = mock_ctrl

            with app.test_client() as client:
                resp = client.get('/api/v1/weather?lat=53.9&lon=27.5&provider=openweather')
                assert resp.status_code == 200
                assert resp.get_json()['data']['temperature'] == 20.0

    def test_provider_selection_google(self, app):
        with patch('api.weather.CurrentWeatherController') as MockCtrl:
            mock_ctrl = Mock()

            mock_model = Mock()
            mock_model.to_dict.return_value = {"temperature": 22.0}

            mock_ctrl.get_current_weather.return_value = (mock_model, None)
            MockCtrl.return_value = mock_ctrl

            with app.test_client() as client:
                resp = client.get('/api/v1/weather?lat=51.5&lon=-0.1&provider=google')
                assert resp.status_code == 200

    def test_city_weather_success(self, app):
        with patch('api.weather.CurrentWeatherController') as MockCtrl:
            mock_ctrl = Mock()

            mock_model = Mock()
            mock_model.to_dict.return_value = {"temperature": 15.0}

            mock_ctrl.get_weather_by_city.return_value = (mock_model, None)
            MockCtrl.return_value = mock_ctrl

            with app.test_client() as client:
                resp = client.get('/api/v1/weather/city?city=Минск&provider=openweather')
                assert resp.status_code == 200
                assert resp.get_json()['data']['temperature'] == 15.0

    def test_city_weather_not_found(self, app):
        with patch('api.weather.CurrentWeatherController') as MockCtrl:
            mock_ctrl = Mock()
            mock_ctrl.get_weather_by_city.return_value = (
                Mock(temperature=Decimal('0')),
                ValueError("City 'Париж' not found")
            )
            MockCtrl.return_value = mock_ctrl

            with app.test_client() as client:
                resp = client.get('/api/v1/weather/city?city=Париж')
                assert resp.status_code == 404

    def test_forecast_success(self, app):
        with patch('api.weather.CurrentWeatherController') as MockCtrl:
            mock_ctrl = Mock()
            mock_ctrl.get_forecast.return_value = (
                Mock(to_dict=lambda: {"location": "53.9,27.5", "forecast": []}),
                None
            )
            MockCtrl.return_value = mock_ctrl

            with app.test_client() as client:
                resp = client.get('/api/v1/weather/forecast?lat=53.9&lon=27.5&days=3')
                assert resp.status_code == 200

    def test_multiple_locations_success(self, app):
        with patch('api.weather.CurrentWeatherController') as MockCtrl:
            mock_ctrl = Mock()
            mock_ctrl.get_multiple_locations.return_value = (
                Mock(to_dict=lambda: {"Минск": 15.0, "Лондон": 12.0}),
                None
            )
            MockCtrl.return_value = mock_ctrl

            with app.test_client() as client:
                resp = client.get('/api/v1/weather/multiple?location=Минск&location=Лондон')
                assert resp.status_code == 200