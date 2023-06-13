import pygame
import assets
import tank
import os
import level
import random
from math import *

pygame.init()
# pygame.mixer.Sound(assets.deathExplosion)

mainRunning = True
SCREEN_WIDTH = 1180
SCREEN_HEIGHT = 768
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREY = (155,155,155)
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("ICS3U FSE")
pygame.display.set_icon(assets.blueBase)

wallwidth = 20
space = pygame.Rect(wallwidth,wallwidth,SCREEN_WIDTH-2*wallwidth, SCREEN_HEIGHT-2*wallwidth)
xmin = wallwidth
xmax = SCREEN_WIDTH- wallwidth
ymin = wallwidth
ymax = SCREEN_HEIGHT - wallwidth

tankLeft = tank.Tank(screen, assets.redBase, 200, screen.get_height()/2, 0, RED, 1, 'player1')
tankRight = tank.Tank(screen, assets.blackBase, 800, screen.get_height()/2, 0, BLACK, 1, 'player2')
dummy = tank.Tank(screen, assets.blueBase, 500, screen.get_height()/2, 0, BLUE, 3, 'dummy')
dummy.angVel = 2*pi/180; dummy.mag = 4; dummy.bulletVel = 8; dummy.reloadPeriod = 5000

Tanks = [tankLeft, tankRight,dummy]

# Tanks = [tank.tankLeft, tank.tankRight]
lis = [0 for i in range(50)] + [1]


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

    keyArray = pygame.key.get_pressed()

    screen.fill(BLACK)
    pygame.draw.rect(screen, GREY, space)
    # for map in level.map1:
    #     pygame.draw.rect(screen, (0,0,0), map)

    # for point in tank.tankLeft.basePoints:
    #     if point[0] < xmin or point[0]> xmax or :

    # print(keyArray[pygame.K_w],keyArray[pygame.K_s],keyArray[pygame.K_a],keyArray[pygame.K_d],leftShoot,"      ", keyArray[pygame.K_UP],keyArray[pygame.K_DOWN],keyArray[pygame.K_LEFT],keyArray[pygame.K_RIGHT], rightShoot)
    tankLeft.update(keyArray[pygame.K_w],keyArray[pygame.K_s],keyArray[pygame.K_a],keyArray[pygame.K_d],leftShoot) 
    tankRight.update(keyArray[pygame.K_UP],keyArray[pygame.K_DOWN],keyArray[pygame.K_LEFT],keyArray[pygame.K_RIGHT], rightShoot)


    dummy.update(0, 0, 0, 1, random.choice(lis))
    deadone = tank.deathDetect(Tanks)
    if deadone:
        pygame.mixer.Sound.play(assets.deathExplosion)
        for i in range(8):
            screen.blit(assets.explosions[i], [deadone.x, deadone.y])
            pygame.time.delay(50)
            pygame.display.flip()
        pygame.time.delay(3000)
        mainRunning = False

    for ta in Tanks:
        if tank.touchingWalls(xmin,xmax, ymin, ymax, ta.basePoints):
            ta.angle -= ta.movement[0]
            ta.x     -= ta.movement[1]
            ta.y     -= ta.movement[2]
    

    pygame.display.flip()
    pygame.time.Clock().tick(50)
 
pygame.quit()
quit()

