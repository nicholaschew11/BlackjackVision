#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
import cv2
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
import logging    
import time
import traceback
from src.OLED.waveshare_OLED import OLED_1in5_rgb
from PIL import Image,ImageDraw,ImageFont
font_path = os.path.join(cv2.__path__[0],'qt','fonts','DejaVuSans.ttf')
logging.basicConfig(level=logging.DEBUG)

def displayMessage(message):
    try:
        disp = OLED_1in5_rgb.OLED_1in5_rgb()

        logging.info("\r 1.5inch rgb OLED ")
        # Initialize library.
        disp.Init()
        # Clear display.
        logging.info("clear display")
        disp.clear()

        # Create blank image for drawing.
        image1 = Image.new('RGB', (disp.width, disp.height), 0)
        draw = ImageDraw.Draw(image1)
        # font = ImageFont.load_default()
        font = ImageFont.truetype(font_path, size=100)
        logging.info ("***draw line")
        draw.line([(0,0),(127,0)], fill = "RED")
        draw.line([(0,0),(0,127)], fill = "RED")
        draw.line([(0,127),(127,127)], fill = "RED")
        draw.line([(127,0),(127,127)], fill = "RED")
        logging.info ("***draw text")
        draw.text((20,50), message, font = font, fill = "BLUE") # replace text w/ message later
        image1 = image1.rotate(0)
        disp.ShowImage(disp.getbuffer(image1))
        time.sleep(5)

        disp.clear()

    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        OLED_1in5_rgb.config.module_exit()
        exit()