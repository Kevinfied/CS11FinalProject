'''
tank.py
Raymond Wu and Kevin Xu

This file contains the class Tank, the only class in this game
Tank class stores the attibutes of each tank character, including things like
tank speed, bullet speed, size, reload time, and number of shots in each load
This file also contains several functions for the class to run and for utility. 
'''


from pygame import *
from math import *
import assets
# assets.py is the file that contains all pictures and sound effects

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
#shoelace is a function that returns the area of a shape given its points in a list format. 
# as the name suggests, it uses the shoelace formula 
# this function is used in pointInRect, the function below for tank death detection


def pointInRect(points, point):
    points.append(points[0])
    
    trianglesArea = shoelace(points[0:2]+point) + shoelace(points[1:3]+point) + shoelace(points[2:4]+point) +shoelace(points[3:]+point)
    
    margin = 0.001
    if 1-margin < trianglesArea/shoelace(points) < 1+margin:
        return True
    else:
        return False

# this function requires a list of points for a non-ortho rectangle (not straight, rotated) and a point. 
# its job is to detect if the point is inside the rectangle
# it checks the sum of areas of the four triangles the point makes with the 4 points of the rectangle,
# using shoelace() defined previously
# and returns True if the point is inside the rectangle
# this function is for checking tank deaths: it checks if the center of any cannon balls is within the tank hitbox



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
# this fuction is used to generate component velocities for tank shots when the heading of the tank is known. 
def velComponents(heading,d):
    return d*cos(heading+pi/2) , -d*sin(heading + pi/2)



# def touchingWalls(xmin, xmax, ymin, ymax, points):
#     for point in points:
#         if point[0]< xmin or point[0] > xmax or point[1] < ymin or point[1] > ymax:
#             return True

#     return False




