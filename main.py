"""
main.py
Kevin Xu and Raymond Wu

This is the main file for our project. It contains the main loop, the major functions.
Main loop is at the bottom of the file.
"""

from pygame import *
from math import *
from random import *

# Import from other files
import assets
import tank
import settings


# Initialize pygame
init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700 + 80
screen = display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
display.set_caption("Tank Trouble")
display.set_icon(assets.blueBase)
gameScreenHeight = 700
# The flag for the main loop
mainRunning = True

# Current mode
mode = 'menu' # this is the most important flag of the whole game. it determines which page we are on and therefore which event loop we are running

# Pre-initialized colors
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREY = (155,155,155)
WHITE = (255,255,255)




#map stuff
gridSize = 100   # grid unit
horizontalLines = []  # horizontal walls
verticalLines   = []  #vertical ones
possibility = [ 0 for i in range(8)]+ [1]  # possibility to generate a wall in an empty slot
width = SCREEN_WIDTH//gridSize  # width and height of the grid in terms of a grid unit
height = gameScreenHeight//gridSize
thickness = 10  # wall thickness

leftScore = rightScore = 0  # scores for tanks. we have to make them global


def gridGen(): # grid generation
    mixer.Sound.play(assets.PUappear)   # plays a sound, empties the lists
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

        # this chunk of code ensures there are always walls around the sides of the window, and the rest of walls are randomly generated. 


    # horizontalLines.append([])
   
    # verticalLines.append([])
    # horizontalLines[-1].append([2*gridSize, 2*gridSize, 3*gridSize, 2*gridSize, 1])
    # horizontalLines[-1].append([2*gridSize, 2*gridSize, 3*gridSize, 2*gridSize, 0])
    # verticalLines[-1].append([2*gridSize, 2*gridSize, 2*gridSize, 3*gridSize, 1])
    # verticalLines[-1].append([2*gridSize, 2*gridSize, 2*gridSize, 3*gridSize, 1])
        
    # debugging code. the big bug was solved Thursday. 


# loops through the wall lists, and draw them when there are actual walls. (index 4, or the last element in each 'wall', decides if there is a wall or not. )
def gridDraw():
    for y in range(len(horizontalLines)):
        for x in range(len(horizontalLines[y])):
            if horizontalLines[y][x][4]:
                draw.line(screen, BLACK, (horizontalLines[y][x][0], horizontalLines[y][x][1]), (horizontalLines[y][x][2], horizontalLines[y][x][3]),thickness)
            if verticalLines[y][x][4]:
                draw.line(screen, BLACK, (verticalLines[y][x][0],   verticalLines[y][x][1]),   (verticalLines[y][x][2], verticalLines[y][x][3]),thickness)  


# simple function that checks if a value is within a min and max range
def within(min, val, ma):
    if min <= val and val <= ma:
        return True
    return False

# check if a list of points are outside a box
def ifOutsideBox(xmin, xmax, ymin, ymax, points):
    for point in points:
        if point[0]< xmin or point[0] > xmax or point[1] < ymin or point[1] > ymax:
            return True
    return False

# check if a list of points are inside a box
def ifInsideBox(xmin, xmax, ymin, ymax, points):
    for point in points:
        if point[0]>= xmin and point[0] <= xmax and point[1] >= ymin and point[1] <= ymax:
            return True
    return False

