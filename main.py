import os
import time
import cv2
import sys

sys.path.insert(1, '/OLED')

from src.CardDetection import CardDetection

from oled import displayMessage


if __name__ == "__main__":
    displayMessage()
    cardDetection = CardDetection()
    cardDetection.run()