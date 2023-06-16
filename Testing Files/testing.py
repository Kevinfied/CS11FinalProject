from pygame import *
from random import *
# running1 = True
# running2 = True

screen1 = Rect(0,0,1080,384)

clock = time.Clock()


def r1(running1):
    screen1 = display.set_mode((700, 384))
    while running1:
        for e in event.get():
            if e.type==QUIT:
                quit()
            if e.type==MOUSEBUTTONDOWN:
                if e.button==1:
                    running1 = False
                    r2(True)
        draw.circle(screen1, (randint(0,255),randint(0,255),randint(0,255)), (randint(0,1080),randint(0,384)), randint(0,100))
        clock.tick(60)
        display.flip()


def r2(running2):
    screen2 = display.set_mode((300, 300))
    while running2:
        for e in event.get():
            if e.type==QUIT:
                quit()
            if e.type==MOUSEBUTTONDOWN:
                if e.button==1:
                    r1(True)
                    running2 = False
        draw.rect(screen2, (randint(0,255),randint(0,255),randint(0,255)), (randint(0,1080),randint(0,384),randint(0,100),randint(0,100)))
        clock.tick(60)
        display.flip()


def mainLoop(running):
    mainScreen = display.set_mode((1080, 384))
    while running:
        for e in event.get():
            if e.type==QUIT:
                quit()
        keyArray = key.get_pressed()
        if keyArray[K_SPACE]:
            r1(True)
        display.flip()

mainLoop(True)