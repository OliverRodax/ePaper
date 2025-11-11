#!/usr/bin/python
import sys
sys.path.append('/home/oliver/Documents/ePaper/src')
from waveshare_epd import epd7in5b_V2
from PIL import Image, ImageDraw
import time
import atexit
from data.data import Data


class Display:
    def __init__(self,data):
        self.epd = epd7in5b_V2.EPD()
        self.data:Data = data

    def demo(self):
        try:
            self.epd.init()

            image_black = Image.new("1", (800, 480), 255)
            draw_black = ImageDraw.Draw(image_black)
            image_red = Image.new("1", (800, 480), 255)
            draw_red = ImageDraw.Draw(image_red)
            for i, medicine in enumerate(self.data.medicine.today_medicine):
                draw_black.text((i * 100, 0), medicine["name"]+ " " + medicine["quantity"]+ " " + medicine["how often"], fill=0)
            
            for i, plant in enumerate(self.data.plants.plants_water_today):
                draw_black.text((i * 100, 100), plant["name"], fill=0)

            draw_black.text((i * 100, 100), self.data.weather.weather["main"] + self.data.weather.weather["feels_like"], fill=0)
            self.epd.display(self.epd.getbuffer(image_black), self.epd.getbuffer(image_red))
            self.epd.sleep()

        except Exception as e:
            print(f"Error: {e}")

        finally:
            print("Program finished")