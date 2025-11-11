from weather.weather import Weather
from plants.plants import Plants
from medicine.medicine import Medicine


class Data():
    def __init__(self, weather, plants, medicine,):
        self.weather:Weather = weather
        self.plants:Plants = plants
        self.medicine:Medicine = medicine