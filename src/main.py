from weather.weather import Weather
from display.display import Display
from plants.plants import Plants

class Main():
    def __init__(self):
        self.weather = Weather()
        self.display = Display()
        self.plants = Plants()
    def main(self):
        pass

if __name__ == "__main__":
    main = Main()
    main.main()
