from pygame import *

screen = display.set_mode((800,600))
running = True # need to break outer loop from inner loop


tank = image.load('assets/redTank.png')
rectTank = image.load('assets/tankBase.png')
while running:
    # event.get() returns a list
    for evt in event.get():
        if evt.type == QUIT:
            running = False

    #------------------------
    print(tank.get_rect().center)
    print(rectTank.get_rect().center)
    break
    #------------------------
    display.flip()

quit()
    
