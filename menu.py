# The Main Menu

from pygame import *
import assets

# font is assets.ClashFontS, M, or L

SCREEN_WIDTH = 1180
SCREEN_HEIGHT = 768

"""menu = 0
game = 1
2 player = 2
pause screen 1 = 3
pause screen 2 = 4"""

screen = display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

def drawButton(num,button,mx,my):
    global over
    if button.collidepoint(mx,my):
        draw.rect(screen, (211,211,255), button)
        draw.rect(screen, (255,0,0), button,2)
        over = num
    else:
        draw.rect(screen, (111,111,155), button)
        draw.rect(screen, (255,255,0), button,2)
    dest = links[current][i]
    txt = assets.clashFontS.render(names[dest], True, 0)
    screen.blit(txt, (button.x+10, button.y+5))


current = 0

background = Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)

links = [(1, 2), (3), (4), (0, 1), (0, 2)]

rects = []

# in the main loop, just draw.rect(screen, GRAY, (background))




