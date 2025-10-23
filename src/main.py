#!/usr/bin/python
from waveshare_epd import epd7in5b_V2
from PIL import Image, ImageDraw
import time
import atexit

def cleanup():
    print("Cleanup completed")

atexit.register(cleanup)

try:
    epd = epd7in5b_V2.EPD()
    print("create class")
    epd.init()

    image = Image.new('1', (800, 480), 255)
    draw = ImageDraw.Draw(image)
    draw.text((100, 200), 'Hello!', fill=0)

    epd.display(epd.getbuffer(image), epd.getbuffer(image))
    time.sleep(3)
    epd.sleep()
    
except Exception as e:
    print(f"Error: {e}")
    
finally:
    print("Program finished")