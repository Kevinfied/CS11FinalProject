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


joystick.init()
# joysticks = [joystick.Joystick(x) for x in range(joystick.get_count())]
screen = display.set_mode((1024,768))
HEIGHT = screen.get_height()
WIDTH = screen.get_width()
BLACK = (0,0,0)
BLUE = (0,0,255)
bulletVel = 12 
bulletLife = 6000 #bullet lives for 6000 miliseconds/6sec
reloadPeriod = 5000 #reload time 
loads = 5 # 5 shots per reload
margin = 50 # to account for the rough resolution of get_ticks()
X = 0 
Y = 1
VX = 2
VY = 3
TIME = 4  # these are indices for the sublists in 2d list shots. each sublist is in the format of [X,Y,VX,VY,TIME]
redTank = image.load('assets/redTankNorm.png')

# returns the velocity components (x and y), given a direction and magnitude (heading and  d)
def velComponents(heading,d):
    return d*cos(heading+pi/2) , -d*sin(heading + pi/2)

class Tank:
    def __init__(self,surf, img, x, y, angle, col, scale):
        self.surf = surf
        self.scale = scale
        width = img.get_width()
        height = img.get_height()
        self.img = transform.scale(img, (width*scale, height*scale))
        
        
        self.x = x
        self.y = y
        self.angle = angle
        
        self.offsetDown = 4.25 * scale
        self.y = y + self.offsetDown
        self.col = col

        self.angVel = 2*pi/40
        self.mag = 10

        self.bulletVel = 11
        self.shots = []
        self.loads = loads
    def update(self,forward, back, left, right,shooting):
        
            

        if left:
            self.angle += self.angVel
        elif right:
            self.angle -= self.angVel
        
        if forward:
            self.x = (self.x + self.mag*cos(self.angle  + pi/2) + WIDTH) % WIDTH
            self.y = (self.y - self.mag*sin(self.angle  + pi/2) + HEIGHT) % HEIGHT
        elif back:
            self.x = (self.x - self.mag*cos(self.angle  + pi/2) + WIDTH) % WIDTH
            self.y = (self.y + self.mag*sin(self.angle  + pi/2) + HEIGHT) % HEIGHT

        rotated_image = transform.rotate(self.img, degrees(self.angle))
        rotatedCenter = (self.offsetDown * cos(self.angle+pi/2) + self.x,  -self.offsetDown * sin(self.angle + pi/2) + self.y)
        new_rect = rotated_image.get_rect(center = rotatedCenter)


        self.surf.blit(rotated_image, new_rect)
        basePoints = []
        h1 = 31.8276 * self.scale
        h2 = 37.20215048 * self.scale
        theta1, theta2, theta3, theta4= 0.8076, 2.3339, 4.0796, 5.3451
        basePoints.append([self.x+ h1*cos(theta1+self.angle),self.y - h2* sin(theta1+self.angle)])
        draw.circle(self.surf, self.col, basePoints[0],10, 2)

       # Mr. pants was here
        
        
        draw.circle(self.surf, self.col, (self.x, self.y), 1)
        draw.rect(self.surf, self.col, new_rect, 2)
        
        if shooting and self.loads != 0:
            muzX, muzY = rotatedCenter[:2]
            vx,vy = velComponents(self.angle, bulletVel)
            self.shots.append([muzX,muzY,vx,vy,time.get_ticks()])
            self.loads -= 1
        if 0<= time.get_ticks()%5000 <= margin:
            print('reloaded')
            self.loads = loads
        # print(time.get_ticks()%5000)
        for shot in self.shots:
            if shot[X]  <= 0 or shot[X]>=screen.get_width():
                shot[VX] = -shot[VX]
            if shot[Y] <= 0 or shot[Y] >= screen.get_height():
                shot[VY] = -shot[VY]

            shot[X] += shot[VX]
            shot[Y] += shot[VY]
        for i in range(len(self.shots)):  
            shot = self.shots[i]
            if time.get_ticks() - shot[TIME] >= bulletLife:
                del self.shots[i]
                break
            if 0 <= shot[X] <= screen.get_width() and 0 <= shot[Y] <= screen.get_height():
                draw.circle(screen, self.col, shot[:2], 5)
                


        

tankLeft = Tank(screen, redTank, 200, screen.get_height()/2, 0, BLACK, 5)
tankRight = Tank(screen, redTank, 800, screen.get_height()/2, 0, BLUE, 0.1)
tankRight.mag = 18




def moveTank(surf, image, rad, x, y):
    rotated_image = transform.rotate(image, degrees(rad))
    offsetToDown = 13
    rotatedCenter = (offsetToDown * cos(rad+pi/2) + x,  -offsetToDown * sin(rad + pi/2) + y+offsetToDown)
    new_rect = rotated_image.get_rect(center = rotatedCenter)
    surf.blit(rotated_image, new_rect)
    draw.circle(surf, (0,0,0), (x, y+offsetToDown), 5)


def collision(tank, obj):
    smartRect(obj.x, obj.y, obj.r, obj.spinRad, (tank.x, tank.y))



    
