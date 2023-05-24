import pygame

pygame.init()
controller = pygame.joystick.Joystick(0)
controller.init()

while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            axis_value = event.value
            axis_id = event.axis
            print(f"Axis {axis_id}: {axis_value}")