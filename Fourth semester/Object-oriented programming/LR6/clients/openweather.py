from typing import Tuple, Optional

import requests
from decimal import Decimal
from clients.weather_data_client import WeatherDataClient

class OpenWeatherClient(WeatherDataClient):
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
    
    def location_current_temperature(self, lat: Decimal, lon: Decimal):
        url = f"{self.base_url}?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
        
        try:
            resp = requests.get(url)
            if resp.status_code != 200:
                return Decimal('0'), Exception(f"openweather returned bad status: {resp.status_code}")
            
            data = resp.json()
            temp = Decimal(str(data['main']['temp']))
            return temp, None
        except requests.RequestException as e:
            return Decimal('0'), Exception(f"failed to call openweather: {e}")
        except (KeyError, ValueError) as e:
            return Decimal('0'), Exception(f"failed to decode response: {e}")

    def get_forecast(self, lat: Decimal, lon: Decimal, days: int = 5) -> Tuple[list, Optional[Exception]]:
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            'lat': float(lat),
            'lon': float(lon),
            'appid': self.api_key,
            'units': 'metric',
            'cnt': days * 8
        }

        try:
            resp = requests.get(url, params=params, timeout=10)

            if resp.status_code == 401:
                return [], Exception("invalid API key")
            if resp.status_code == 404:
                return [], Exception("location not found")
            if resp.status_code != 200:
                return [], Exception(f"openweather forecast error: {resp.status_code}")

            data = resp.json()

            if 'list' not in data:
                return [], Exception("unexpected forecast format")

            forecast_by_day = {}
            for item in data['list']:
                date = item['dt_txt'].split(' ')[0]  # "2026-05-13"
                if date not in forecast_by_day:
                    forecast_by_day[date] = []
                forecast_by_day[date].append(item)

            forecast_days = []
            for i, (date, periods) in enumerate(forecast_by_day.items()):
                if i >= days:
                    break

                temps = [p['main']['temp'] for p in periods]
                forecast_days.append({
                    'date': date,
                    'temp_min': Decimal(str(min(temps))),
                    'temp_max': Decimal(str(max(temps))),
                    'description': periods[0]['weather'][0]['description'],
                    'humidity': periods[0]['main']['humidity'],
                    'precipitation_chance': periods[0].get('pop', 0) * 100
                })

            return forecast_days, None

        except requests.RequestException as e:
            return [], Exception(f"network error: {e}")
        except (KeyError, ValueError) as e:
            return [], Exception(f"decode error: {e}")
