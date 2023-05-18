from pygame import *
from math import *
screen = display.set_mode((800,600))
running = True # need to break outer loop from inner loop
GREEN = (0,255,0)
RED = (255,0,0)
BLACK = (0,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
def grid(color,x,y,width,height,spacing):
    BLACK = (0,0,0)
    draw.rect(screen,BLACK,(x,y,width,height))
    i=0
    while spacing*i <= width:
        draw.line(screen,color,(x+spacing*i,y), (x+spacing*i,y+height) )
        i+=1
    j=0
    while spacing*j <= height:
        draw.line(screen,color,(x,y+spacing*j), (x+width,y+spacing*j))
        j+=1

def drawStar(x,y,r,color,spinRad):
    allPoints=[] # the list for all coordinates
    innerR = r*(sin(radians(18))/sin(radians(126))) #inner radius for a perfect star
    for k in range(0,5):  # add a outer vertice followed by an inner vertice each time. 
        allPoints.append( ( x+ r*cos(  k*(2*pi/5)   + pi/2  +  spinRad)  ,  y - r*sin(2*pi*k/5 + pi/2+   spinRad)  ) ) 
        allPoints.append( ( x+ innerR*cos(2*pi*k/5 + pi/5 + pi/2 +   spinRad)  ,  y - innerR*sin(2*pi*k/5 + pi/5 + pi/2+   spinRad)  ))
    draw.polygon(screen,color, allPoints) # draw the polygon



def drawClock(hour,minute,second):
    GREEN = (0,255,0)
    RED = (255,0,0)
    BLACK = (0,0,0)
    BLUE = (0,0,255)
    WHITE = (255,255,255)
    screen.fill(WHITE)
    x=400;y=300 # coordinates for the colock center
    hour=hour%12 
    minute=minute%60
    second=second%60
    hourRadian = -2*pi*(hour+(minute+second/60)/60)/12  + pi/2
    minuteRadian = -2*pi*(minute+second/60)/60  + pi/2
    secondRadian = -2*pi*second/60  + pi/2
    draw.circle(screen,BLACK,(x,y),100,2)
    tickPoints=[]
    for k in range(12):
        tickPoints.append([(x+80*cos(k*pi/6) , y+80*sin(k*pi/6)),(x+92*cos(k*pi/6) , y+92*sin(k*pi/6))])
        draw.line(screen, BLACK, (x+80*cos(k*pi/6) , y+80*sin(k*pi/6)), (x+92*cos(k*pi/6) , y+92*sin(k*pi/6)),4)
    hHand=65;hCounter=25
    mHand=83;mCounter=35
    sHand=90;sCounter=40
    draw.line(screen,BLACK, (x+hHand*cos(hourRadian), y-hHand*sin(hourRadian)), (x+hCounter*cos(hourRadian-pi), y-hCounter*sin(hourRadian-pi)),6)
    draw.line(screen,BLUE, (x+mHand*cos(minuteRadian), y-mHand*sin(minuteRadian)), (x+mCounter*cos(minuteRadian-pi), y-mCounter*sin(minuteRadian-pi)),2)
    draw.line(screen,GREEN, (x+sHand*cos(secondRadian), y-sHand*sin(secondRadian)), (x+sCounter*cos(secondRadian-pi), y-sCounter*sin(secondRadian-pi)),1)


def drawRect(x,y,r,color,spinRad):
    points=[]
    RED = (255,0,0)
    points.append((x+r*cos(2*pi/6 + spinRad), y- r*sin(2*pi/6 + spinRad)))
    points.append((x+r*cos(2*pi/6 + 2*pi/6 + spinRad), y- r*sin(2*pi/6 + 2*pi/6 + spinRad)))
    points.append((x+r*cos(2*pi/6 + pi + spinRad), y- r*sin(2*pi/6 + pi + spinRad)))
    points.append((x+r*cos(2*pi/6 + 2*pi/6 + pi + spinRad ), y- r*sin(2*pi/6 + 2*pi/6 + pi+ spinRad)))
    draw.polygon(screen,color,points)
    # draw.circle(screen, RED, points[0], 5)
    # draw.circle(screen, RED, points[1], 5)
    draw.line(screen, RED, points[0], points[1],6)



ang = 0
spin = 0
x = screen.get_width()/2
y = screen.get_height()/2
mag = 5
angVel = 2*pi/90

def screenEdgeTeleport(x,y):
    xEdge = screen.get_width()
    yEdge = screen.get_height()

while running:
    # event.get() returns a list
    FORWARD,BACK,LEFT,RIGHT = False,False,False,False
    for evt in event.get():
        if evt.type == QUIT:
            running = False
    keyArray = key.get_pressed() 
    
    if keyArray[K_UP]:
        FORWARD = True
    if keyArray[K_DOWN]:
        BACK = True
    if keyArray[K_LEFT]:
        LEFT = True
    if keyArray[K_RIGHT]:
        RIGHT = True
    
    #------------------------
    # x = 400 + 100*cos(radians(ang))
    # y = 300 + 100*sin(radians(ang))
    # ang +=1
    screen.fill((0,0,0))
    drawRect(x,y,50,GREEN,spin)
    # drawStar(x,y,100,GREEN,spin)
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

    # drawClock(12,15,30)
    #------------------------
    time.delay(10)
    display.flip()


quit()
    