# huge function that runs all bullet bouncing and tank-wall collision
def ifHitWalls(): 
    for y in range(len(horizontalLines)): 
        for x in range(len(horizontalLines[y])): 
            for ta in Tanks:
                if horizontalLines[y][x][4] or verticalLines[y][x][4]: # if valid walls present
                    
                    x1 = horizontalLines[y][x][0]; x2 = horizontalLines[y][x][2]; ycoord = horizontalLines[y][x][1]
                    xcoord = verticalLines[y][x][0]; y1 = verticalLines[y][x][1]; y2 = verticalLines[y][x][3]
            
                
                    for shot in ta.shots:
                        
                        if horizontalLines[y][x][4]:  # bounce all bullets
                            if within(ycoord - thickness/2 - ta.bulletRad, shot[tank.Y] , ycoord + thickness/2 + ta.bulletRad) and within(x1, shot[tank.X], x2):
                        
                                shot[tank.VY] = -shot[tank.VY]
                                mixer.Sound.play(assets.pong)
                            elif within(ycoord - thickness/2, shot[tank.Y], ycoord + thickness/2) and within(x1 - ta.bulletRad, shot[tank.X], x2 + ta.bulletRad):
                            
                                shot[tank.VX] = -shot[tank.VX]
                                mixer.Sound.play(assets.ping)
                            
                        if verticalLines[y][x][4]:
                            if within(xcoord - thickness/2 - ta.bulletRad, shot[tank.X], xcoord + thickness/2 + ta.bulletRad) and within(y1, shot[tank.Y], y2):
                            
                                shot[tank.VX] = -shot[tank.VX]
                                mixer.Sound.play(assets.ping)
                        
                            elif within(xcoord - thickness/2, shot[tank.X], xcoord + thickness/2) and within(y1 - ta.bulletRad, shot[tank.Y], y2 + ta.bulletRad):
                            
                                shot[tank.VY] = -shot[tank.VY]
                                mixer.Sound.play(assets.pong)
                    

                    if horizontalLines[y][x][4] and (ifInsideBox(x1, x2, ycoord-thickness/2, ycoord+thickness/2, ta.basePoints) or ta.small_rect.colliderect((x1, ycoord-thickness/2, x2-x1, thickness))):
                            
                            undoMotion(ta) #no box points in the tank
                            
                    if verticalLines[y][x][4] and (ifInsideBox(xcoord-thickness/2, xcoord+thickness/2, y1, y2, ta.basePoints) or ta.small_rect.colliderect((xcoord-thickness/2, y1, thickness, y2-y1))):
                            
                            undoMotion(ta)
                    # tank collision: undo the motion of last frame if there is any collision. so you can't plow through walls


# simple functin to undo the motion of a tank
def undoMotion(ta):
    ta.angle -= ta.movement[0]
    ta.x     -= ta.movement[1]
    ta.y     -= ta.movement[2]

tankLeft = tank.Tank(screen, assets.redBase, 200, gameScreenHeight/2, 0, RED, 1, 'player1') # red tank initialized
tankRight = tank.Tank(screen, assets.blackBase, 800, gameScreenHeight/2, 0, BLACK, 1, 'player2')  # blue tank initialized
dummy = tank.Tank(screen, assets.blueBase, 500, gameScreenHeight/2, 0, BLUE, 3, 'dummy')   # dummy tank isn't even used because we ran out of time.
dummy.angVel = 2*pi/180; dummy.mag = 4; dummy.bulletVel = 8; dummy.reloadPeriod = 5000  # dummy tank is supposed to be AI

Tanks = [tankLeft, tankRight,dummy]
del Tanks[2]
# Tanks = [tank.tankLeft, tank.tankRight]


# resets the angle, coordinates and shots of tanks. 
def tanksReset():
    for ta in Tanks:
        ta.angle = random()*2*pi
        ta.x = horizontalLines[randint(0,height-1)][randint(0,width-1)][0]+50
        ta.y = horizontalLines[randint(0,height-1)][randint(0,width-1)][1]+50
        ta.shots = []

# draws the score board based on scores for left and right tank, and also the win threshold
def drawScoreBoard(scorel, scorer, winScore):
    rectLeft = Rect(0, gameScreenHeight, 100, 80)
    rectRight = Rect(SCREEN_WIDTH-100, gameScreenHeight, 100, 80)
    draw.rect(screen, RED, rectLeft)
    draw.rect(screen, BLACK, rectRight)
    lt = assets.clashFontM.render(str(scorel), True, WHITE )
    rt = assets.clashFontM.render(str(scorer), True, WHITE )
    screen.blit(lt, lt.get_rect(center = rectLeft.center) )
    screen.blit(rt, rt.get_rect(center = rectRight.center) )
    if winScore != 0:
        ct = assets.clashFontL.render('First to '+str(winScore), True, BLACK)
    else:
        ct = assets.clashFontL.render('Infinite Mode', True, BLACK)  # if threshold is 0, it says infinite mode
    screen.blit(ct, ct.get_rect(center = (SCREEN_WIDTH/2, gameScreenHeight + 40)))
    


