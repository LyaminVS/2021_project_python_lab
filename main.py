import pygame
import background
import map_logic
import menu
import objects
import sound
import start_screen

pygame.init()


finished = False

while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()