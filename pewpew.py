from pygame import *
init()
def similar(x1,y1,x2,y2,d):
    wid = x2-x1
    hei = y2-y1
    hy = max(1,(wid**2 + hei**2) ** 0.5)
    sx = d * wid / hy
    sy = d * hei / hy
    return sx,sy

screen = display.set_mode((1024, 768))
boxx, boxy = 512,384
X = 0
Y = 1
VX = 2
VY = 3
TIME = 4
running = True
myClock = time.Clock()
shots = []
bulletPeriod = 3000


while running:
    
    for evnt in event.get():
        if evnt.type == QUIT:
            running = False
        if evnt.type == MOUSEBUTTONDOWN:
            x,y = evnt.pos
            vx,vy = similar(boxx,boxy,x,y,10)
            shot = [boxx,boxy,vx,vy,time.get_ticks()]
            shots.append(shot)

    for shot in shots:
        if shot[X]  <= 1 or shot[X]>=screen.get_width():
            shot[VX]= -shot[VX]
        if shot[Y] <= 0 or shot[Y] >= screen.get_height():
            shot[VY] = -shot[VY]

        shot[X] += shot[VX]
        shot[Y] += shot[VY]
    screen.fill((0,0,0))
    draw.circle(screen, (255,0,0), (boxx,boxy), 15)
    
    for i in range(len(shots)):  
        # shot[0] = debug(shot[0])
        shot = shots[i]
        if time.get_ticks() - shot[TIME] >= bulletPeriod:
            del shots[i]
            break
        if 0 <= shot[X] <= screen.get_width() and 0 <= shot[Y] <= screen.get_height():
            draw.circle(screen, (255,255,0), shot[:2], 5)
        # else:
        #     del shots[i]
        #     break
        
    print(len(shots))
     
    display.flip()
    
    myClock.tick(60)                        
print(shots)
quit()

