"""
assets.py
Raymond Wu and Kevin Xu

This file loads and contains all the assets for the game.
"""


from pygame import *
init()


redBase = image.load('assets/redTankNorm.png')
blueBase = image.load('assets/blueTankNorm.png')
blackBase = image.load('assets/blackTankNorm.png')


redMissile = image.load('assets/redTankMissile.png')
blueMissile = image.load('assets/blueTankMissile.png')
blackMissile = image.load('assets/blackTankMissile.png')

blueMachine = image.load('assets/blueTankMachine.png')
redMachine = image.load('assets/redTankMachine.png')
blackMachine = image.load('assets/blackTankMachine.png')


redShield = image.load("assets/redTankShield.png")
blueShield = image.load("assets/blueTankShield.png")
blackShield = image.load("assets/blackTankShield.png")

blueRay = image.load("assets/blueTankRay.png")
redRay = image.load("assets/redTankRay.png")
blackRay = image.load("assets/blackTankRay.png")

blueShotgun = image.load("assets/blueTankShotgun.png")
redShotgun = image.load("assets/redTankShotgun.png")
blackShotgun = image.load("assets/blackTankShotgun.png")

machinegunPU = image.load("assets/machineGunPU.png")
shotgunPU = image.load("assets/shotgunPU.png")
shieldPU = image.load("assets/shieldPU.png")
rayPU = image.load("assets/rayCannonPU.png")
missilePU = image.load("assets/missilePU.png")


deathExplosion = mixer.Sound("assets/sounds/funnyDeath.mp3")
pop = mixer.Sound("assets/sounds/pop.mp3")
ping = mixer.Sound("assets/sounds/ping.mp3")
pong = mixer.Sound("assets/sounds/pong.mp3")
shotVanish = mixer.Sound("assets/sounds/shotVanish.mp3")
PUappear = mixer.Sound('assets/sounds/PUappear.mp3')
activated = mixer.Sound('assets/sounds/shieldActivated.mp3')

# Font
font.init()
clashFontS = font.Font("assets/font/CR.ttf", 14)
clashFontM = font.Font("assets/font/CR.ttf", 20)
clashFontL = font.Font("assets/font/CR.ttf", 25)
clashFontXL = font.Font("assets/font/CR.ttf", 35)
clashFontTitle = font.Font("assets/font/CR.ttf", 80)
explosions = []
for i in range(1,9):
    explosions.append(transform.scale(image.load("assets/explosion" + str(i) + ".png"), (100,100)))


# Arrows
arrowLeft = image.load("assets/arrowLeft.png")
arrowRight = image.load("assets/arrowRight.png")

#Settings Background
settingsBg = image.load("assets/settingBKG.png")