# 4 Settings that you can change
winScore=0
bulletLoad=0
reloadPeriod=0
bulletLife=0

# function that fetch the setting values from a txt file and updates the 4 global varaibles
def loadSettings():
    set = settings.getSettings()
    global winScore, bulletLoad, reloadPeriod, bulletLife
    winScore, bulletLoad, reloadPeriod, bulletLife = set[0], set[1], set[2], set[3]


# push the settings into tank.py so they take effect
def syncSettings():
    global bulletLoad, reloadPeriod, bulletLife
    loadSettings()
    tank.loads = bulletLoad
    tank.reloadPeriod = reloadPeriod
    tank.bulletLife = bulletLife



# event loop for gameplay
def gameplay():
    global mode
    global leftScore, rightScore
    global winner

    rightShoot,leftShoot = False, False # shooting bools
    for evt in event.get():
        if evt.type == QUIT:
            mode = 'quit'
        if evt.type == KEYDOWN:
            if evt.key == K_c:
                leftShoot = True
            if evt.key == K_SLASH:
                rightShoot = True
            if evt.key == K_ESCAPE:
                mode = 'pause'
            if evt.key == K_BACKSLASH:  # refresh the map when that key's being hit
                gridGen()

    keyArray = key.get_pressed()
    screen.fill(GREY)
    tankLeft.update(keyArray[K_w],keyArray[K_s],keyArray[K_a],keyArray[K_d],leftShoot)   # update the tanks
    tankRight.update(keyArray[K_UP],keyArray[K_DOWN],keyArray[K_LEFT],keyArray[K_RIGHT], rightShoot)
    if len(Tanks) == 3:
        dummy.update(0, 0, 0, 1, 0)

    # print(tank.loads,  tank.reloadPeriod, tank.bulletLife)  # debug
    
    deadone = tank.deathDetect(Tanks)  # if any tank is dead, run the thing below
    if deadone:
        mixer.Sound.play(assets.deathExplosion)
        _ = screen.copy()
        for i in range(8):  # explosion
            screen.blit(_, (0,0))
            assets.explosions[i] = transform.scale(assets.explosions[i], (deadone.scale*100, deadone.scale*100))
            heherect = assets.explosions[i].get_rect(center = (deadone.x, deadone.y))
            screen.blit(assets.explosions[i], heherect)
            time.delay(100)
            display.flip()
        time.delay(1000)
        if deadone == tankLeft:  # update scores
            rightScore += 1
        else:
            leftScore += 1
        if winScore != 0:
            if rightScore == winScore:
                winner = "PLAYER 2"
                mode = 'end'
                
            elif leftScore == winScore:  # check for end game
                winner = "PLAYER 1"
                mode = 'end'

        gridGen()   # reset map and tanks for the next round
        tanksReset()

    
    ifHitWalls()  # runs the huge function
    gridDraw()    # draw grid (walls)
    drawScoreBoard(leftScore, rightScore,winScore)# draw score board
    tank.bulletVanish(Tanks)                        # vanish shots
    display.flip()
    time.Clock().tick(50)
    

# event loop for pause screen
def pausing():
    global mode
    for evt in event.get():
        if evt.type == QUIT:
            mode = 'quit'
        if evt.type == KEYDOWN:
            if evt.key == K_ESCAPE:
                mode = 'game'
            if evt.key == K_m:
                mode = 'menu'


    pauseText = assets.clashFontL.render("Paused", True, RED)
    toMainText = assets.clashFontS.render("press M for main menu", True, WHITE)
    tmtRect = toMainText.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 +50))
    screen.blit(pauseText, (screen.get_width()/2 - pauseText.get_width()/2, screen.get_height()/2 - pauseText.get_height()/2))
    screen.blit(toMainText, tmtRect)
    display.flip()


