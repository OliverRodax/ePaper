#!/usr/bin/python
import sys

sys.path.append("/home/oliver/Documents/ePaper/src")
from waveshare_epd import epd7in5b_V2
from PIL import Image, ImageDraw, ImageFont
import time
import atexit
from data.data import Data


class Display:
    def __init__(self, data):
        self.epd = epd7in5b_V2.EPD()
        self.data: Data = data
        self.font_large = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24
        )
        self.font_medium = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18
        )
        self.font_small = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14
        )

    def demo(self):
        try:
            self.epd.init()

            image_black = Image.new("1", (800, 480), 255)
            draw_black = ImageDraw.Draw(image_black)
            image_red = Image.new("1", (800, 480), 255)
            draw_red = ImageDraw.Draw(image_red)

            for i, medicine in enumerate(self.data.medicine.today_medicine):
                draw_black.text(
                    (i * 200, 0),
                    medicine["name"] + " Quantity:" + str(medicine["quantity"]),
                    font=self.font_large,
                    fill=0,
                )

            for i, plant in enumerate(self.data.plants.plants_water_today):
                draw_black.text(
                    (i * 100, 100), plant["name"], font=self.font_large,
                    fill=0
                )

            draw_black.text(
                (0, 200),
                "Weather: "
                + self.data.weather.weather["main"]
                + " Temperature: "
                + str(self.data.weather.weather["feels_like"]),
                font=self.font_large,
                fill=0,
            )

            self.epd.display(
                self.epd.getbuffer(image_black), self.epd.getbuffer(image_red)
            )
            self.epd.sleep()

        except Exception as e:
            print(f"Error: {e}")

        finally:
            print("Program finished")
