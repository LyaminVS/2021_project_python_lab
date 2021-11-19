import pygame
import menu


class Objects(pygame.sprite.Sprite):
    """
    Класс свойств объекта с функцией отрисовки.
    """

    def __init__(self, screen, image, name, x_0, y_0):
        super().__init__()
        self.name = name
        self.image = pygame.image.load(image)
        self.surface = screen
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x_0
        self.y = y_0
        self.inventory = None

    def draw(self, x, y):
        self.surface.blit(self.y, (x, y))

    def __str__(self):
        line = ";".join((self.name, self.image, self.x, self.y))
        return line


class Player(pygame.sprite.Sprite):
    """
    инвентарь
    скорость
    различные состояния картинки
    """

    def __init__(self, screen, name, x_0, y_0):
        super().__init__()
        self.name = name
        self.surface = screen
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x_0
        self.y = y_0
        self.vx = 2
        self.vy = 2
        self.image = pygame.image.load("skin run right1.png")
        self.inventory = None

    def draw(self, right):
        if right == 1:
            self.image = pygame.image.load("skin run right1.png")
        else:
            self.image = pygame.image.load("skin run left1.png")

    def __str__(self):
        line = ";".join((self.name, self.image, self.x, self.y))
        return line


class Resources:
    """
    от этого класса наследовать все ресурсы
    """

    def __init__(self, screen, image, name):
        self.name = name
        self.image = pygame.image.load(image)
        self.surface = screen
        self.amount = 15
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def __str__(self):
        line = ";".join((self.name, self.image, self.width, self.height))
        return line


class Taco(Resources):
    def __init__(self, screen):
        super(Taco, self).__init__(screen, "taco.png", "taco")
