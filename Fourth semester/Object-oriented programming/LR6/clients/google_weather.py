import requests
from decimal import Decimal
from typing import Tuple, Optional
from clients.weather_data_client import WeatherDataClient


class GoogleWeatherClient(WeatherDataClient):
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    def location_current_temperature(self, lat: Decimal, lon: Decimal) -> Tuple[Decimal, Optional[Exception]]:
        url = f"{self.base_url}/currentConditions:lookup"
        params = {
            'key': self.api_key,
            'location.latitude': float(lat),
            'location.longitude': float(lon)
        }

        try:
            resp = requests.get(url, params=params, timeout=10)

            if resp.status_code == 404:
                return Decimal('0'), Exception("location not found")
            if resp.status_code == 400:
                return Decimal('0'), Exception(f"bad request: {resp.text}")
            if resp.status_code == 403:
                return Decimal('0'), Exception("API key invalid or billing not enabled")
            if resp.status_code != 200:
                return Decimal('0'), Exception(f"google weather error: {resp.status_code}")

            data = resp.json()

            if 'temperature' not in data or 'degrees' not in data['temperature']:
                return Decimal('0'), Exception("unexpected response format")

            temp = Decimal(str(data['temperature']['degrees']))
            return temp, None

        except requests.RequestException as e:
            return Decimal('0'), Exception(f"network error: {e}")
        except (KeyError, ValueError) as e:
            return Decimal('0'), Exception(f"decode error: {e}")

    def get_forecast(self, lat: Decimal, lon: Decimal, days: int = 5) -> Tuple[list, Optional[Exception]]:
        url = f"{self.base_url}/forecast:lookup"
        params = {
            'key': self.api_key,
            'location.latitude': float(lat),
            'location.longitude': float(lon),
            'periodCount': min(days * 8, 120),
            'languageCode': 'en-US'
        }

        try:
            resp = requests.get(url, params=params, timeout=10)

            if resp.status_code == 404:
                return [], Exception("Location not found or forecast unavailable")
            if resp.status_code != 200:
                return [], Exception(f"Google API error: {resp.status_code}")

            data = resp.json()

            periods = data.get('forecast', {}).get('forecastPeriod', [])

            if not periods:
                return [], None

            forecast_by_day = {}
            for period in periods:
                start_time = period.get('startTime', '')
                if not start_time:
                    continue
                date = start_time.split('T')[0]
                forecast_by_day.setdefault(date, []).append(period)

            forecast_days = []
            for i, (date, day_periods) in enumerate(forecast_by_day.items()):
                if i >= days:
                    break

                temps = []
                for p in day_periods:
                    for temp_key in ['temperature', 'minTemperature', 'maxTemperature']:
                        val = p.get(temp_key, {}).get('degrees')
                        if val is not None:
                            temps.append(val)

                if not temps:
                    continue

                forecast_days.append({
                    'date': date,
                    'temp_min': Decimal(str(min(temps))),
                    'temp_max': Decimal(str(max(temps))),
                    'description': day_periods[0].get('weatherCondition', {}).get('description', {}).get('text', '')
                })

            return forecast_days, None

        except requests.RequestException as e:
            return [], Exception(f"Network error: {e}")
        except (KeyError, ValueError, TypeError) as e:
            return [], None