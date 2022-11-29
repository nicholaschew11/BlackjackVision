#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging    
import time
import traceback
from waveshare_OLED import OLED_1in5_rgb
from PIL import Image,ImageDraw,ImageFont
logging.basicConfig(level=logging.DEBUG)

try:
    disp = OLED_1in5_rgb.OLED_1in5_rgb()

    logging.info("\r 1.5inch rgb OLED ")
    # Initialize library.
    disp.Init()
    # Clear display.
    logging.info("clear display")
    disp.clear()

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    OLED_1in5_rgb.config.module_exit()
    exit()