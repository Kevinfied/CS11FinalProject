import pygame

pygame.joystick.init()

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))


while True:

    pygame.time.wait(100)
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.JOYBUTTONDOWN:
            print(event)
        if event.type == pygame.JOYHATMOTION:
            print(event)
