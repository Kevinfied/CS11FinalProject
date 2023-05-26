from pygame import *


rect1 = Rect(100,100,10,10)
rect2 = Rect(200,200,100,100)

screen = display.set_mode((800,600))

running = True
while running:
    for evt in event.get():
        if evt.type == QUIT:
            running = False
    mb = mouse.get_pressed()
    mx,my = mouse.get_pos()
    if mb[0] == 1:
        rect1.center = (mx,my)
    if mb[2] == 1:
        rect2.center = (mx,my)
    screen.fill((255,255,255))
    draw.circle(screen,(0,0,0),rect1.center,5)
    draw.rect(screen,(255,0,0),rect2)
    if rect1.colliderect(rect2):
        print(True)
    else:
        print(False)
    display.flip()

