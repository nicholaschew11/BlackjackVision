import os
import time
import numpy as np
import cv2

from .blackjackk import blackjack

from src.Video import Video
import src.Cards as Cards

import pygame
import random

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
FPS = 20

pygame.init()
bounds = (1024, 768)
window = pygame.display.set_mode(bounds)
pygame.display.set_caption("BlackjackVision")



# cardBack = pygame.image.load('images/BACK.png')
# cardBack = pygame.transform.scale(cardBack, (int(238*0.8), int(332*0.8)))

playhand = []

cardtype = ["CLUB", "DIAMOND", "HEART", "SPADE"]

for t in cardtype:
  for i in range(1, 14):
    playhand.append(str("images/"+t+"-"+str(i)+".svg"))

rHand = []
currHand =[]


def addtohand(type, value):
  currHand.append(str(type+" - "+str(value)))
  rHand.append(str("src/images/"+type+"-"+str(value)+".svg"))

addtohand("CLUB", 5)

def renderGame(window,prediction):
   window.fill((94,174,235))
   font = pygame.font.SysFont('comicsans',60, True)
   font1 = pygame.font.SysFont('comicsans',40, True)

   for i in range(len(rHand)):
       print(rHand[i])
       window.blit(pygame.image.load(rHand[i]), (50+(175*i), 400))
   text = font.render("BlackjackVision", True, (255,255,255))
   window.blit(text, (300, 0))
   window.blit(pygame.image.load("src/images/rich.png"),(670,10))
   window.blit(pygame.image.load("src/images/nerd.png"),(760,10))
   text1 = font1.render(str("Optimal Next Play:"+prediction), True, (255,255,255))
   window.blit(text1, (40, 200))
renderGame(window,"")

def black(strategy_name, cards):
    strategy_name = strategy_name
    print("Player strategy:", strategy_name)
    this_table = blackjack.Table(4, 0.75)
    this_table.shoe.cards=[("2d",[0],"2")]
    for card in cards:
        this_table.shoe.cards.append(card)
    new_deck = blackjack.Deck()
    this_table.shoe.cards = this_table.shoe.cards + new_deck.cards
    return this_table.play_one_round(strategy_name)    # Play a game.
class CardDetection:
    def __init__(self) -> None:
        self.arr = []

    def run(self):
        cardiB=[]
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
        count=0
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
                
                rank={'Ace':['A',[1,11]],'Two':['2',[2]],'Three':['3',[3]],'Four':['4',[4]],'Five':['5',[5]],'Six':['6',[6]],'Seven':['7',[7]],'Eight':['8',[8]],'Nine':['9',[9]],'Ten':['T',[10]],'Jack':['J',[10]],'Queen':['Q',[10]],'King':['K',[10]],'Unknown':None}
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
                            cardName = cards[k].best_rank_match+ " of "+ cards[k].best_suit_match
                            if cardName not in self.arr:
                                self.arr.append(cardName)
                                #dictionary to store suits and rank keys + values
                                cardSuit=cards[k].best_suit_match
                                cardiB.append((rank[cards[k].best_rank_match][0]+cardSuit[0].lower(),rank[cards[k].best_rank_match][1],rank[cards[k].best_rank_match][0]))
                                print(len(cardiB))

                                if len(cardiB)>2:
                                    result = black("Basic Strategy Section 4", cardiB)
                                    print(result[len(cardiB)-3])
                                    prediction=result[len(cardiB)-3]
                                    renderGame(window,prediction)
                                    pygame.display.update()
                                    print(count)
                                    if(count%350==0):
                                        prediction = random.choice(currHand)
                                        addtohand(random.choice(cardtype), random.randrange(1, 13, 1)) 
            
                        
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




            