# The starting menu
def mainMenu():
    global mode
    global leftScore, rightScore

    # The 2 buttons in the main menu
    play1Rect = Rect(SCREEN_WIDTH/2-200, (SCREEN_HEIGHT/4 * 3 )-150, 400, 100)
    settingsRect = Rect(SCREEN_WIDTH/2-200, (SCREEN_HEIGHT/4) * 3, 400, 100)

   
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()
    for evt in event.get():
        if evt.type == QUIT:
            mode = 'quit'
        if evt.type == MOUSEBUTTONDOWN:
            if play1Rect.collidepoint(mx, my):
                # Once the user clicks on the "play" button, it will reset the scores of the tanks
                # and then it will bring the user to the instructions screen
                leftScore = rightScore = 0
                syncSettings() # Applying the current settings
                mixer.Sound.play(assets.pop)
                mode = 'instruction'
                return
            elif    settingsRect.collidepoint(mx, my):
                # Brings the user to the settings page
                mixer.Sound.play(assets.pop)
                mode = 'setting'
                loadSettings() # Loading the current settings
                return
    

    # Loading some assets and drawing them on the screen
    screen.fill((255, 255, 255))
    titleTxt = assets.clashFontTitle.render("Tank Trouble", True, (0, 0, 0))
    titleRect = titleTxt.get_rect()
    titleRect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/4)
    screen.blit(titleTxt, (titleRect))
    play1txt = assets.clashFontL.render("Play", True, (0, 0, 0))
    play1txtRect = play1txt.get_rect()
    play1txtRect.center = ((SCREEN_WIDTH/2-200) + (400/2), ((SCREEN_HEIGHT/4 * 3 )-150) + (100/2))
    settingstxt = assets.clashFontL.render("Settings", True, (0, 0, 0))
    settingstxtRect = settingstxt.get_rect()
    settingstxtRect.center = ((SCREEN_WIDTH/2-200) + (400/2), ((SCREEN_HEIGHT/4) * 3) + (100/2))
    draw.rect(screen, (0, 0, 255), play1Rect, 50, 10)
    screen.blit(play1txt, (play1txtRect))
    draw.rect(screen, (0, 0,255),   settingsRect, 50, 10)
    screen.blit(settingstxt, (settingstxtRect))

    # Button Hover Effect
    # Enlarges the button when user hovers mouse over them. 
    if play1Rect.collidepoint(mx, my):
        if mb[0] == 0:
            play1txtL = assets.clashFontXL.render("Play", True, (0, 0, 0))
            play1txtLRect = play1txtL.get_rect()
            play1txtLRect.center = ((SCREEN_WIDTH/2-200) + (400/2), ((SCREEN_HEIGHT/4 * 3 )-150) + (100/2))
            buttonH1 = Rect(SCREEN_WIDTH/2-210, (SCREEN_HEIGHT/4 * 3 )-160, 420, 120)
            draw.rect(screen, (0, 0, 255), buttonH1, 60, 10)
            screen.blit(play1txtL, (play1txtLRect))
    if  settingsRect.collidepoint(mx, my):
        if mb[0] == 0:
            settingstxtL = assets.clashFontXL.render("Settings", True, (0, 0, 0))
            settingstxtLRect = settingstxtL.get_rect()
            settingstxtLRect.center = ((SCREEN_WIDTH/2-200) + (400/2), ((SCREEN_HEIGHT/4) * 3) + (100/2))
            buttonH2 = Rect(SCREEN_WIDTH/2-210, (SCREEN_HEIGHT/4) * 3 - 10, 420, 120)
            draw.rect(screen, (0, 0, 255), buttonH2, 60, 10)
            screen.blit(settingstxtL, (settingstxtLRect))

    display.flip()








