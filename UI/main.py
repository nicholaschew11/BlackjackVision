import pygame
import random


pygame.init()
bounds = (1024, 768)
window = pygame.display.set_mode(bounds)
pygame.display.set_caption("BlackjackVision")



cardBack = pygame.image.load('images/BACK.png')
cardBack = pygame.transform.scale(cardBack, (int(238*0.8), int(332*0.8)))

playhand = []

cardtype = ["CLUB", "DIAMOND", "HEART", "SPADE"]

for t in cardtype:
  for i in range(1, 14):
    playhand.append(str("images/"+t+"-"+str(i)+".svg"))

rHand = []
currHand =[]

def addtohand(type, value):
  currHand.append(str(type+" - "+str(value)))
  rHand.append(str("images/"+type+"-"+str(value)+".svg"))

addtohand("CLUB", 5)
prediction=""

def renderGame(window):
  window.fill((94,174,235))
  font = pygame.font.SysFont('comicsans',60, True)
  font1 = pygame.font.SysFont('comicsans',40, True)



  for i in range(len(rHand)):
    window.blit(pygame.image.load(rHand[i]), (50+(175*i), 400))

  text = font.render("BlackjackVision", True, (255,255,255))
  window.blit(text, (300, 0))
  window.blit(pygame.image.load("images/rich.png"),(670,10))
  window.blit(pygame.image.load("images/nerd.png"),(760,10))
  text1 = font1.render(str("Optimal Next Play:"+prediction), True, (255,255,255))
  window.blit(text1, (40, 200))

  


run = True
count = 0
while run:
  count+=1
  renderGame(window)
  pygame.display.update()
  print(count)
  if(count%350==0):
    prediction = random.choice(currHand)
    addtohand(random.choice(cardtype), random.randrange(1, 13, 1))


