from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv
from api.weather import WeatherHandler

load_dotenv()

app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL,
    config={'app_name': "Weather API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

weather_handler = WeatherHandler()

@app.route('/api/v1/weather', methods=['GET'])
def get_current_weather():
    return weather_handler.handle_get_current_weather()

@app.route('/api/v1/weather/city', methods=['GET'])
def get_weather_by_city():
    return weather_handler.handle_get_weather_by_city()

@app.route('/api/v1/weather/forecast', methods=['GET'])
def get_forecast():
    return weather_handler.handle_get_forecast()

@app.route('/api/v1/weather/multiple', methods=['GET'])
def get_multiple_locations():
    return weather_handler.handle_get_multiple_locations()

@app.route('/api/v1/weather/forecast/city', methods=['GET'])
def get_forecast_by_city():
    return weather_handler.handle_get_forecast_by_city()

@app.route('/swagger.json')
def swagger():
    return jsonify({
        "swagger": "2.0",
        "info": {"title": "Weather API", "version": "1.0"},
        "host": "localhost:8080",
        "basePath": "/api/v1",
        "paths": {
            "/weather": {"get": {"summary": "Current weather by coordinates", "parameters": [
                {"name": "lat", "in": "query", "type": "string", "required": True},
                {"name": "lon", "in": "query", "type": "string", "required": True},
                {"name": "provider", "in": "query", "type": "string", "enum": ["openweather", "google"]}
            ], "responses": {"200": {"description": "OK"}}}},
            "/weather/city": {"get": {"summary": "Current weather by city name", "parameters": [
                {"name": "city", "in": "query", "type": "string", "required": True},
                {"name": "provider", "in": "query", "type": "string", "enum": ["openweather", "google"]}
            ], "responses": {"200": {"description": "OK"}}}},
            "/weather/forecast": {"get": {"summary": "Forecast by coordinates", "parameters": [
                {"name": "lat", "in": "query", "type": "string", "required": True},
                {"name": "lon", "in": "query", "type": "string", "required": True},
                {"name": "days", "in": "query", "type": "integer", "default": 5},
                {"name": "provider", "in": "query", "type": "string", "enum": ["openweather", "google"]}
            ], "responses": {"200": {"description": "OK"}}}},
            "/weather/forecast/city": {"get": {"summary": "Forecast by city name", "parameters": [
                {"name": "city", "in": "query", "type": "string", "required": True},
                {"name": "days", "in": "query", "type": "integer", "default": 5},
                {"name": "provider", "in": "query", "type": "string", "enum": ["openweather", "google"]}
            ], "responses": {"200": {"description": "OK"}}}},
            "/weather/multiple": {"get": {"summary": "Weather for multiple locations", "parameters": [
                {"name": "location", "in": "query", "type": "array", "collectionFormat": "multi", "required": True},
                {"name": "provider", "in": "query", "type": "string", "enum": ["openweather", "google"]}
            ], "responses": {"200": {"description": "OK"}}}}
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)