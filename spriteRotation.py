from pygame import *
from math import *
screen = display.set_mode((800,600))
running = True # need to break outer loop from inner loop
tank = image.load('assets/redTank.png')


def moveTank(surf, image, rad, x, y):
    rotated_image = transform.rotate(image, degrees(rad))
    
    ogImageCenter = (x,y)
    offsetToLeft = 13
    tankCenterX = ogImageCenter[0]-offsetToLeft
    tankCenterY = ogImageCenter[1]
    rotatedCenter = (tankCenterX + offsetToLeft * cos(rad) + x, tankCenterY - offsetToLeft * sin(rad) + y)

    new_rect = rotated_image.get_rect(center = rotatedCenter)

    surf.blit(rotated_image, new_rect)
    # draw.circle(surf, (0,0,0), (tankCenterX, tankCenterY), 5)

spin = 0
x = screen.get_width()/2
y = screen.get_height()/2
mag = 5
angVel = 2*pi/90

myClock = time.Clock()
while running:
    FORWARD,BACK,LEFT,RIGHT = False,False,False,False
    for evt in event.get():
        if evt.type == QUIT:
            running = False
    keyArray = key.get_pressed() 
    
    if keyArray[K_UP] or keyArray[K_w]:
        FORWARD = True
    if keyArray[K_DOWN] or keyArray[K_s]:
        BACK = True
    if keyArray[K_LEFT] or keyArray[K_a]:
        LEFT = True
    if keyArray[K_RIGHT] or keyArray[K_d]:
        RIGHT = True

    #------------------------
    screen.fill((155,155,155))
    moveTank(screen, tank, spin,x,y)

    if LEFT:
        spin+= angVel
    elif RIGHT:
        spin-= angVel
    
    if FORWARD:
        x = (x + mag*cos(spin + pi/2) +800) % 800
        y = (y - mag*sin(spin + pi/2) +600) % 600
    elif BACK:
        x = (x - mag*cos(spin + pi/2) +800) % 800
        y = (y + mag*sin(spin + pi/2) +600) % 600


    spin = spin % (2*pi)
    print(f"{spin/pi:.2f}")
    
    
    #------------------------
    display.flip()
    myClock.tick(30)
quit()
    
