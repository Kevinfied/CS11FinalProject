from pygame import *
from math import *

RED = (255,0,0)
GREEN = (0,255,0)

def shoelace(points):
    downsum, upsum = 0,0
    points.append(points[0])
    
    for i in range(len(points)-1):
        downsum += points[i][0] * points[i+1][1]
        upsum   += points[i+1][0] * points[i][1]
    return 0.5*abs(downsum-upsum)


    



def pointInRect(points, point):
    points.append(points[0])
    trianglesArea = shoelace(points[0:2]+point) + shoelace(points[1:3]+point) + shoelace(points[2:4]+point) +shoelace(points[3:]+point)
    print(trianglesArea)
    print(shoelace(points))
    margin = 0.001
    if 1-margin < trianglesArea/shoelace(points) < 1+margin:
        return True
    else:
        return False

# print(pointInRect(points, [[4,4]]))
# print(points[0:2]+point, points[1:3]+point, points[2:], points[3]+points[0]+point)

def smartRect(x,y,r,spinRad, point):
    points=[]
    
    points.append((x+r*cos(2*pi/6 + spinRad), y- r*sin(2*pi/6 + spinRad)))
    points.append((x+r*cos(2*pi/6 + 2*pi/6 + spinRad), y- r*sin(2*pi/6 + 2*pi/6 + spinRad)))
    points.append((x+r*cos(2*pi/6 + pi + spinRad), y- r*sin(2*pi/6 + pi + spinRad)))
    points.append((x+r*cos(2*pi/6 + 2*pi/6 + pi + spinRad ), y- r*sin(2*pi/6 + 2*pi/6 + pi+ spinRad)))
    if pointInRect(points, point):
        draw.polygon(screen,RED,points)
    else:
        draw.polygon(screen,GREEN,points)
    # draw.circle(screen, RED, points[0], 5)
    # draw.circle(screen, RED, points[1], 5)
    # draw.line(screen, col, points[0], points[1],6)



screen = display.set_mode((800,600))
running = True # need to break outer loop from inner loop


x,y = screen.get_width()/2, screen.get_height()/2
ang = 0
angVel = 2*pi/360
myclock = time.Clock()
while running:
    # event.get() returns a list
    for evt in event.get():
        if evt.type == QUIT:
            running = False

    #------------------------
    mx,my = mouse.get_pos()
    screen.fill((155,155,155))
    smartRect(x,y,50,ang,[[mx,my]])
    ang += angVel
    #------------------------
    display.flip()
    myclock.tick(30)
quit()
    
