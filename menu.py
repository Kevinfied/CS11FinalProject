# The Main Menu

from pygame import *
import assets

SCREEN_WIDTH = 1180
SCREEN_HEIGHT = 768

def mainMenu(screenWidth, screenHeight):
    running = True
    rects = []
    
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                quit()
        
        screen.fill((0,0,0))
        
    return


# font is assets.ClashFontS, M, or L




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




def drawButton(num,button,mx,my):
    global over
    if button.collidepoint(mx,my):
        draw.rect(screen, (211,211,255), button)
        draw.rect(screen, (255,0,0), button,2)
        over = num
    else:
        draw.rect(screen, (111,111,155), button)
        draw.rect(screen, (255,255,0), button,2)
    dest = links[location][i]
    txt = fnt.render(names[dest], True, 0)
    screen.blit(txt, (button.x+10, button.y+5))


init()
screen = display.set_mode((1080, 384))

names = ["cabin","fort","tavern","ship"]
pics = []
for n in names:
    p = image.load("images/"+n+".png")
    pics.append(p)

links = [[1,2,3],[0,2],[0,1],[0]]
rects = [Rect(50, 50, 100, 40),Rect(50, 120, 100, 40),Rect(50, 190, 100, 40)]
location = 0
fnt = font.SysFont("Arial", 24)
running = True
while running:
    for e in event.get():
        if e.type==QUIT:
            running = False
        if e.type==MOUSEBUTTONDOWN:
            if over > -1:
                location = links[location][over]
        
    over = -1
    mb = mouse.get_pressed()
    mx, my = mouse.get_pos()
    
    # draw everything
    screen.blit(pics[location], (0,0))
    for i in range(len(links[location])):
        drawButton(i,rects[i],mx,my)
    display.flip()

quit()




