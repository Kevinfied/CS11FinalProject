from pygame import *
from math import *
import assets

init()
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
BLUE = (0,0,255)

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
    
    margin = 0.001
    if 1-margin < trianglesArea/shoelace(points) < 1+margin:
        return True
    else:
        return False

# print(pointInRect(points, [[4,4]]))
# print(points[0:2]+point, points[1:3]+point, points[2:], points[3]+points[0]+point)





joystick.init()
# joysticks = [joystick.Joystick(x) for x in range(joystick.get_count())]



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



def touchingWalls(xmin, xmax, ymin, ymax, points):
    for point in points:
        if point[0]< xmin or point[0] > xmax or point[1] < ymin or point[1] > ymax:
            return True

    return False


class Tank:
    def __init__(self,surf, img, x, y, angle, col, scale, name):
        self.surf = surf
        self.scale = scale
        width = img.get_width()
        height = img.get_height()
        self.img = transform.scale(img, (width*scale, height*scale))
        self.name = name
        
        self.x = x
        self.y = y
        self.angle = angle
        
        self.offsetDown = 4.25 * scale
        self.y = y + self.offsetDown
        self.col = col

        self.angVel = 2*pi/90
        self.mag = 8

        self.bulletVel = 12
        self.bulletRad = 5 * scale
        self.shots = []
        self.loads = loads

        self.tanks = []
    def update(self,forward, back, left, right,shooting):
        
            
        self.movement = [0,0,0]
        if left:
            self.angle += self.angVel
            self.movement[0] = self.angVel
        elif right:
            self.angle -= self.angVel
            self.movement[0] = -self.angVel
        if forward:
            self.x = self.x + self.mag*cos(self.angle  + pi/2) 
            self.y = self.y - self.mag*sin(self.angle  + pi/2) 
            self.movement[1] = self.mag*cos(self.angle  + pi/2)
            self.movement[2] = - self.mag*sin(self.angle  + pi/2)
        elif back:
            self.x = self.x - self.mag*cos(self.angle  + pi/2) 
            self.y = self.y + self.mag*sin(self.angle  + pi/2) 
            self.movement[1] = - self.mag*cos(self.angle  + pi/2)
            self.movement[2] = self.mag*sin(self.angle  + pi/2)
        

        rotated_image = transform.rotate(self.img, degrees(self.angle))
        rotatedCenter = (self.offsetDown * cos(self.angle+pi/2) + self.x,  -self.offsetDown * sin(self.angle + pi/2) + self.y)
        bounding_rect = rotated_image.get_rect(center = rotatedCenter)


        self.surf.blit(rotated_image, bounding_rect)
        self.basePoints = []
        fatPoints = []

        h1 = (21*2**0.5) * self.scale
        h2 = (21**2 + 31**2)**0.5 * self.scale
        crookedAngle  = 0.975386
        theta1 = 0.278300
        theta2 = 0.191184
        theta = [pi/4, 3*pi/4, pi+crookedAngle, 2*pi-crookedAngle] + [pi/2 - theta1, theta1 + pi/2, pi/2 - theta2, pi/2 + theta2]

        
        mh1 = (21**2+6**2)**0.5 * self.scale
        mh2 = (31**2+6**2)**0.5 * self.scale


        for i in range(4):
            if i//2 == 0:
                self.basePoints.append([rotatedCenter[0]+ h1* cos(theta[i] + self.angle), rotatedCenter[1] - h1 * sin(theta[i] + self.angle)])
                fatPoints.append([rotatedCenter[0]+ (h1+self.bulletRad)* cos(theta[i] + self.angle), rotatedCenter[1] - (h1+self.bulletRad) * sin(theta[i] + self.angle)])
            else:
                self.basePoints.append([rotatedCenter[0]+ h2* cos(theta[i] + self.angle), rotatedCenter[1] - h2 * sin(theta[i] + self.angle)])
                fatPoints.append([rotatedCenter[0]+ (h2+self.bulletRad)* cos(theta[i] + self.angle), rotatedCenter[1] - (h2+self.bulletRad) * sin(theta[i] + self.angle)])
        
        
        for i in range(4,8):
            if i//6 == 0:
                self.basePoints.append([rotatedCenter[0] + mh1* cos(theta[i] + self.angle), rotatedCenter[1] - mh1 * sin(theta[i] + self.angle)])
            else:
                self.basePoints.append([rotatedCenter[0] + mh2* cos(theta[i] + self.angle), rotatedCenter[1] - mh2* sin(theta[i] + self.angle)])

        for point in self.basePoints:
            draw.circle(self.surf, self.col, point, 3)
        for point in fatPoints:
            draw.circle(self.surf, self.col, point, 3)
        

        
       # Mr. pants was here
        
        
        draw.circle(self.surf, self.col, (self.x, self.y), 3)
        draw.circle(self.surf, self.col, rotatedCenter, 3) 
        draw.rect(self.surf, self.col, bounding_rect, 2)
        
        

        
        # print(movement)
        if shooting and self.loads != 0:
            mixer.Sound.play(assets.pop)
            muzX, muzY = (fatPoints[0][0]+fatPoints[1][0])/2 + self.bulletRad*cos(self.angle+pi/2), (fatPoints[0][1]+fatPoints[1][1])/2 - self.bulletRad * sin(self.angle +pi/2)
            vx,vy = velComponents(self.angle, self.bulletVel)
            self.shots.append([muzX,muzY,vx,vy,time.get_ticks()])
            self.loads -= 1
        if 0<= time.get_ticks()%5000 <= margin:
            self.loads = loads
        # print(time.get_ticks()%5000)
        for shot in self.shots:
            if shot[X]  <= 0 or shot[X]>=self.surf.get_width():
                shot[VX] = -shot[VX]
                mixer.Sound.play(assets.ping)
            if shot[Y] <= 0 or shot[Y] >= self.surf.get_height():
                shot[VY] = -shot[VY]
                mixer.Sound.play(assets.pong)
            shot[X] += shot[VX]
            shot[Y] += shot[VY]
        for i in range(len(self.shots)):  
            shot = self.shots[i]
            if time.get_ticks() - shot[TIME] >= bulletLife:
                del self.shots[i]
                mixer.Sound.play(assets.shotVanish)
                break
            if 0 <= shot[X] <= self.surf.get_width() and 0 <= shot[Y] <= self.surf.get_height():
                draw.circle(self.surf, self.col, shot[:2], self.bulletRad)
        for tank in self.tanks:
            if tank != self:
                for i in range(len(tank.shots)):  
                    shot = tank.shots[i]
                    if pointInRect(fatPoints, [shot[:2]]):
                        print(tank.name + '  destroyed  ' + self.name)
                        return 'end'
        
# def deathDetect(tanks):
#     for tank in tanks:
#             if tank != self:
#                 for i in range(len(tank.shots)):  
#                     shot = tank.shots[i]
#                     if pointInRect(tank.fatPoints, [shot[:2]]):
#                         print(tank.name + '  destroyed  ' + self.name)
#                         return 'end'

# changed from 5 to 3 and the circle is now in the wrong position. 

                


        




# player1 = Tank(screen, assets.blueBase, 200, screen.get_height()/2, 0, BLACK, 5)
# player2 = Tank(screen, assets.redBase, 800, screen.get_height()/2, 0, BLUE, 5)
# bot = Tank(screen, assets.blackBase, 800, screen.get_height()/2, 0, BLUE, 5)

# def moveTank(surf, image, rad, x, y):
#     rotated_image = transform.rotate(image, degrees(rad))
#     offsetToDown = 13
#     rotatedCenter = (offsetToDown * cos(rad+pi/2) + x,  -offsetToDown * sin(rad + pi/2) + y+offsetToDown)
#     new_rect = rotated_image.get_rect(center = rotatedCenter)
#     surf.blit(rotated_image, new_rect)
#     draw.circle(surf, (0,0,0), (x, y+offsetToDown), 5)





    
