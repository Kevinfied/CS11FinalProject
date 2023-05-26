from pygame import *
from math import *
joystick.init()
# joysticks = [joystick.Joystick(x) for x in range(joystick.get_count())]
screen = display.set_mode((1024,768))
HEIGHT = screen.get_height()
WIDTH = screen.get_width()
BLACK = (0,0,0)
BLUE = (0,0,255)
running = True # need to break outer loop from inner loop
redTank = image.load('assets/redTank.png')

class tank:
    def __init__(self,surf, img, x, y, angle, col):
        self.surf = surf
        self.img = img
        self.x = x
        self.y = y
        self.angle = angle
        
        self.offsetDown = 13
        self.col = col

        self.angVel = 2*pi/40
        self.mag = 10
    def update(self,forward, back, left, right):
        self.forward = forward
        self.back = back
        self.left = left
        self.right = right

        if self.left:
            self.angle += self.angVel
        elif self.right:
            self.angle -= self.angVel
        
        if self.forward:
            self.x = (self.x + self.mag*cos(self.angle  + pi/2) + WIDTH) % WIDTH
            self.y = (self.y - self.mag*sin(self.angle  + pi/2) + HEIGHT) % HEIGHT
        elif self.back:
            self.x = (self.x - self.mag*cos(self.angle  + pi/2) + WIDTH) % WIDTH
            self.y = (self.y + self.mag*sin(self.angle  + pi/2) + HEIGHT) % HEIGHT

        rotated_image = transform.rotate(self.img, degrees(self.angle))
        rotatedCenter = (self.offsetDown * cos(self.angle+pi/2) + self.x,  -self.offsetDown * sin(self.angle + pi/2) + self.y+self.offsetDown)
        new_rect = rotated_image.get_rect(center = rotatedCenter)
        self.surf.blit(rotated_image, new_rect)
        draw.circle(self.surf, self.col, (self.x, self.y+self.offsetDown), 10)

tankLeft = tank(screen, redTank, 200, screen.get_height()/2, 0, BLACK)
tankRight = tank(screen, redTank, 800, screen.get_height()/2, 0, BLUE)

class Tank:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
    def move(self, x, y):
        self.x = x
        self.y = y
    def draw(self, surf):
        surf.blit(self.image, (self.x, self.y))


def moveTank(surf, image, rad, x, y):
    rotated_image = transform.rotate(image, degrees(rad))
    
    
    offsetToDown = 13
    rotatedCenter = (offsetToDown * cos(rad+pi/2) + x,  -offsetToDown * sin(rad + pi/2) + y+offsetToDown)
    new_rect = rotated_image.get_rect(center = rotatedCenter)
    surf.blit(rotated_image, new_rect)
    draw.circle(surf, (0,0,0), (x, y+offsetToDown), 5)




# x = screen.get_width()/2
# y = screen.get_height()/2
# self.mag = 10
# angVel = 2*pi/40

myClock = time.Clock()
while running:
    # FORWARD,BACK,LEFT,RIGHT = False,False,False,False
    for evt in event.get():
        if evt.type == QUIT:
            running = False
    keyArray = key.get_pressed()
    # joyHat = joysticks[0].get_hat(0)
    
    # if keyArray[K_UP] or keyArray[K_w]:
    #     FORWARD = True
    # if keyArray[K_DOWN] or keyArray[K_s]:
    #     BACK = True
    # if keyArray[K_LEFT] or keyArray[K_a]:
    #     LEFT = True
    # if keyArray[K_RIGHT] or keyArray[K_d]:
    #     RIGHT = True
    #------------------------
    keyArray[K_UP],keyArray[K_DOWN],keyArray[K_LEFT],keyArray[K_RIGHT]
    screen.fill((155,155,155))
    tankLeft.update(keyArray[K_w],keyArray[K_s],keyArray[K_a],keyArray[K_d])
    tankRight.update(keyArray[K_UP],keyArray[K_DOWN],keyArray[K_LEFT],keyArray[K_RIGHT])

    #------------------------
    display.flip()
    myClock.tick(30)
quit()
    
