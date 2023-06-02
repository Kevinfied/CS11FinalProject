import pygame
import assets
import tank
import os

pygame.init()

mainRunning = True
SCREEN_WIDTH = 1180
SCREEN_HEIGHT = 768

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("ICS3U FSE")
pygame.display.set_icon(assets.blueBase)


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

    screen.fill((155,155,155))
    tank.tankLeft.update(keyArray[pygame.K_w],keyArray[pygame.K_s],keyArray[pygame.K_a],keyArray[pygame.K_d],leftShoot)
    tank.tankRight.update(keyArray[pygame.K_UP],keyArray[pygame.K_DOWN],keyArray[pygame.K_LEFT],keyArray[pygame.K_RIGHT], rightShoot)



    pygame.display.flip()
    pygame.time.Clock().tick(60)
 
pygame.quit()
quit()

