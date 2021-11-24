import pygame


def draw_map(sc, x_0, y_0, objects):
    """
    рисует карту
    :return:
    """
    bg = pygame.image.load('pics/background.png')
    bg_rect = bg.get_rect()
    sc.blit(bg, (-x_0, -y_0))
    draw_objects(sc, objects, x_0, y_0)


def draw_objects(sc_0, objects_list, x_m, y_m):
    """
    рисует объекты
    :return:
    """
    for obj in objects_list:
        sc_0.blit(obj.image, (obj.x - x_m, obj.y - y_m))