class Tank:
    def __init__(self,surf, img, x, y, angle, col, scale, name): #self, surface, image, x coordinate, y coordinate, angle, color, scale, name
        self.surf = surf
        self.scale = scale
        width = img.get_width()
        height = img.get_height()
        self.img = transform.scale(img, (width*scale, height*scale)) # scale scales the tank
        self.name = name
        
        self.x = x
        self.y = y
        self.angle = angle
        
        self.offsetDown = 4.25 * scale  # the offset between the turret center(physics center) and the picture center. Since the tank rotates around its center of base
        self.y = y + self.offsetDown  # self.y is the y coord of the physics center of tank 
        self.col = col

        self.angVel = 2*pi/90 # angular velocity of tank
        self.mag = 6          # linear velocity of tank (magnitude)

        self.bulletVel = 6.5  # bullet velocity
        self.bulletRad = 5 * scale  #bulletRadius
        self.shots = []       # the list of bullets by this tank
        self.loads = loads    # the number of shots for each reload
        
    def update(self,forward, back, left, right,shooting): # update is running periodically for players to control the tanks
        # foreard, back, left, right and shooting are key bindings

        self.movement = [0,0,0] # movement of this frame: angular change, change in x, change in y
        if left:
            self.angle += self.angVel
            self.movement[0] = self.angVel # record movement if it happened
        elif right:
            self.angle -= self.angVel
            self.movement[0] = -self.angVel
        if forward:
            self.x = self.x + self.mag*cos(self.angle  + pi/2) # some trigonometry for an authentic tank drive
            self.y = self.y - self.mag*sin(self.angle  + pi/2) 
            self.movement[1] = self.mag*cos(self.angle  + pi/2)
            self.movement[2] = - self.mag*sin(self.angle  + pi/2)
        elif back:
            self.x = self.x - self.mag*cos(self.angle  + pi/2) 
            self.y = self.y + self.mag*sin(self.angle  + pi/2) 
            self.movement[1] = - self.mag*cos(self.angle  + pi/2)
            self.movement[2] = self.mag*sin(self.angle  + pi/2)
        

        rotated_image = transform.rotate(self.img, degrees(self.angle)) # rotates the tank image based on angle
        rotatedCenter = (self.offsetDown * cos(self.angle+pi/2) + self.x,  -self.offsetDown * sin(self.angle + pi/2) + self.y) # rotated image center calculated with trig
        bounding_rect = rotated_image.get_rect(center = rotatedCenter)  # bounding rect
        self.small_rect = bounding_rect.scale_by(0.5,0.5)  # half scaled bounding rect is used for tank-wall collision
        self.small_rect.center = (self.x, self.y)          # centered at the physics center of tank

        self.surf.blit(rotated_image, bounding_rect)       # blit the rotated tank with bounding rect centered at rotated center for realistic rotation physics
        self.basePoints = [] # the 8 key points that defines the tank shape (big rect plus small rect on top)
        self.fatPoints = []  # the four points used for death detection

        h1 = (21*2**0.5) * self.scale
        h2 = (21**2 + 31**2)**0.5 * self.scale
        crookedAngle  = 0.975386
        theta1 = 0.278300
        theta2 = 0.191184
        theta = [pi/4, 3*pi/4, pi+crookedAngle, 2*pi-crookedAngle] + [pi/2 - theta1, theta1 + pi/2, pi/2 - theta2, pi/2 + theta2]

        
        mh1 = (21**2+6**2)**0.5 * self.scale
        mh2 = (31**2+6**2)**0.5 * self.scale
        # the math data to make basePoints an fatPoints: angles and hypotenuse lengths
        # the points are made using polar form

        for i in range(4):
            if i//2 == 0:
                self.basePoints.append([rotatedCenter[0]+ h1* cos(theta[i] + self.angle), rotatedCenter[1] - h1 * sin(theta[i] + self.angle)])
                self.fatPoints.append([rotatedCenter[0]+ (h1+self.bulletRad)* cos(theta[i] + self.angle), rotatedCenter[1] - (h1+self.bulletRad) * sin(theta[i] + self.angle)])
            else:
                self.basePoints.append([rotatedCenter[0]+ h2* cos(theta[i] + self.angle), rotatedCenter[1] - h2 * sin(theta[i] + self.angle)])
                self.fatPoints.append([rotatedCenter[0]+ (h2+self.bulletRad)* cos(theta[i] + self.angle), rotatedCenter[1] - (h2+self.bulletRad) * sin(theta[i] + self.angle)])
        
        
        for i in range(4,8):
            if i//6 == 0:
                self.basePoints.append([rotatedCenter[0] + mh1* cos(theta[i] + self.angle), rotatedCenter[1] - mh1 * sin(theta[i] + self.angle)])
            else:
                self.basePoints.append([rotatedCenter[0] + mh2* cos(theta[i] + self.angle), rotatedCenter[1] - mh2* sin(theta[i] + self.angle)])
        #the four points that defines the muzzle shape


        if shooting and self.loads != 0: # if shooting key pressed and there are still shots
            mixer.Sound.play(assets.pop)
            muzX, muzY = (self.fatPoints[0][0]+self.fatPoints[1][0])/2 + self.bulletRad*cos(self.angle+pi/2), (self.fatPoints[0][1]+self.fatPoints[1][1])/2 - self.bulletRad * sin(self.angle +pi/2)
            vx,vy = velComponents(self.angle, self.bulletVel) # the shot starts from the muzzle of the tank
            self.shots.append([muzX,muzY,vx,vy,time.get_ticks()]) # add the shot to the list shots
            self.loads -= 1  # one shot fired, one less remained
        if 0<= time.get_ticks()% reloadPeriod <= margin:  # when it's reload time, refill loads
            self.loads = loads
        for shot in self.shots:
            shot[X] += shot[VX]
            shot[Y] += shot[VY]
        # runs the shots animation
        
        
        


def deathDetect(tanks): # detect if any tanks get shot
    for shooter in tanks:
        for target in tanks:
            if shooter != target:  # for each shooter-target pair
                for i in range(len(shooter.shots)):  
                    shot = shooter.shots[i]
                    if pointInRect(target.fatPoints, [shot[:2]]):   # if any shots from shooter shot target, delete the shot and returns the target for identificatin purpose
                        del shooter.shots[i]
                        # print(shooter.name + '  destroyed  ' + target.name)
                        return target
    
def bulletVanish(tanks):  # vanish bullets when they reach their lifespan
    for ta in tanks:
        for i in range(len(ta.shots)):  # for each shot in each tank
                shot = ta.shots[i]
                if time.get_ticks() - shot[TIME] >= bulletLife:  # if the bullet lived long enough, it will receive its fate of being deleted
                    del ta.shots[i]
                    mixer.Sound.play(assets.shotVanish)  # plays the shot Vanish sound
                    break                                  # breaks from the loop so the loop doesn't break
                if 0 <= shot[X] <= ta.surf.get_width() and 0 <= shot[Y] <= ta.surf.get_height(): # only draws the shot if it's within visible window. not necessary though (legacy feature)
                    draw.circle(ta.surf, ta.col, shot[:2], ta.bulletRad)


