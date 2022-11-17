import os
import time
import cv2

from src.CardDetection import CardDetection

if __name__ == "__main__":
    cardDetection = CardDetection()
    cardDetection.run()

    #Might need to put code below in a separate thread

    # loop = 0
    # while (loop == 0):
    #     for i, card in enumerate():
    #         print(card)

    #     time.sleep(1)

    #     key = cv2.waitKey(1) & 0xFF
    #     if key == ord("q"):
    #         cam_quit = 1