
def play():
    mainRunning = True
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 700
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLACK = (0,0,0)
    BLUE = (0,0,255)
    GREY = (155,155,155)
    screen = display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    display.set_caption("ICS3U FSE")
    display.set_icon(assets.blueBase)

    wallwidth = 20
    space = Rect(wallwidth,wallwidth,SCREEN_WIDTH-2*wallwidth, SCREEN_HEIGHT-2*wallwidth)
    xmin = wallwidth
    xmax = SCREEN_WIDTH- wallwidth
    ymin = wallwidth
    ymax = SCREEN_HEIGHT - wallwidth

    tankLeft = tank.Tank(screen, assets.redBase, 200, screen.get_height()/2, 0, RED, 1, 'player1')
    tankRight = tank.Tank(screen, assets.blackBase, 800, screen.get_height()/2, 0, BLACK, 1, 'player2')
    dummy = tank.Tank(screen, assets.blueBase, 500, screen.get_height()/2, 0, BLUE, 3, 'dummy')
    dummy.angVel = 2*pi/180; dummy.mag = 4; dummy.bulletVel = 8; dummy.reloadPeriod = 5000

    Tanks = [tankLeft, tankRight,dummy]
    del Tanks[2]
    # Tanks = [tank.tankLeft, tank.tankRight]
    lis = [0 for i in range(50)] + [1]



    #map stuff
    gridSize = 100
    horizontalLines = []
    verticalLines   = []
    possibility = [ 0 for i in range(8)]+ [1]
    width = screen.get_width()//gridSize
    height = screen.get_height()//gridSize
    thickness = 10
    def gridGen():
        for y in range(height+1):
            horizontalLines.append([])
            verticalLines.append([])
            for x in range(width+1):
                # if y == 0 or y == height-1:
                #     horizontalLines[-1].append([x*gridSize, y*gridSize, (x+1)*gridSize, y*gridSize, 1])
                #     verticalLines[-1].append([x*gridSize, y*gridSize, x*gridSize, (y+1)*gridSize, choice(possibility)])
                # else:
                if y == 0 or y == height:
                    horizontalLines[-1].append([x*gridSize, y*gridSize, (x+1)*gridSize, y*gridSize, 1])
                    verticalLines[-1].append([x*gridSize, y*gridSize, x*gridSize, (y+1)*gridSize, choice(possibility)])
                if x == 0 or x == width:
                    horizontalLines[-1].append([x*gridSize, y*gridSize, (x+1)*gridSize, y*gridSize, choice(possibility)])
                    verticalLines[-1].append([x*gridSize, y*gridSize, x*gridSize, (y+1)*gridSize, 1])
                else:
                    horizontalLines[-1].append([x*gridSize, y*gridSize, (x+1)*gridSize, y*gridSize, choice(possibility)])
                    verticalLines[-1].append([x*gridSize, y*gridSize, x*gridSize, (y+1)*gridSize, choice(possibility)])
            
    def gridDraw():
        for y in range(len(horizontalLines)):
            for x in range(len(horizontalLines[y])):
                if horizontalLines[y][x][4]:
                    draw.line(screen, BLACK, (horizontalLines[y][x][0], horizontalLines[y][x][1]), (horizontalLines[y][x][2], horizontalLines[y][x][3]),thickness)
                if verticalLines[y][x][4]:
                    draw.line(screen, BLACK, (verticalLines[y][x][0],   verticalLines[y][x][1]),   (verticalLines[y][x][2], verticalLines[y][x][3]),thickness)  

    def ifHitWalls():
        for y in range(len(horizontalLines)):
            for x in range(len(horizontalLines[y])):
                
                    for ta in Tanks:
                        for shot in ta.shots:
                            if horizontalLines[y][x][4] and horizontalLines[y][x][0] <= shot[tank.X] and shot[tank.X] <= horizontalLines[y][x][2]:
                                # print('inRange')
                                if shot[tank.Y] <= horizontalLines[y][x][1] + thickness/2 + ta.bulletRad and shot[tank.Y] >= horizontalLines[y][x][1] - thickness/2 - ta.bulletRad:
                                    shot[tank.VY] = -shot[tank.VY]
                                    tank.bounceSound('pong')
                            if verticalLines[y][x][4] and verticalLines[y][x][1] <= shot[tank.Y] and shot[tank.Y] <= verticalLines[y][x][3]:
                                # print('inRange')
                                if shot[tank.X] <= verticalLines[y][x][0] + thickness/2 + ta.bulletRad and shot[tank.X] >= verticalLines[y][x][0] - thickness/2 - ta.bulletRad:
                                    shot[tank.VX] = -shot[tank.VX]
                                    tank.bounceSound('ping')
                        
                # if verticalLines[y][x][4:]:


    gridGen()


    while mainRunning:
        rightShoot,leftShoot = False, False
        for evt in event.get():
            if evt.type == QUIT:
                mainRunning = False
            if evt.type == KEYDOWN:
                if evt.key == K_c:
                    leftShoot = True
                if evt.key == K_SLASH:
                    rightShoot = True
            if evt.type == MOUSEBUTTONDOWN:
                horizontalLines = []
                verticalLines   = []
                gridGen()

        keyArray = key.get_pressed()

        screen.fill(GREY)
        # draw.rect(screen, GREY, space)
        # for map in level.map1:
        #     draw.rect(screen, (0,0,0), map)

    

        # print(keyArray[K_w],keyArray[K_s],keyArray[K_a],keyArray[K_d],leftShoot,"      ", keyArray[K_UP],keyArray[K_DOWN],keyArray[K_LEFT],keyArray[K_RIGHT], rightShoot)
        tankLeft.update(keyArray[K_w],keyArray[K_s],keyArray[K_a],keyArray[K_d],leftShoot) 
        tankRight.update(keyArray[K_UP],keyArray[K_DOWN],keyArray[K_LEFT],keyArray[K_RIGHT], rightShoot)
        if len(Tanks) == 3:
            dummy.update(0, 0, 0, 1, 0)


        deadone = tank.deathDetect(Tanks)
        if deadone:
            mixer.Sound.play(assets.deathExplosion)
            _ = screen.copy()
            for i in range(8):
                screen.blit(_, (0,0))
                assets.explosions[i] = transform.scale(assets.explosions[i], (deadone.scale*100, deadone.scale*100))
                heherect = assets.explosions[i].get_rect(center = (deadone.x, deadone.y))
                screen.blit(assets.explosions[i], heherect)
                time.delay(100)
                display.flip()
            time.delay(3000)
            mainRunning = False

        for ta in Tanks:
            if tank.touchingWalls(xmin,xmax, ymin, ymax, ta.basePoints):
                ta.angle -= ta.movement[0]
                ta.x     -= ta.movement[1]
                ta.y     -= ta.movement[2]
        ifHitWalls()
        

        gridDraw()
        display.flip()
        time.Clock().tick(50)
    
    quit()
