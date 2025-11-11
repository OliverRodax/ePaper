from weather.weather import Weather
from display.display import Display
from plants.plants import Plants
from medicine.medicine import Medicine
from data.data import Data

class Main():
    def __init__(self):
        self.weather = Weather(city="Seebenstein")
        self.medicine = Medicine()
        self.plants = Plants()
        self.data = Data(self.weather,self.plants,self.medicine)
        self.display = Display(self.data)
        self.run = True
        
    def main_loop(self):
        self.medicine.update_medicine()
        self.plants.update_plants()
        self.weather.get_weather_by_coords()
        self.display.demo()


if __name__ == "__main__":
    main = Main()
    #while main.run:
    main.main_loop()
