import pygame
from start_screen import Button


def draw_map(sc, x, y, objects):
    """
    рисует карту
    :return:
    """

    bg = pygame.image.load('pics/background.png')
    sc.blit(bg, (-x, -y))
    draw_objects(objects, x, y)


def draw_objects(objects_list, x, y):
    """
    рисует объекты
    :return:
    """

    for obj in objects_list:
        obj.draw(x, y)


def create_grid(x0, y0, rows, columns, screen):
    """
    Создает сетку
    x0, y0 - координаты начала
    x1, y1 - координаты конца
    """
    grid = []
    x = x0
    y = y0
    for i in range(rows):
        for j in range(columns):
            square = Button(x, y, 500, 300, "", screen)
            grid.append(square)
            x += 600
        x = x0
        y += 400
    return grid


def change_coord_grid(grid, x0, y0, rows, columns):
    x = x0
    y = y0
    f = 0
    for i in range(rows):
        for j in range(columns):
            square = grid[f]
            square.x = -x + 1600
            square.y = -y + 3350
            x += 600
            f += 1
        x = x0
        y += 400