def settingsScreen():
    global mode
    global winScore
    global bulletLoad
    global reloadPeriod
    global bulletLife
    background = transform.scale(assets.settingsBg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # Just loading a bunch of assets and adjusting them
    settingsTitle = assets.clashFontXL.render("SETTINGS" , True, (0, 0, 0))
    settingsTitleRect = settingsTitle.get_rect()
    settingsTitleRect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/8)
    winScoreTxt = assets.clashFontL.render("Win Score", True, (0, 0, 0))
    winScoreTxtRect = winScoreTxt.get_rect()
    winScoreTxtRect.center = (SCREEN_WIDTH/4, SCREEN_HEIGHT/4)
    tankLoadTxt = assets.clashFontL.render("Tank Load", True, (0, 0, 0))
    tankLoadTxtRect = tankLoadTxt.get_rect()
    tankLoadTxtRect.center = (SCREEN_WIDTH/4, SCREEN_HEIGHT/4 + 100)
    reloadPeriodTxt = assets.clashFontL.render("Reload Period", True, (0, 0, 0))
    reloadPeriodTxtRect = reloadPeriodTxt.get_rect()
    reloadPeriodTxtRect.center = (SCREEN_WIDTH/4, SCREEN_HEIGHT/4 + 200)
    bulletLifeTxt = assets.clashFontL.render("Bullet Life", True, (0, 0, 0))
    bulletLifeTxtRect = bulletLifeTxt.get_rect()
    bulletLifeTxtRect.center = (SCREEN_WIDTH/4, SCREEN_HEIGHT/4 + 300)

    increaseButton = transform.scale(assets.arrowRight, (50, 50))
    decreaseButton = transform.scale(assets.arrowLeft, (50, 50))

    # The arrow buttons
    winScoreUp = Rect(SCREEN_WIDTH/2 + 150, SCREEN_HEIGHT/4 - 25, 50, 50)
    winScoreDown = Rect(SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT/4 - 25, 50, 50)
    tankLoadUp = Rect(SCREEN_WIDTH/2 + 150, SCREEN_HEIGHT/4 + 75, 50, 50)
    tankLoadDown = Rect(SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT/4 + 75, 50, 50)
    reloadPeriodUp = Rect(SCREEN_WIDTH/2 + 150, SCREEN_HEIGHT/4 + 175, 50, 50)
    reloadPeriodDown = Rect(SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT/4 + 175, 50, 50)
    bulletLifeUp = Rect(SCREEN_WIDTH/2 + 150, SCREEN_HEIGHT/4 + 275, 50, 50)
    bulletLifeDown = Rect(SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT/4 + 275, 50, 50)

    # The values of the settings
    winScoreVal = assets.clashFontL.render(str(winScore), True, (0, 0, 0))
    winScoreValRect = winScoreVal.get_rect()
    winScoreValRect.center = (SCREEN_WIDTH/2 + 75, SCREEN_HEIGHT/4)
    tankLoadVal = assets.clashFontL.render(str(bulletLoad), True, (0, 0, 0))
    tankLoadValRect = tankLoadVal.get_rect()
    tankLoadValRect.center = (SCREEN_WIDTH/2 + 75, SCREEN_HEIGHT/4 + 100)
    reloadPeriodVal = assets.clashFontL.render(str(reloadPeriod), True, (0, 0, 0))
    reloadPeriodValRect = reloadPeriodVal.get_rect()
    reloadPeriodValRect.center = (SCREEN_WIDTH/2 + 75, SCREEN_HEIGHT/4 + 200)
    bulletLifeVal = assets.clashFontL.render(str(bulletLife), True, (0, 0, 0))
    bulletLifeValRect = bulletLifeVal.get_rect()
    bulletLifeValRect.center = (SCREEN_WIDTH/2 + 75, SCREEN_HEIGHT/4 + 300)
    
    resetRect = Rect(20,20,100,40)
    defaultTxt = assets.clashFontS.render('Default', True, WHITE)
    escTxt = assets.clashFontS.render('esc to go back', True, BLACK)
    bounds = [[0,100],[1,10],[500,10000],[1000,10000]] # defines the min and max of all adjustable values in settings
    mx, my = mouse.get_pos()

    for evt in event.get():
        if evt.type == QUIT:
            settings.saveSettings(winScore, bulletLoad, reloadPeriod, bulletLife) # save settngs to txt file before closing
            mode = 'quit'
        if evt.type == KEYDOWN:
            if evt.key == K_ESCAPE:
                # mainMenu()
                settings.saveSettings(winScore, bulletLoad, reloadPeriod, bulletLife) # save settings when returned to menu
               
                mode = 'menu'
                return
        if evt.type == MOUSEBUTTONDOWN:
            if evt.button == 1:
                # The buttons for the adjusting the settings
                if winScoreUp.collidepoint(mx, my):
                    if winScore+1 <= bounds[0][1]:
                        winScore += 1
                        mixer.Sound.play(assets.pop)  # if adjusment is valid, do it and play pop
                    else:
                        mixer.Sound.play(assets.pong)  # else play pong. same thing for all below
                if winScoreDown.collidepoint(mx, my):
                    if winScore-1 >= bounds[0][0]:
                        winScore -= 1
                        mixer.Sound.play(assets.pop)
                    else:
                        mixer.Sound.play(assets.pong)
                if tankLoadUp.collidepoint(mx, my):
                    if bulletLoad+1 <= bounds[1][1]:
                        bulletLoad += 1
                        mixer.Sound.play(assets.pop)
                    else:
                        mixer.Sound.play(assets.pong)
                if tankLoadDown.collidepoint(mx, my):
                    if bulletLoad-1 >= bounds[1][0]:
                        bulletLoad -= 1
                        mixer.Sound.play(assets.pop)
                    else:
                        mixer.Sound.play(assets.pong)
                if reloadPeriodUp.collidepoint(mx, my):
                    if reloadPeriod+500 <= bounds[2][1]:
                        reloadPeriod += 500
                        mixer.Sound.play(assets.pop)
                    else:
                        mixer.Sound.play(assets.pong)
                if reloadPeriodDown.collidepoint(mx, my):
                    if reloadPeriod-500 >= bounds[2][0]:
                        reloadPeriod -= 500
                        mixer.Sound.play(assets.pop)
                    else:
                        mixer.Sound.play(assets.pong)
                if bulletLifeUp.collidepoint(mx, my):
                    if  bulletLife+1000 <= bounds[3][1]:
                        bulletLife += 1000
                        mixer.Sound.play(assets.pop)
                    else:
                        mixer.Sound.play(assets.pong)
                if bulletLifeDown.collidepoint(mx, my):
                    if bulletLife-1000 >= bounds[3][0]:
                        bulletLife -= 1000  
                        mixer.Sound.play(assets.pop)  
                    else:
                        mixer.Sound.play(assets.pong)
                if resetRect.collidepoint(mx,my):
                    settings.saveDefaultSettings()
                    loadSettings()
                    mixer.Sound.play(assets.pop)

    # Drawing assets on the screen             
    screen.blit(background, (0,0))
    screen.blit(settingsTitle, (settingsTitleRect))
    screen.blit(winScoreTxt, (winScoreTxtRect))
    screen.blit(tankLoadTxt, (tankLoadTxtRect))
    screen.blit(reloadPeriodTxt, (reloadPeriodTxtRect))
    screen.blit(bulletLifeTxt, (bulletLifeTxtRect))
    screen.blit(increaseButton, (winScoreUp))
    screen.blit(decreaseButton, (winScoreDown))
    screen.blit(increaseButton, (tankLoadUp))
    screen.blit(decreaseButton, (tankLoadDown))
    screen.blit(increaseButton, (reloadPeriodUp))
    screen.blit(decreaseButton, (reloadPeriodDown))
    screen.blit(increaseButton, (bulletLifeUp))
    screen.blit(decreaseButton, (bulletLifeDown))
    screen.blit(winScoreVal, (winScoreValRect))
    screen.blit(tankLoadVal, (tankLoadValRect))
    screen.blit(reloadPeriodVal, (reloadPeriodValRect))
    screen.blit(bulletLifeVal, (bulletLifeValRect))
    draw.rect(screen, BLACK, resetRect, False, 9)
    screen.blit(defaultTxt, defaultTxt.get_rect(center = resetRect.center))
    screen.blit(escTxt, (20, gameScreenHeight) )
    
    display.flip()
    # return


