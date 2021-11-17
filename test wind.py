import pygame as pg
import sys

W = 1280
H = 720

sc = pg.display.set_mode(W, H)
bg = pg.image.load('background_grass.png')
bg_rect = bg.get_rect()
sc.blit(bg, bg_rect)


pg.display.update()
