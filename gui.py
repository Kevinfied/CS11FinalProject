# The Main Menu

from pygame import *
import assets

import assets
import tank

from math import *
from random import *


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700



def play():
    def pauseMenu():
        pause = True
        while pause:
            for evt in event.get():
                if evt.type == QUIT:
                    quit()
                if evt.type == KEYDOWN:
                    if evt.key == K_ESCAPE:
                        return False
            screen.fill(BLACK)
            pauseText = assets.clashFontM.render("Paused", True, RED)
            screen.blit(pauseText, (screen.get_width()/2 - pauseText.get_width()/2, screen.get_height()/2 - pauseText.get_height()/2))
            display.flip()
            return True

    mainRunning = True
    paused = False
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 700
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLACK = (0,0,0)
    BLUE = (0,0,255)
    GREY = (155,155,155)
    screen = display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    display.set_caption("ICS3U FSE")
    display.set_icon(assets.blueBase)

    wallwidth = 20
    space = Rect(wallwidth,wallwidth,SCREEN_WIDTH-2*wallwidth, SCREEN_HEIGHT-2*wallwidth)
    xmin = wallwidth
    xmax = SCREEN_WIDTH- wallwidth
    ymin = wallwidth
    ymax = SCREEN_HEIGHT - wallwidth

    tankLeft = tank.Tank(screen, assets.redBase, 200, screen.get_height()/2, 0, RED, 1, 'player1')
    tankRight = tank.Tank(screen, assets.blackBase, 800, screen.get_height()/2, 0, BLACK, 1, 'player2')
    dummy = tank.Tank(screen, assets.blueBase, 500, screen.get_height()/2, 0, BLUE, 3, 'dummy')
    dummy.angVel = 2*pi/180; dummy.mag = 4; dummy.bulletVel = 8; dummy.reloadPeriod = 5000

    Tanks = [tankLeft, tankRight,dummy]
    del Tanks[2]
    # Tanks = [tank.tankLeft, tank.tankRight]
    lis = [0 for i in range(50)] + [1]



    #map stuff
    gridSize = 100
    horizontalLines = []
    verticalLines   = []
    possibility = [ 0 for i in range(8)]+ [1]
    width = screen.get_width()//gridSize
    height = screen.get_height()//gridSize
    thickness = 10
    def gridGen():
        for y in range(height+1):
            horizontalLines.append([])
            verticalLines.append([])
            for x in range(width+1):
                # if y == 0 or y == height-1:
                #     horizontalLines[-1].append([x*gridSize, y*gridSize, (x+1)*gridSize, y*gridSize, 1])
                #     verticalLines[-1].append([x*gridSize, y*gridSize, x*gridSize, (y+1)*gridSize, choice(possibility)])
                # else:
                if y == 0 or y == height:
                    horizontalLines[-1].append([x*gridSize, y*gridSize, (x+1)*gridSize, y*gridSize, 1])
                    verticalLines[-1].append([x*gridSize, y*gridSize, x*gridSize, (y+1)*gridSize, choice(possibility)])
                if x == 0 or x == width:
                    horizontalLines[-1].append([x*gridSize, y*gridSize, (x+1)*gridSize, y*gridSize, choice(possibility)])
                    verticalLines[-1].append([x*gridSize, y*gridSize, x*gridSize, (y+1)*gridSize, 1])
                else:
                    horizontalLines[-1].append([x*gridSize, y*gridSize, (x+1)*gridSize, y*gridSize, choice(possibility)])
                    verticalLines[-1].append([x*gridSize, y*gridSize, x*gridSize, (y+1)*gridSize, choice(possibility)])
            
    def gridDraw():
        for y in range(len(horizontalLines)):
            for x in range(len(horizontalLines[y])):
                if horizontalLines[y][x][4]:
                    draw.line(screen, BLACK, (horizontalLines[y][x][0], horizontalLines[y][x][1]), (horizontalLines[y][x][2], horizontalLines[y][x][3]),thickness)
                if verticalLines[y][x][4]:
                    draw.line(screen, BLACK, (verticalLines[y][x][0],   verticalLines[y][x][1]),   (verticalLines[y][x][2], verticalLines[y][x][3]),thickness)  

    def ifHitWalls():
        for y in range(len(horizontalLines)):
            for x in range(len(horizontalLines[y])):
                
                    for ta in Tanks:
                        for shot in ta.shots:
                            if horizontalLines[y][x][4] and horizontalLines[y][x][0] <= shot[tank.X] and shot[tank.X] <= horizontalLines[y][x][2]:
                                # print('inRange')
                                if shot[tank.Y] <= horizontalLines[y][x][1] + thickness/2 + ta.bulletRad and shot[tank.Y] >= horizontalLines[y][x][1] - thickness/2 - ta.bulletRad:
                                    shot[tank.VY] = -shot[tank.VY]
                                    tank.bounceSound('pong')
                            if verticalLines[y][x][4] and verticalLines[y][x][1] <= shot[tank.Y] and shot[tank.Y] <= verticalLines[y][x][3]:
                                # print('inRange')
                                if shot[tank.X] <= verticalLines[y][x][0] + thickness/2 + ta.bulletRad and shot[tank.X] >= verticalLines[y][x][0] - thickness/2 - ta.bulletRad:
                                    shot[tank.VX] = -shot[tank.VX]
                                    tank.bounceSound('ping')
                        
                # if verticalLines[y][x][4:]:


    gridGen()

    while mainRunning:
        if not paused:
            rightShoot,leftShoot = False, False
            for evt in event.get():
                if evt.type == QUIT:
                    mainRunning = False
                if evt.type == KEYDOWN:
                    if evt.key == K_c:
                        leftShoot = True
                    if evt.key == K_SLASH:
                        rightShoot = True
                    if evt.key == K_ESCAPE:
                        paused = True
                if evt.type == MOUSEBUTTONDOWN:
                    horizontalLines = []
                    verticalLines   = []
                    gridGen()

            keyArray = key.get_pressed()

            screen.fill(GREY)
            # draw.rect(screen, GREY, space)
            # for map in level.map1:
            #     draw.rect(screen, (0,0,0), map)

        

            # print(keyArray[K_w],keyArray[K_s],keyArray[K_a],keyArray[K_d],leftShoot,"      ", keyArray[K_UP],keyArray[K_DOWN],keyArray[K_LEFT],keyArray[K_RIGHT], rightShoot)
            tankLeft.update(keyArray[K_w],keyArray[K_s],keyArray[K_a],keyArray[K_d],leftShoot) 
            tankRight.update(keyArray[K_UP],keyArray[K_DOWN],keyArray[K_LEFT],keyArray[K_RIGHT], rightShoot)
            if len(Tanks) == 3:
                dummy.update(0, 0, 0, 1, 0)


            deadone = tank.deathDetect(Tanks)
            if deadone:
                mixer.Sound.play(assets.deathExplosion)
                _ = screen.copy()
                for i in range(8):
                    screen.blit(_, (0,0))
                    assets.explosions[i] = transform.scale(assets.explosions[i], (deadone.scale*100, deadone.scale*100))
                    heherect = assets.explosions[i].get_rect(center = (deadone.x, deadone.y))
                    screen.blit(assets.explosions[i], heherect)
                    time.delay(100)
                    display.flip()
                time.delay(3000)
                mainRunning = False

            for ta in Tanks:
                if tank.touchingWalls(xmin,xmax, ymin, ymax, ta.basePoints):
                    ta.angle -= ta.movement[0]
                    ta.x     -= ta.movement[1]
                    ta.y     -= ta.movement[2]
            ifHitWalls()
            

            gridDraw()
            display.flip()
            time.Clock().tick(50)
        else:
            for evt in event.get():
                if evt.type == QUIT:
                    quit()
                if evt.type == KEYDOWN:
                    if evt.key == K_ESCAPE:
                        paused = False

            pauseText = assets.clashFontL.render("Paused", True, RED)
            screen.blit(pauseText, (screen.get_width()/2 - pauseText.get_width()/2, screen.get_height()/2 - pauseText.get_height()/2))
            display.flip()


    