# event loop for instruction screen
def instructionsScreen():
    global mode
    keyArray = key.get_pressed()
    buttons = [[],[]]
    
    for evt in event.get():
        if evt.type == QUIT:
            mode = 'quit'
        if evt.type == KEYDOWN:
            if evt.key == K_ESCAPE:
                mode = 'menu'
        
        if keyArray[K_q] and keyArray[K_SLASH]:
            mixer.Sound.play(assets.activated)
            mode = 'game'
    screen.fill(WHITE)
    drawScoreBoard(leftScore, rightScore, winScore)
    valids = [[0,0], [0,1], [0,5], [0,6],[1,0], [1,1], [1,2], [1,5], [1,6], [1,7]] # valid spots for keys
    keyBinds = [keyArray[K_q], keyArray[K_w], keyArray[K_SLASH], keyArray[K_UP], keyArray[K_a], keyArray[K_s], keyArray[K_d], keyArray[K_LEFT], keyArray[K_DOWN], keyArray[K_RIGHT]]
    for y in range(2):
        for x in range(9):
            buttons[y].append(Rect(x*100 + 100, y*100+150, 90,90))
    
    for y in range(2):
        for x in range(9):
            for pair in valids:  # only draw key buttons if they are actual keys
                if y== pair[0] and x == pair[1]:
                    if keyBinds[valids.index(pair)]:
                        draw.rect(screen, GREEN, buttons[y][x], False, 5)  # if key's pressed, draw it green
                    else:
                        draw.rect(screen, GREY, buttons[y][x], False, 5)  # else draw it grey 

    # display texts.
    titleTxt = assets.clashFontXL.render('Controls', True, BLACK)
    shootTxt = assets.clashFontS.render('awsd movement, Q shoot; arrow keys movement, / shoot', True, BLACK)
    proceedTxt = assets.clashFontS.render('Hit Q and / (slash) together to proceed', True, BLACK)
    escTxt = assets.clashFontS.render('Always esc to go back; hit back slash during game to refresh map', True, BLACK)
    screen.blit(escTxt, (20, gameScreenHeight-80) )
    screen.blit(titleTxt, titleTxt.get_rect(center = (SCREEN_WIDTH/2, 100)))
    screen.blit(shootTxt, shootTxt.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/5 * 3)))
    screen.blit(proceedTxt, proceedTxt.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/5 * 3 + 30)))
    display.flip()
    

# simple screen to deliver the message for the winner
def gameOverScreen(winner):
    global mode
    if winner == 'PLAYER 2':
        gameOverTitle = assets.clashFontXL.render(winner + " WINS", True, BLACK)
    else:
        gameOverTitle = assets.clashFontXL.render(winner + " WINS", True, (255, 0, 0))
    gameOverTitleRect = gameOverTitle.get_rect()
    gameOverTitleRect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
   
    for evt in event.get():
        if evt.type == QUIT:
            mode = 'quit'
        if evt.type == KEYDOWN:
            if evt.key == K_ESCAPE:
                mode = 'menu'
                return
    screen.blit(gameOverTitle, (gameOverTitleRect))
    display.flip()
    

# a super short main loop thanks to the use of functions
gridGen()
tanksReset()
while mainRunning:
    if mode == 'menu':
        mainMenu()
    elif mode == 'instruction':
        instructionsScreen()
    elif mode == 'game':
        gameplay()
    elif mode == 'pause':
        pausing()
    elif mode == 'setting':
        settingsScreen()
    elif mode == "end":
        gameOverScreen(winner)
    elif mode == 'quit':
        mainRunning = False
quit()
