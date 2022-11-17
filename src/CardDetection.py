import os
import time
import numpy as np
import cv2

from src.Video import Video
import src.Cards as Cards

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
FPS = 20

class CardDetection:
    def __init__(self) -> None:
        self.arr = []

    def run(self):
        
        frame_rate_calc = 1
        freq = cv2.getTickFrequency()
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        
        video = Video((FRAME_WIDTH, FRAME_HEIGHT), FPS)
        video.start()
        time.sleep(1)

        # Load the train rank and suit images
        train_ranks = Cards.load_ranks( './images/')
        train_suits = Cards.load_suits( './images/')


        ### ---- MAIN LOOP ---- ###
        # The main loop repeatedly grabs frames from the video stream
        # and processes them to find and identify playing cards.

        cam_quit = 0 # Loop control variable

        # Begin capturing frames
        while cam_quit == 0:

            # Grab frame from video stream
            image = video.read()

            # Start timer (for calculating frame rate)
            t1 = cv2.getTickCount()

            # Pre-process camera image (gray, blur, and threshold it)
            pre_proc = Cards.preprocess_image(image)
            
            # Find and sort the contours of all cards in the image (query cards)
            cnts_sort, cnt_is_card = Cards.find_cards(pre_proc)

            # If there are no contours, do nothing
            if len(cnts_sort) != 0:

                # Initialize a new "cards" list to assign the card objects.
                # k indexes the newly made array of cards.
                cards = []
                k = 0

                # For each contour detected:
                for i in range(len(cnts_sort)):
                    if (cnt_is_card[i] == 1):

                        # Create a card object from the contour and append it to the list of cards.
                        # preprocess_card function takes the card contour and contour and
                        # determines the cards properties (corner points, etc). It generates a
                        # flattened 200x300 image of the card, and isolates the card's
                        # suit and rank from the image.
                        cards.append(Cards.preprocess_card(cnts_sort[i],image))

                        # Find the best rank and suit match for the card.
                        cards[k].best_rank_match,cards[k].best_suit_match,cards[k].rank_diff,cards[k].suit_diff = Cards.match_card(cards[k],train_ranks,train_suits)
                        

                        if cards[k].best_rank_match != "Unknown" and cards[k].best_suit_match != "Unknown":
                            if self.arr.index(cards[k].best_rank_match, "of", cards[k].best_suit_match) != - 1:
                                self.arr.append(cards[k].best_rank_match, "of", cards[k].best_suit_match)
                            
                        
                        
                        # Draw center point and match result on the image.
                        image = Cards.draw_results(image, cards[k])
                        k = k + 1
                
                # Draw card contours on image (have to do contours all at once or
                # they do not show up properly for some reason)
                if (len(cards) != 0):
                    temp_cnts = []
                    for i in range(len(cards)):
                        temp_cnts.append(cards[i].contour)
                    cv2.drawContours(image,temp_cnts, -1, (255,0,0), 2)
                
                
            # Draw framerate in the corner of the image. Framerate is calculated at the end of the main loop,
            # so the first time this runs, framerate will be shown as 0.
            cv2.putText(image,"FPS: "+str(int(frame_rate_calc)),(10,26),font,0.7,(255,0,255),2,cv2.LINE_AA)

            # Finally, display the image with the identified cards!
            cv2.imshow("Card Detector",image)

            # Calculate framerate
            t2 = cv2.getTickCount()
            time1 = (t2-t1)/freq
            frame_rate_calc = 1/time1
            
            # Poll the keyboard. If 'q' is pressed, exit the main loop.
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                cam_quit = 1
                

        # Close all windows and close the PiCamera video stream.
        cv2.destroyAllWindows()
        video.stop()




            