# def hoverButton(button):
#     button = Rect(button[0], button[1], button[2], button[3])
#     buttonX = button[0]
#     buttonY = button[1]
#     buttonWidth = button[2]
#     buttonHeight = button[3]

#     if buttonWidth < 250:

    
#     return button

# def drawButton(button, mx, my):
#     buttonX = button[0]
#     buttonY = button[1]
#     buttonWidth = button[2]
#     buttonHeight = button[3]


    


def mainMenu():
    init()
    mainMenuClock = time.Clock()
    mainScreen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    running = True
    rects = [Rect(SCREEN_WIDTH/2-200, (SCREEN_HEIGHT/4 * 3 )-150, 400, 100), Rect(SCREEN_WIDTH/2-200, (SCREEN_HEIGHT/4) * 3, 400, 100)]
    play1Rect = Rect(SCREEN_WIDTH/2-200, (SCREEN_HEIGHT/4 * 3 )-150, 400, 100)
    play2Rect = Rect(SCREEN_WIDTH/2-200, (SCREEN_HEIGHT/4) * 3, 400, 100)
    button1Hover = False
    button2Hover = False
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                quit()
            if evt.type == MOUSEBUTTONDOWN:
                if play1Rect.collidepoint(mx, my):
                    play()
                    return
                elif play2Rect.collidepoint(mx, my):
                    return
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()


        mainScreen.fill((255, 255, 255))

        titleTxt = assets.clashFontTitle.render("Tank Trouble", True, (0, 0, 0))
        titleRect = titleTxt.get_rect()
        titleRect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/4)
        mainScreen.blit(titleTxt, (titleRect))

        play1txt = assets.clashFontL.render("Play", True, (0, 0, 0))
        play1txtRect = play1txt.get_rect()
        play1txtRect.center = ((SCREEN_WIDTH/2-200) + (400/2), ((SCREEN_HEIGHT/4 * 3 )-150) + (100/2))

        draw.rect(mainScreen, (0, 0, 255), play1Rect, 50, 10)
        mainScreen.blit(play1txt, (play1txtRect))
        draw.rect(mainScreen, (0, 0,255), play2Rect, 50, 10)

        if play1Rect.collidepoint(mx, my):
            if mb[0] == 0:
                play1txtL = assets.clashFontXL.render("Play", True, (0, 0, 0))
                play1txtLRect = play1txtL.get_rect()
                play1txtLRect.center = ((SCREEN_WIDTH/2-200) + (400/2), ((SCREEN_HEIGHT/4 * 3 )-150) + (100/2))
                button1Hover = True
                buttonH1 = Rect(SCREEN_WIDTH/2-210, (SCREEN_HEIGHT/4 * 3 )-160, 420, 120)
                draw.rect(mainScreen, (0, 0, 255), buttonH1, 60, 10)
                mainScreen.blit(play1txtL, (play1txtLRect))
                # hoverButton(mainScreen, play1Rect, mx, my)
        
        if play2Rect.collidepoint(mx, my):
            if mb[0] == 0:
                # play2txtL = assets.clashFontXL.render("Play", True, (0, 0, 0))
                # play2txtLRect = play2txtL.get_rect()
                # play2txtLRect.center = ((SCREEN_WIDTH/2-200) + (400/2), ((SCREEN_HEIGHT/4) * 3) + (100/2))
                button2Hover = True
                buttonH2 = Rect(SCREEN_WIDTH/2-210, (SCREEN_HEIGHT/4) * 3 - 10, 420, 120)
                draw.rect(mainScreen, (0, 0, 255), buttonH2, 60, 10)
                # mainScreen.blit(play2txtL, (play2txtLRect))
                # hoverButton(mainScreen, play2Rect, mx, my)
        
        # if play1Rect.collidepoint(mx, my):
        #     if mb[0] == 0:
        #         button1Hover = True
        #         buttonH1 = hoverButton(play1Rect)
        #         draw.rect(mainScreen, (0, 0, 255), buttonH1, 200, 20)
        #         # hoverButton(mainScreen, play1Rect, mx, my)
        # elif play2Rect.collidepoint(mx, my):
        #     if mb[0] == 0:
        #         hoverButton(mainScreen, play2Rect, mx, my)

        # if button1Hover == False:

    
        "USE time.wait() for the button hover effect so it doesnt change the tick speed"

        # mainMenuClock.tick(60)
        display.flip()
        
    return







