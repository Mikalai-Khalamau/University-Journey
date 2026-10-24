from flask import request, jsonify
from controllers.weather import CurrentWeatherController
from clients.openweather import OpenWeatherClient
from clients.google_weather import GoogleWeatherClient
from shared.utils.env import get_env
from shared.responses.status import StatusResponse
from shared.responses.success import SuccessResponse
from decimal import Decimal

class WeatherHandler:
    def __init__(self):
        self.clients = {}

        ow_api_key = get_env("OPENWEATHER_API_KEY", "")
        ow_base_url = get_env("OPENWEATHER_BASE_URL", "")
        if ow_api_key:
            self.clients['openweather'] = OpenWeatherClient(ow_api_key, ow_base_url)

        gw_api_key = get_env("GOOGLE_WEATHER_API_KEY", "")
        gw_base_url = get_env("GOOGLE_WEATHER_BASE_URL", "")
        if gw_api_key:
            self.clients['google'] = GoogleWeatherClient(gw_api_key, gw_base_url)

    def _get_client(self, provider: str = None):
        if not provider:
            provider = 'openweather'
        if provider not in self.clients:
            return None
        return CurrentWeatherController(self.clients[provider])

    def handle_get_current_weather(self):
        try:
            provider = request.args.get('provider', 'openweather')
            lat_str = request.args.get('lat')
            lon_str = request.args.get('lon')

            if not lat_str or not lon_str:
                return jsonify(StatusResponse(400, "invalid coordinates").to_dict()), 400

            try:
                lat = Decimal(lat_str)
                lon = Decimal(lon_str)
            except:
                return jsonify(StatusResponse(400, "invalid coordinates").to_dict()), 400

            controller = self._get_client(provider)
            if not controller:
                return jsonify(StatusResponse(400, f"provider '{provider}' not available").to_dict()), 400

            result, err = controller.get_current_weather(lat, lon)
            if err:
                return jsonify(StatusResponse(500, str(err)).to_dict()), 500

            return jsonify(SuccessResponse(200, "Success", result).to_dict()), 200
        except Exception as e:
            return jsonify(StatusResponse(500, str(e)).to_dict()), 500

    def handle_get_weather_by_city(self):
        try:
            provider = request.args.get('provider', 'openweather')
            city = request.args.get('city')

            if not city:
                return jsonify(StatusResponse(400, "city parameter required").to_dict()), 400

            controller = self._get_client(provider)
            if not controller:
                return jsonify(StatusResponse(400, f"provider '{provider}' not available").to_dict()), 400

            result, err = controller.get_weather_by_city(city)
            if err:
                return jsonify(StatusResponse(404, str(err)).to_dict()), 404

            return jsonify(SuccessResponse(200, "Success", result).to_dict()), 200
        except Exception as e:
            return jsonify(StatusResponse(500, str(e)).to_dict()), 500

    def handle_get_forecast(self):
        try:
            provider = request.args.get('provider', 'google')
            lat_str = request.args.get('lat')
            lon_str = request.args.get('lon')
            days = request.args.get('days', '5')

            if not lat_str or not lon_str:
                return jsonify(StatusResponse(400, "invalid coordinates").to_dict()), 400

            try:
                lat = Decimal(lat_str)
                lon = Decimal(lon_str)
                days_int = int(days)
            except:
                return jsonify(StatusResponse(400, "invalid parameters").to_dict()), 400

            controller = self._get_client(provider)
            if not controller:
                return jsonify(StatusResponse(400, f"provider '{provider}' not available").to_dict()), 400

            result, err = controller.get_forecast(lat, lon, days_int)
            if err:
                return jsonify(StatusResponse(500, str(err)).to_dict()), 500

            return jsonify(SuccessResponse(200, "Success", result).to_dict()), 200
        except Exception as e:
            return jsonify(StatusResponse(500, str(e)).to_dict()), 500

    def handle_get_multiple_locations(self):
        try:
            provider = request.args.get('provider', 'openweather')
            locations = request.args.getlist('location')

            if not locations:
                return jsonify(StatusResponse(400, "at least one location required").to_dict()), 400

            controller = self._get_client(provider)
            if not controller:
                return jsonify(StatusResponse(400, f"provider '{provider}' not available").to_dict()), 400

            result, err = controller.get_multiple_locations(locations)
            if err:
                return jsonify(StatusResponse(500, str(err)).to_dict()), 500

            return jsonify(SuccessResponse(200, "Success", result).to_dict()), 200
        except Exception as e:
            return jsonify(StatusResponse(500, str(e)).to_dict()), 500

    def handle_get_forecast_by_city(self):
        try:
            provider = request.args.get('provider', 'openweather')
            city = request.args.get('city')
            days = request.args.get('days', '5')

            if not city:
                return jsonify(StatusResponse(400, "city parameter required").to_dict()), 400

            try:
                days_int = int(days)
            except:
                return jsonify(StatusResponse(400, "invalid days parameter").to_dict()), 400

            controller = self._get_client(provider)
            if not controller:
                return jsonify(StatusResponse(400, f"provider '{provider}' not available").to_dict()), 400

            result, err = controller.get_forecast_by_city(city, days_int)

            if err:
                return jsonify(StatusResponse(404 if "not found" in str(err).lower() else 500, str(err)).to_dict()), 500

            return jsonify(SuccessResponse(200, "Success", result).to_dict()), 200
        except Exception as e:
            return jsonify(StatusResponse(500, str(e)).to_dict()), 500