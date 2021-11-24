import pygame


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
