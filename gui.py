# The Main Menu

from pygame import *
import assets

import assets
import tank

from math import *
from random import *

import settings

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700 + 80



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
    # SCREEN_WIDTH = 1000
    # SCREEN_HEIGHT = 700
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLACK = (0,0,0)
    BLUE = (0,0,255)
    GREY = (155,155,155)
    WHITE = (255,255,255)
    screen = display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    display.set_caption("ICS3U FSE")
    display.set_icon(assets.blueBase)
    gameScreenHeight = 700
    # wallwidth = 20
    # space = Rect(wallwidth,wallwidth,SCREEN_WIDTH-2*wallwidth, SCREEN_HEIGHT-2*wallwidth)
    # xmin = wallwidth
    # xmax = SCREEN_WIDTH- wallwidth
    # ymin = wallwidth
    # ymax = SCREEN_HEIGHT - wallwidth

    #map stuff
    gridSize = 100
    horizontalLines = []
    verticalLines   = []
    possibility = [ 0 for i in range(8)]+ [1]
    width = SCREEN_WIDTH//gridSize
    height = gameScreenHeight//gridSize
    thickness = 10
    def gridGen():
        del horizontalLines[:]
        del verticalLines[:]
        for y in range(height+1):
            horizontalLines.append([])
            verticalLines.append([])
            for x in range(width+1):
                if (y == 0 or y == height): 
                    horizontalLines[-1].append([x*gridSize, y*gridSize, (x+1)*gridSize, y*gridSize, 1]) #1
                    
                    if (x == 0 or x == width) and y != height:
                        verticalLines[-1].append([x*gridSize, y*gridSize, x*gridSize, (y+1)*gridSize, 1]) #1
                    elif y != height:
                        verticalLines[-1].append([x*gridSize, y*gridSize, x*gridSize, (y+1)*gridSize, choice(possibility)]) #choi
                    else:
                        verticalLines[-1].append([x*gridSize, y*gridSize, x*gridSize, (y+1)*gridSize, 0])
                elif (x == 0 or x == width):
                    verticalLines[-1].append([x*gridSize, y*gridSize, x*gridSize, (y+1)*gridSize, 1]) #1
                    horizontalLines[-1].append([x*gridSize, y*gridSize, (x+1)*gridSize, y*gridSize, choice(possibility)]) #choi
                else:
                    horizontalLines[-1].append([x*gridSize, y*gridSize, (x+1)*gridSize, y*gridSize, choice(possibility)])#choice(possibility)
                    verticalLines[-1].append([x*gridSize, y*gridSize, x*gridSize, (y+1)*gridSize, choice(possibility)])
        # horizontalLines.append([])
        # verticalLines.append([])
        # horizontalLines[-1].append([2*gridSize, 2*gridSize, 3*gridSize, 2*gridSize, 1])
        # horizontalLines[-1].append([2*gridSize, 2*gridSize, 3*gridSize, 2*gridSize, 0])
        # verticalLines[-1].append([2*gridSize, 2*gridSize, 2*gridSize, 3*gridSize, 1])
        # verticalLines[-1].append([2*gridSize, 2*gridSize, 2*gridSize, 3*gridSize, 1])
            
    def gridDraw():
        for y in range(len(horizontalLines)):
            for x in range(len(horizontalLines[y])):
                if horizontalLines[y][x][4]:
                    draw.line(screen, BLACK, (horizontalLines[y][x][0], horizontalLines[y][x][1]), (horizontalLines[y][x][2], horizontalLines[y][x][3]),thickness)
                if verticalLines[y][x][4]:
                    draw.line(screen, BLACK, (verticalLines[y][x][0],   verticalLines[y][x][1]),   (verticalLines[y][x][2], verticalLines[y][x][3]),thickness)  


    def within(min, val, ma):
        if min <= val and val <= ma:
            return True
        return False
    def ifOutsideBox(xmin, xmax, ymin, ymax, points):
        for point in points:
            if point[0]< xmin or point[0] > xmax or point[1] < ymin or point[1] > ymax:
                return True
        return False
    def ifInsideBox(xmin, xmax, ymin, ymax, points):
        for point in points:
            if point[0]>= xmin and point[0] <= xmax and point[1] >= ymin and point[1] <= ymax:
                return True
        return False
    def ifHitWalls():
        for y in range(len(horizontalLines)):
            for x in range(len(horizontalLines[y])):
                for ta in Tanks:
                    if horizontalLines[y][x][4] or verticalLines[y][x][4]:
                        
                        x1 = horizontalLines[y][x][0]; x2 = horizontalLines[y][x][2]; ycoord = horizontalLines[y][x][1]
                        xcoord = verticalLines[y][x][0]; y1 = verticalLines[y][x][1]; y2 = verticalLines[y][x][3]
                
                    
                        for shot in ta.shots:
                            
                            if horizontalLines[y][x][4]:  
                                if within(ycoord - thickness/2 - ta.bulletRad, shot[tank.Y] , ycoord + thickness/2 + ta.bulletRad) and within(x1, shot[tank.X], x2):
                            
                                    shot[tank.VY] = -shot[tank.VY]
                                    tank.bounceSound('pong')
                                elif within(ycoord - thickness/2, shot[tank.Y], ycoord + thickness/2) and within(x1 - ta.bulletRad, shot[tank.X], x2 + ta.bulletRad):
                                
                                    shot[tank.VX] = -shot[tank.VX]
                                    tank.bounceSound('ping')
                                
                            if verticalLines[y][x][4]:
                                
                                if within(xcoord - thickness/2 - ta.bulletRad, shot[tank.X], xcoord + thickness/2 + ta.bulletRad) and within(y1, shot[tank.Y], y2):
                                
                                    shot[tank.VX] = -shot[tank.VX]
                                    tank.bounceSound('ping')
                            
                                elif within(xcoord - thickness/2, shot[tank.X], xcoord + thickness/2) and within(y1 - ta.bulletRad, shot[tank.Y], y2 + ta.bulletRad):
                                
                                    shot[tank.VY] = -shot[tank.VY]
                                    tank.bounceSound('pong')
                        # pointinRect
                        if horizontalLines[y][x][4] and (ifInsideBox(x1, x2, ycoord-thickness/2, ycoord+thickness/2, ta.basePoints) or ta.small_rect.colliderect((x1, ycoord-thickness/2, x2-x1, thickness))):
                                print('touching')
                                undoMotion(ta) #no box points in the tank
                        if verticalLines[y][x][4] and (ifInsideBox(xcoord-thickness/2, xcoord+thickness/2, y1, y2, ta.basePoints) or ta.small_rect.colliderect((xcoord-thickness/2, y1, thickness, y2-y1))):
                                print('touching')
                                undoMotion(ta)

    

    def undoMotion(ta):
        ta.angle -= ta.movement[0]
        ta.x     -= ta.movement[1]
        ta.y     -= ta.movement[2]

    tankLeft = tank.Tank(screen, assets.redBase, 200, gameScreenHeight/2, 0, RED, 1, 'player1')
    tankRight = tank.Tank(screen, assets.blackBase, 800, gameScreenHeight/2, 0, BLACK, 1, 'player2')
    dummy = tank.Tank(screen, assets.blueBase, 500, gameScreenHeight/2, 0, BLUE, 3, 'dummy')
    dummy.angVel = 2*pi/180; dummy.mag = 4; dummy.bulletVel = 8; dummy.reloadPeriod = 5000

    Tanks = [tankLeft, tankRight,dummy]
    del Tanks[2]
    # Tanks = [tank.tankLeft, tank.tankRight]

    def tanksReset():
    
        for ta in Tanks:
            ta.angle = random()*2*pi
            ta.x = horizontalLines[randint(0,height-1)][randint(0,width-1)][0]+50
            ta.y = horizontalLines[randint(0,height-1)][randint(0,width-1)][1]+50
            ta.shots = []
    def drawScoreBoard(scorel, scorer):
        rectLeft = Rect(0, gameScreenHeight, 100, 80)
        rectRight = Rect(SCREEN_WIDTH-100, gameScreenHeight, 100, 80)
        draw.rect(screen, RED, rectLeft)
        draw.rect(screen, BLACK, rectRight)
        lt = assets.clashFontM.render(str(scorel), True, WHITE )
        rt = assets.clashFontM.render(str(scorer), True, WHITE )
        screen.blit(lt, lt.get_rect(center = rectLeft.center) )
        screen.blit(rt, rt.get_rect(center = rectRight.center) )
    leftScore = rightScore = 0
    gridGen()
    tanksReset()
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
                    if evt.key == K_BACKSLASH:
                        gridGen()

            keyArray = key.get_pressed()
            screen.fill(GREY)
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
                # time.delay(3000)
                if deadone == tankLeft:
                    rightScore += 1
                else:
                    leftScore += 1
                gridGen()
                tanksReset()

            
            ifHitWalls()
            gridDraw()
            drawScoreBoard(leftScore, rightScore)
            tank.bulletVanish(Tanks)
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
                    settingsScreen()
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
        settingstxt = assets.clashFontL.render("Settings", True, (0, 0, 0))
        settingstxtRect = settingstxt.get_rect()
        settingstxtRect.center = ((SCREEN_WIDTH/2-200) + (400/2), ((SCREEN_HEIGHT/4) * 3) + (100/2))

        draw.rect(mainScreen, (0, 0, 255), play1Rect, 50, 10)
        mainScreen.blit(play1txt, (play1txtRect))
        draw.rect(mainScreen, (0, 0,255), play2Rect, 50, 10)
        mainScreen.blit(settingstxt, (settingstxtRect))
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
                settingstxtL = assets.clashFontXL.render("Settings", True, (0, 0, 0))
                settingstxtLRect = settingstxtL.get_rect()
                settingstxtLRect.center = ((SCREEN_WIDTH/2-200) + (400/2), ((SCREEN_HEIGHT/4) * 3) + (100/2))
                button2Hover = True
                buttonH2 = Rect(SCREEN_WIDTH/2-210, (SCREEN_HEIGHT/4) * 3 - 10, 420, 120)
                draw.rect(mainScreen, (0, 0, 255), buttonH2, 60, 10)
                mainScreen.blit(settingstxtL, (settingstxtLRect))
                
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







def gameOverScreen(winner):
    
    return

def settingsScreen():
    settingsScreen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    settingsTitle = assets.clashFontXL.render("Settings", True, (0, 0, 0))
    settingsTitleRect = settingsTitle.get_rect()
    settingsTitleRect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/4)
    changingSettings = True
    while changingSettings:
        for evt in event.get():
            if evt.type == QUIT:
                quit()
            if evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    mainMenu()
                    settings.saveSettings()
                    return
        settingsScreen.fill((255, 255, 255))
        settingsScreen.blit(settingsTitle, (settingsTitleRect))

        
        display.flip()


    # Save settings in file i/o
    return

def instructionsScreen():
    return

def gameOverScreen():
    gameOver = True
    gameOverScreen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    while gameOver:
        for evt in event.get():
            if evt.type == QUIT:
                quit()
            if evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    mainMenu()
                    return
        gameOverScreen.fill((255, 255, 255))

        
        display.flip()
    








mainMenu()





