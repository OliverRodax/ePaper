import os
import requests

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

if __name__ == "__main__":
    city = "Seebenstein"
    results = geocode(city, limit=1)
    #print(results)
    if not results:
        print("Location not found")
    else:
        loc = results[0]
        lat, lon = loc["lat"], loc["lon"]
        weather = get_weather_by_coords(lat, lon)
        #print(weather)
        forecast = get_weather_forecast_by_coords(lat, lon)
        print(forecast)