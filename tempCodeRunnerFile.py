if horizontalLines[y][x][0] <= shot[tank.X] and shot[tank.X] <= horizontalLines[y][x][2]:
                        #     # print('inRange')
                        #     if shot[tank.Y] <= horizontalLines[y][x][1] + thickness/2 + ta.bulletRad and shot[tank.Y] >= horizontalLines[y][x][1] - thickness/2 - ta.bulletRad:
                        #         shot[tank.VY] = -shot[tank.VY]
                        #         tank.bounceSound('pong')