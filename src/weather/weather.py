
# Origianl Structure of a API Json
#{
#   "coord": { "lon": 16.1506, "lat": 47.6957 },
#   "weather": [
#     {
#       "id": 804,
#       "main": "Clouds",
#       "description": "overcast clouds",
#       "icon": "04n"
#     }
#   ],
#   "base": "stations",
#   "main": {
#     "temp": 10.08,
#     "feels_like": 9.47,
#     "temp_min": 10.08,
#     "temp_max": 10.08,
#     "pressure": 1005,
#     "humidity": 89,
#     "sea_level": 1005,
#     "grnd_level": 943
#   },
#   "visibility": 10000,
#   "wind": { "speed": 1.38, "deg": 219, "gust": 1.2 },
#   "clouds": { "all": 93 },
#   "dt": 1761164041,
#   "sys": {
#     "type": 2,
#     "id": 2007654,
#     "country": "AT",
#     "sunrise": 1761110661,
#     "sunset": 1761148504
#   },
#   "timezone": 7200,
#   "id": 7871872,
#   "name": "Seebenstein",
#   "cod": 200
# }

import os
import requests

class Weather():
    def __init__(self, city):
        self.API_KEY = os.getenv("WEATHER_KEY")
        if not self.API_KEY:
            raise SystemExit("Set OPENWEATHER_API_KEY in the environment")
        self.city = city
        self.GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"
        self.WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
        geocode_results = self.geocode()
        if not geocode_results:
            print("Location not found")
        else:
            loc = geocode_results[0]
            self.lat, self.lon = loc["lat"], loc["lon"]

    def geocode(self, limit: int = 1):
        q = self.city
        params = {"q": q, "limit": limit, "appid": self.API_KEY}
        resp = requests.get(self.GEOCODE_URL, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def get_weather_by_coords(self, units: str = "metric"):
        params = {"lat": self.lat, "lon": self.lon, "units": units, "appid": self.API_KEY}
        resp = requests.get(self.WEATHER_URL, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def get_weather_forecast_by_coords(self,units: str = "metric"):
        FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
        params = {"lat": self.lat, "lon": self.lon, "units": units, "appid": self.API_KEY}
        resp = requests.get(FORECAST_URL, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
            
    def strip_weather(self,weather):
        weather_stripped = {
            "main": weather["weather"][0]["main"],
            "description": weather["weather"][0]["description"],
            "feels_like": weather["main"]["feels_like"],
            "dt": weather["dt"],
            "sunrise": weather["sys"]["sunrise"],
            "sunset": weather["sys"]["sunset"],
            "temperature": weather["main"]["temp"],
            "timezone": weather["timezone"]
        }
        return weather_stripped

    def strip_forecast(self,forecast):
        stripped_forecast = []
        for weather in forecast["list"]:
            stripped_forecast.append({
            "main": weather["weather"][0]["main"],
            "description": weather["weather"][0]["description"],
            "feels_like": weather["main"]["feels_like"],
            "dt": weather["dt"],
            "dt_txt": weather["dt_txt"],
            "temperature": weather["main"]["temp"]
            }
    )
        return stripped_forecast


