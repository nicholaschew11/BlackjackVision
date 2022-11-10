import os
import time
import numpy as np
import cv2

from src.Video import Video
from src.Cards import Cards

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
FPS = 20

class CardDetection:
    def __init__(self) -> None:
        pass

    def run(self):
        video = Video.Video((FRAME_WIDTH, FRAME_HEIGHT), FPS, 0)
        video.start()
        time.sleep()


            