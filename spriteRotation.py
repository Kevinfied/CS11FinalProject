from pygame import *
from math import *
screen = display.set_mode((800,600))
running = True # need to break outer loop from inner loop
tank = image.load('assets/redTank.png')


def blitRotateCenter(surf, image, center, angle):
    rotated_image = transform.rotate(image, angle)
    rad = radians(angle)
    ogImageCenter = image.get_rect(center = center).center
    offsetToLeft = 10
    tankCenterX = ogImageCenter[0]-offsetToLeft
    tankCenterY = ogImageCenter[1]
    rotatedCenter = (tankCenterX + offsetToLeft * cos(rad), tankCenterY + offsetToLeft * sin(rad))
    
    new_rect = rotated_image.get_rect(center = rotatedCenter)
    surf.blit(rotated_image, new_rect)

ang = 0

myClock = time.Clock()
while running:
    # event.get() returns a list
    for evt in event.get():
        if evt.type == QUIT:
            running = False

    #------------------------
    screen.fill((155,155,155))
    blitRotateCenter(screen, tank, (100,100), ang)
    ang += 1
    ang %= 360
    print('ang', ang)
    #------------------------
    display.flip()
    myClock.tick(30)
quit()
    
