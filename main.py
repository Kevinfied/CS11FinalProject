import pygame
import assets
import tank
import os
import level
import random
from math import *
from random import *
# import gui

pygame.init()
# pygame.mixer.Sound(assets.deathExplosion)





mainRunning = True
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREY = (155,155,155)
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("ICS3U FSE")
pygame.display.set_icon(assets.blueBase)






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
            if (y == 0 or y == height): 
                horizontalLines[-1].append([x*gridSize, y*gridSize, (x+1)*gridSize, y*gridSize, 1]) #1
                
                if (x == 0 or x == width) and y != height:
                    verticalLines[-1].append([x*gridSize, y*gridSize, x*gridSize, (y+1)*gridSize, 1]) #1
                else:
                    verticalLines[-1].append([x*gridSize, y*gridSize, x*gridSize, (y+1)*gridSize, choice(possibility)]) #choi
            elif (x == 0 or x == width):
                verticalLines[-1].append([x*gridSize, y*gridSize, x*gridSize, (y+1)*gridSize, 1]) #1
                
                
                horizontalLines[-1].append([x*gridSize, y*gridSize, (x+1)*gridSize, y*gridSize, choice(possibility)]) #choi
            else:
                horizontalLines[-1].append([x*gridSize, y*gridSize, (x+1)*gridSize, y*gridSize, choice(possibility)])
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
                pygame.draw.line(screen, BLACK, (horizontalLines[y][x][0], horizontalLines[y][x][1]), (horizontalLines[y][x][2], horizontalLines[y][x][3]),thickness)
            if verticalLines[y][x][4]:
                pygame.draw.line(screen, BLACK, (verticalLines[y][x][0],   verticalLines[y][x][1]),   (verticalLines[y][x][2], verticalLines[y][x][3]),thickness)  


def within(min, val, ma):
    if min <= val and val <= ma:
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
                    
                    if horizontalLines[y][x][4] and ifInsideBox(x1, x2, ycoord-thickness/2, ycoord+thickness/2, ta.basePoints):
                            print('touching')
                            undoMotion(ta)
                    if verticalLines[y][x][4] and ifInsideBox(xcoord-thickness/2, xcoord+thickness/2, y1, y2, ta.basePoints):
                            print('touching')
                            undoMotion(ta)

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

def undoMotion(ta):
    ta.angle -= ta.movement[0]
    ta.x     -= ta.movement[1]
    ta.y     -= ta.movement[2]

tankLeft = tank.Tank(screen, assets.redBase, 200, screen.get_height()/2, 0, RED, 1, 'player1')
tankRight = tank.Tank(screen, assets.blackBase, 800, screen.get_height()/2, 0, BLACK, 1, 'player2')
dummy = tank.Tank(screen, assets.blueBase, 500, screen.get_height()/2, 0, BLUE, 3, 'dummy')
dummy.angVel = 2*pi/180; dummy.mag = 4; dummy.bulletVel = 8; dummy.reloadPeriod = 5000

Tanks = [tankLeft, tankRight,dummy]
del Tanks[2]
# Tanks = [tank.tankLeft, tank.tankRight]

gridGen()
while mainRunning:
    rightShoot,leftShoot = False, False
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            mainRunning = False
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_c:
                leftShoot = True
            if evt.key == pygame.K_SLASH:
                rightShoot = True
        if evt.type == pygame.MOUSEBUTTONDOWN:
            horizontalLines = []
            verticalLines   = []
            gridGen()

    keyArray = pygame.key.get_pressed()

    screen.fill(GREY)
    # pygame.draw.rect(screen, GREY, space)
    # for map in level.map1:
    #     pygame.draw.rect(screen, (0,0,0), map)



    # print(keyArray[pygame.K_w],keyArray[pygame.K_s],keyArray[pygame.K_a],keyArray[pygame.K_d],leftShoot,"      ", keyArray[pygame.K_UP],keyArray[pygame.K_DOWN],keyArray[pygame.K_LEFT],keyArray[pygame.K_RIGHT], rightShoot)
    tankLeft.update(keyArray[pygame.K_w],keyArray[pygame.K_s],keyArray[pygame.K_a],keyArray[pygame.K_d],leftShoot) 
    tankRight.update(keyArray[pygame.K_UP],keyArray[pygame.K_DOWN],keyArray[pygame.K_LEFT],keyArray[pygame.K_RIGHT], rightShoot)
    if len(Tanks) == 3:
        dummy.update(0, 0, 0, 1, 0)


    deadone = tank.deathDetect(Tanks)
    deadone = None
    if deadone:
        pygame.mixer.Sound.play(assets.deathExplosion)
        _ = screen.copy()
        for i in range(8):
            screen.blit(_, (0,0))
            assets.explosions[i] = pygame.transform.scale(assets.explosions[i], (deadone.scale*100, deadone.scale*100))
            heherect = assets.explosions[i].get_rect(center = (deadone.x, deadone.y))
            screen.blit(assets.explosions[i], heherect)
            pygame.time.delay(100)
            pygame.display.flip()
        pygame.time.delay(3000)
        mainRunning = False

    # for ta in Tanks:
    #     if tank.touchingWalls(xmin,xmax, ymin, ymax, ta.basePoints):
    #         # ta.angle -= ta.movement[0]
    #         # ta.x     -= ta.movement[1]
    #         # ta.y     -= ta.movement[2]
    #         undoMotion(ta)
    ifHitWalls()
    

    gridDraw()
    pygame.display.flip()
    pygame.time.Clock().tick(50)
    # print('fdslkjfdslkjdfsa')

pygame.quit()
quit()

