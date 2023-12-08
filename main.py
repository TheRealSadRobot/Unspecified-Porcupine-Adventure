import pygame

pygame.init()

import time
import Player
import Menu
import Settings
import Level

window = pygame.display.set_mode((1280,720))
fpstimer = pygame.time.Clock()
linelayer = pygame.Surface((1280, 720))
charlayer = pygame.Surface((1280, 720))
charlayer.set_colorkey("#111111")

objects = []


if Settings.debug:
    level = Level.Level(charlayer, objects)
else:
    title = Menu.menu(charlayer,"Title",objects)

print(objects)

while True:
    fpstimer.tick(60)
    #prep Charlayer
    charlayer.fill("#111111")

    for item in objects:
        item.update()
    
    window.blit(charlayer, (0,0))
    pygame.display.flip()
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
