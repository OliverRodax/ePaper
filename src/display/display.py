#!/usr/bin/python
import sys

sys.path.append("/home/oliver/Documents/ePaper/src")
from waveshare_epd import epd7in5b_V2
from PIL import Image, ImageDraw, ImageFont
import time
import atexit
from data.data import Data
import os

class Display:
    def __init__(self, data):
        self.current_dir = os.getcwd()
        self.epd = epd7in5b_V2.EPD()
        self.data: Data = data
        self.font_large = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40
        )
        self.font_medium = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18
        )
        self.font_small = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14
        )
        self.image_black = Image.new("1", (800, 480), 255)
        self.draw_black = ImageDraw.Draw(self.image_black)
        self.image_red = Image.new("1", (800, 480), 255)
        self.draw_red = ImageDraw.Draw(self.image_red)
        
    def draw_text_in_box(self, box_coords, text, font, fill=0, spacing=4, max_font_size=None, min_font_size=8, centered=False):
        """
        Draw text within a bounding box with word wrapping, newline support, and dynamic font sizing
        box_coords: (x1, y1, x2, y2)
        centered: if True, center each line horizontally; if False, left-align
        """
        x1, y1, x2, y2 = box_coords
        box_width = x2 - x1
        box_height = y2 - y1
        
        # Try to find the best font size that fits
        if max_font_size is None:
            max_font_size = font.size
        
        best_font = font
        best_lines = []
        
        # Try font sizes from max down to min
        for font_size in range(max_font_size, min_font_size - 1, -1):
            # Create temporary font
            try:
                temp_font = ImageFont.truetype(
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size
                )
            except:
                # Fallback to proportional scaling if font loading fails
                temp_font = ImageFont.truetype(font.path, font_size) if hasattr(font, 'path') else font
            
            # Split text into paragraphs and word wrap
            paragraphs = text.split('\n')
            all_lines = []
            total_height = 0
            
            for paragraph in paragraphs:
                if not paragraph.strip():  # Skip empty lines
                    continue
                    
                words = paragraph.split()
                current_line = []
                
                for word in words:
                    test_line = ' '.join(current_line + [word])
                    test_width = self.draw_black.textlength(test_line, font=temp_font)
                    
                    if test_width <= box_width:
                        current_line.append(word)
                    else:
                        if current_line:
                            line_text = ' '.join(current_line)
                            all_lines.append(line_text)
                            total_height += temp_font.size + spacing
                        current_line = [word]
                
                if current_line:
                    line_text = ' '.join(current_line)
                    all_lines.append(line_text)
                    total_height += temp_font.size + spacing
            
            # Remove extra spacing from last line
            if all_lines:
                total_height -= spacing
            
            # Check if this font size fits in the box
            if total_height <= box_height:
                best_font = temp_font
                best_lines = all_lines
                break
        
        # If no font size fits, use the smallest one and truncate if needed
        if not best_lines:
            # Use smallest font and calculate lines anyway
            smallest_font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", min_font_size
            )
            best_font = smallest_font
            # Recalculate lines with smallest font (this will fit height-wise)
            paragraphs = text.split('\n')
            best_lines = []
            
            for paragraph in paragraphs:
                if not paragraph.strip():
                    continue
                words = paragraph.split()
                current_line = []
                
                for word in words:
                    test_line = ' '.join(current_line + [word])
                    test_width = self.draw_black.textlength(test_line, font=smallest_font)
                    
                    if test_width <= box_width:
                        current_line.append(word)
                    else:
                        if current_line:
                            best_lines.append(' '.join(current_line))
                        current_line = [word]
                
                if current_line:
                    best_lines.append(' '.join(current_line))
        
        # Draw lines with the best fitting font
        y = y1
        for line in best_lines:
            line_width = self.draw_black.textlength(line, font=best_font)
            
            if centered:
                # Center each line horizontally
                x = x1 + (box_width - line_width) // 2
            else:
                # Left align
                x = x1
                
            self.draw_black.text((x, y), line, font=best_font, fill=fill)
            y += best_font.size + spacing
        
        return best_font.size  # Return the actual font size used


    def demo(self):
        try:
            self.epd.init()
            medicine_text = ""
            plant_text = ""
            for i, medicine in enumerate(self.data.medicine.today_medicine):
                medicine_text += "• " + medicine["name"]+ " " + str(medicine["quantity"]) + "\n"
            for i, plant in enumerate(self.data.plants.plants_water_today):
                plant_text = plant["name"] + "\n"
            weather_text = self.data.weather.city + "\n" + str(self.data.weather.weather["feels_like"]) + "°C" + "\n" + self.data.weather.weather["main"]
            pill_icon_path = os.path.join(self.current_dir,"src" , "data", "pill-icon-for-any-purposes-vector-3994985304.bmp")
            pill_icon = Image.open(pill_icon_path)
            
            self.image_black.paste(pill_icon, (100, 0))
            self.draw_text_in_box((0,0,400,150),medicine_text,self.font_large)
            self.draw_text_in_box((400,0,800,150),plant_text,self.font_large)
            self.draw_text_in_box((0,200,400,300),weather_text,self.font_large,centered=True)
            
            self.epd.display(
                self.epd.getbuffer(self.image_black), self.epd.getbuffer(self.image_red)
            )
            self.epd.sleep()

        except Exception as e:
            print(f"Error: {e}")

        finally:
            print("Program finished")
