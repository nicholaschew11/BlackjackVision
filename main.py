import os
import time
import cv2

from src.CardDetection import CardDetection

if __name__ == "__main__":
    cardDetection = CardDetection()
    cardDetection.run()