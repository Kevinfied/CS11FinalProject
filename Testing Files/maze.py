from pygame import *
from random import *
from pprint import *
screen = display.set_mode( (800, 600) )
running = True
BLACK = (0,0,0)
WHITE = (255, 255, 255)

gridSize = 100

width = screen.get_width()//gridSize
height = screen.get_height()//gridSize

horizontalLines = []
verticalLines   = []
lines = []


possibility = [ 0 for i in range(8)]+ [1]
def gridGen():
    
    for y in range(height+1):
        horizontalLines.append([])
        verticalLines.append([])
        for x in range(width+1):
            if y == 0 or y == height:
                horizontalLines[-1].append([x*gridSize, y*gridSize, (x+1)*gridSize, y*gridSize, 1])
                verticalLines[-1].append([x*gridSize, y*gridSize, x*gridSize, (y+1)*gridSize, choice(possibility)])
            else:
                horizontalLines[-1].append([x*gridSize, y*gridSize, (x+1)*gridSize, y*gridSize, choice(possibility)])
                verticalLines[-1].append([x*gridSize, y*gridSize, x*gridSize, (y+1)*gridSize, choice(possibility)])
            

        # for y in range(height):
        #     for x in range(width):
        #         horizontalLines[y][x].append()

pprint(horizontalLines)
pprint(verticalLines)


thickness = 10
screen.fill(WHITE)
rects = 0

gridGen()
while running:
    for evnt in event.get():
        if evnt.type == QUIT:
            running = False
        if evnt.type == MOUSEBUTTONDOWN:
            print('dslfslfj')
            horizontalLines = []
            verticalLines   = []
            pprint(horizontalLines); pprint(verticalLines)
            gridGen()

    # if rects < 20:
    #     if randint(0,1):
    #         draw.rect(screen, BLACK, (randint(0,width)* gridSize, randint(0,height) * gridSize, short, randint(0,height)* gridSize))
    #     else:
    #         draw.rect(screen, BLACK, (randint(0,width)* gridSize, randint(0,height) * gridSize, randint(0, width) * gridSize, short))
    #     rects += 1
    horizontalLines = []
    verticalLines   = []
    pprint(horizontalLines); pprint(verticalLines)
    gridGen()
    screen.fill(WHITE)
    for y in range(height):
        for x in range(width):
            if horizontalLines[y][x][4]:
                draw.line(screen, BLACK, (horizontalLines[y][x][0], horizontalLines[y][x][1]), (horizontalLines[y][x][2], horizontalLines[y][x][3]),thickness)
            if verticalLines[y][x][4]:
                draw.line(screen, BLACK, (verticalLines[y][x][0],   verticalLines[y][x][1]),   (verticalLines[y][x][2], verticalLines[y][x][3]),thickness) 
    # draw.line(screen, BLACK, (0,600), (800, 600),10)
    display.flip()
quit()


