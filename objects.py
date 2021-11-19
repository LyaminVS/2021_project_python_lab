import pygame
import menu


class Objects(pygame.sprite.Sprite):
    """
    Класс свойств объекта с функцией отрисовки.
    """

    def __init__(self, screen, image, x_0, y_0):
        super().__init__()
        self.image = pygame.image.load(image)
        self.surface = screen
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x_0
        self.y = y_0

    def draw(self, x, y):
        self.surface.blit(self.y, (x, y))


class Buildings(Objects):
    """
    меню взаимодействия
    инвентарь постройки
    """

    def __init__(self, screen, image, x_0, y_0):
        super().__init__()
        self.menu = 0  # add


class Player(pygame.sprite.Sprite):
    """
    инвентарь
    скорость
    различные состояния картинки
    """

    def __init__(self, screen, x_0, y_0):
        super().__init__()
        self.surface = screen
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x_0
        self.y = y_0
        self.vx = 2
        self.vy = 2
        self.image = pygame.image.load("skin run right1.png")

    def draw(self, right):
        if right == 1:
            self.image = pygame.image.load("skin run right1.png")
        else:
            self.image = pygame.image.load("skin run left1.png")


class Resources:
    """
    от этого класса наследовать все ресурсы
    """
    def __init__(self, screen, image):
        self.image = pygame.image.load(image)
        self.surface = screen
