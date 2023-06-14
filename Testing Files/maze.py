from pygame import *
from random import *

screen = display.set_mode( (800, 600) )
running = True
BLACK = (0,0,0)
WHITE = (255, 255, 255)

gridSize = 100

width = screen.get_width()//gridSize
height = screen.get_height()//gridSize
short = 10
screen.fill(WHITE)
rects = 0


while running:
    for evnt in event.get():
        if evnt == QUIT:
            running = False
    if rects < 20:
        if randint(0,1):
            draw.rect(screen, BLACK, (randint(0,width)* gridSize, randint(0,height) * gridSize, short, randint(0,height)* gridSize))
        else:
            draw.rect(screen, BLACK, (randint(0,width)* gridSize, randint(0,height) * gridSize, randint(0, width) * gridSize, short))
        rects += 1
    display.flip()
quit()


