#!/usr/bin/python
from waveshare_epd import epd7in5b_V2
from PIL import Image, ImageDraw
import time
import atexit


class Display:
    def _init_(self):
        self.epd = epd7in5b_V2.EPD()

    def demo(self):
        try:
            self.epd.init()

            image = Image.new("1", (800, 480), 255)
            draw = ImageDraw.Draw(image)
            draw.text((100, 200), "Hello!", fill=0)

            self.epd.display(self.epd.getbuffer(image), self.epd.getbuffer(image))
            time.sleep(3)
            self.epd.sleep()

        except Exception as e:
            print(f"Error: {e}")

        finally:
            print("Program finished")
