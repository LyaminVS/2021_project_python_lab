import pygame
import background
import map_logic
import menu
import objects
import sound
import start_screen

pygame.init()
screen = pygame.display.set_mode(1280, 720)
FPS = 30
finished = False
clock = pygame.time.Clock()


while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()