def gameOverScreen():
    return

def settingsScreen():
    # Save settings in file i/o
    return













# def pauseMenu():
#     pauseScreen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#     paused = True
#     while paused:
#         for evt in event.get():
#             if evt.type == QUIT:
#                 quit()
#             if evt.type == KEYDOWN:
#                 if evt.key == K_ESCAPE:

#                     paused = False

mainMenu()



# """menu = 0
# game = 1
# 2 player = 2
# pause screen 1 = 3
# pause screen 2 = 4"""

# screen = display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# def drawButton(num,button,mx,my):
#     global over
#     if button.collidepoint(mx,my):
#         draw.rect(screen, (211,211,255), button)
#         draw.rect(screen, (255,0,0), button,2)
#         over = num
#     else:
#         draw.rect(screen, (111,111,155), button)
#         draw.rect(screen, (255,255,0), button,2)
#     dest = links[current][i]
#     txt = assets.clashFontS.render(names[dest], True, 0)
#     screen.blit(txt, (button.x+10, button.y+5))


# current = 0

# background = Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)

# links = [(1, 2), (3), (4), (0, 1), (0, 2)]

# rects = []

# # in the main loop, just draw.rect(screen, GRAY, (background))




# def drawButton(num,button,mx,my):
#     global over
#     if button.collidepoint(mx,my):
#         draw.rect(screen, (211,211,255), button)
#         draw.rect(screen, (255,0,0), button,2)
#         over = num
#     else:
#         draw.rect(screen, (111,111,155), button)
#         draw.rect(screen, (255,255,0), button,2)
#     dest = links[location][i]
#     txt = fnt.render(names[dest], True, 0)
#     screen.blit(txt, (button.x+10, button.y+5))


# init()
# screen = display.set_mode((1080, 384))

# names = ["cabin","fort","tavern","ship"]
# pics = []
# for n in names:
#     p = image.load("images/"+n+".png")
#     pics.append(p)

# links = [[1,2,3],[0,2],[0,1],[0]]
# rects = [Rect(50, 50, 100, 40),Rect(50, 120, 100, 40),Rect(50, 190, 100, 40)]
# location = 0
# fnt = font.SysFont("Arial", 24)
# running = True
# while running:
#     for e in event.get():
#         if e.type==QUIT:
#             running = False
#         if e.type==MOUSEBUTTONDOWN:
#             if over > -1:
#                 location = links[location][over]
        
#     over = -1
#     mb = mouse.get_pressed()
#     mx, my = mouse.get_pos()
    
#     # draw everything
#     screen.blit(pics[location], (0,0))
#     for i in range(len(links[location])):
#         drawButton(i,rects[i],mx,my)
#     display.flip()

# quit()




