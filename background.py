import pygame
from start_screen import Button


def draw_map(sc, x, y):
    """
    рисует карту
    """

    bg = pygame.image.load('pics/background.png')
    sc.blit(bg, (-x, -y))


def draw_objects(objects_list, x, y):
    """
    рисует объекты
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
            x += 600  # смещение сетки по горизонтали. это и все другие постоянные значения в этой функции выбраны в
            # соответствии с выбранным размером холста и размером областей, отображаемых на экране
        x = x0
        y += 400  # смещение сетки по вертикали
    return grid


def change_coord_grid(grid, x0, y0, columns):
    """
    функция, которая отвечает за изменение координат сетки
    :param grid: сетка, координаты которой нужно изменить
    :param x0: начальная координата сетки по горизонтали
    :param y0: начальная координата сетки по вертикали
    :param columns: столбцы
    """
    x = x0
    y = y0
    f = 0
    for square in grid:
        if f % columns == 0 and f != 0:
            x = x0
            y -= 400  # смещение сетки по вертикали. это и все другие постоянные значения в этой функции выбраны в
            # соответствии с выбранным размером холста и размером областей, отображаемых на экране
            f = 0
        square.x = -x + 2300  # начальное положение сетки по абсолютной горизонтальной координате
        square.y = -y + 3850  # начальное положение сетки по абсолютной вертикальной координате
        x -= 600  # смещение сетки по горизонтали
        f += 1


if __name__ == "__main__":
    print("This module is not for direct call!")
