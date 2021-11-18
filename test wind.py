import pygame as pg
import sys

W = 1280
H = 720
pg.init()
sc = pg.display.set_mode((W, H))
bg = pg.image.load('background_grass.png')
bg_rect = bg.get_rect()

FPS = 30


clock = pg.time.Clock()

finished = False


while not finished:
    sc.fill((0,255,255))
    sc.blit(bg, bg_rect)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
    pg.display.update()
pg.quit()
