from pygame import *
import assets
screen = display.set_mode((800,600))
running = True # need to break outer loop from inner loop

scale = 5 
x, y = assets.redBase.get_width(), assets.redBase.get_height()
bigTank = transform.scale(assets.redBase, (x*scale, y * scale))
print(bigTank.get_rect())
print(bigTank.get_size())
screen.fill((155,155,155))
screen.blit(bigTank, (0,0))
while running:
    # event.get() returns a list
    for evt in event.get():
        if evt.type == QUIT:
            running = False

    #------------------------
    posX, posY = mouse.get_pos()
    print(posX // scale, posY // scale,  bigTank.get_rect().center)
    # print()
    #------------------------
    display.flip()

quit()
    
