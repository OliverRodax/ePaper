import os
import requests
import csv
import pandas as pd
import json

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


# Use an environment variable for the API key
API_KEY = "e15eaa7e4d12f5714a90efe14861857a"
if not API_KEY:
    raise SystemExit("Set OPENWEATHER_API_KEY in the environment")

GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

def geocode(city: str, country: str | None = None, limit: int = 1):
    q = f"{city},{country}" if country else city
    params = {"q": q, "limit": limit, "appid": API_KEY}
    resp = requests.get(GEOCODE_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

def get_weather_by_coords(lat: float, lon: float, units: str = "metric"):
    params = {"lat": lat, "lon": lon, "units": units, "appid": API_KEY}
    resp = requests.get(WEATHER_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

def get_weather_forecast_by_coords(lat: float, lon: float, units: str = "metric"):
    FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"lat": lat, "lon": lon, "units": units, "appid": API_KEY}
    resp = requests.get(FORECAST_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()
        
def strip_weather(weather):
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

def strip_forecast(forecast):
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

if __name__ == "__main__":
    city = "Seebenstein"
    #results = geocode(city, limit=1)
    #print(results)
    # if not results:
    #     print("Location not found")
    # else:
    #      loc = results[0]
    #     lat, lon = loc["lat"], loc["lon"]
        #weather = get_weather_by_coords(lat, lon)
    with open('src/weather/weather.json', 'r',encoding='utf-8') as f:
        weather = json.load(f)
    striped_weather = strip_weather(weather)
    #print(striped_weather)

        #print(weather)
        # with open('src/weather/weather.json', 'w') as f:
        #     json.dump(weather, f, indent=4)
        #forecast = get_weather_forecast_by_coords(lat, lon)

    with open('src/weather/forecast.json', 'r',encoding='utf-8') as f:
        forecast = json.load(f)
    stripped_forecast = strip_forecast(forecast)
    with open('src/weather/stripped_forecast.json', 'w',encoding='utf-8') as f:
        json.dump(stripped_forecast, f, indent=4)
    print(stripped_forecast)
        # with open('forecast.json', 'w') as f:
        #     json.dump(forecast, f, indent=4)



