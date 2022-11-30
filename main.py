import os
import time
import cv2
import sys


from src.CardDetection import CardDetection

from src.OLED.oled import displayMessage


if __name__ == "__main__":
    displayMessage("Blackjack")
    cardDetection = CardDetection()
    cardDetection.run()