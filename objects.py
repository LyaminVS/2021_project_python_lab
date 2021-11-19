import pygame


class Objects(pygame.sprite.Sprite):
    """
    Класс объекта (пока только применим к зданиям).
    """
    def __init__(self, screen, image, name, x_0, y_0):
        """
        Конкструктор класса Objects.
        :param screen: экран отрисовки
        :param image: иллюстрация объекта
        :param name: имя объекта
        :param x_0: координата объекта по х
        :param y_0: координата объекта по у
        """
        super().__init__()
        self.name = name
        self.image = pygame.image.load(image)
        self.image_name = image
        self.surface = screen
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x_0
        self.y = y_0
        self.inventory = None

    def draw(self, x, y):
        """
        Функция отрисовки объекта.
        :param x: координата отрисовки по х (левая верхняя)
        :param y: координата отрисовки по у (правая верхняя)
        """
        self.surface.blit(self.y, (x, y))

    def __str__(self):
        """
        :return: параметры объекта одной строкой с разделителем ";"
        """
        line = ";".join((self.name, self.image_name, str(self.x), str(self.y)))
        return line


class Player(pygame.sprite.Sprite):
    """
    Класс игрока, наследующий Spite для проверки коллизий.
    """
    def __init__(self, screen, name, x_0, y_0):
        """
        Конструктор класса Player.
        :param screen: экран отрисовки
        :param name: имя объекта
        :param x_0: координата игрока по оси х
        :param y_0: координата игрока по оси у
        """
        super().__init__()
        self.name = "player"
        self.surface = screen
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x_0
        self.y = y_0
        self.vx = 2
        self.vy = 2
        self.image = pygame.image.load("skin run right1.png")
        self.image_name = "skin run right1.png"
        self.inventory = None

    def draw(self, right):
        """
        Функция отрисовки игрока.
        :param right: параметр, проверяющий, в какую сторону движется игрок
        """
        if right == 1:
            self.image = pygame.image.load("skin run right1.png")
            self.image_name = "skin run right1.png"
        else:
            self.image = pygame.image.load("skin run left1.png")
            self.image_name = "skin run left1.png"

    def __str__(self):
        """
        :return: параметры объекта одной строкой с разделителем ";"
        """
        line = ";".join((self.name, self.image_name, str(self.x), str(self.y)))
        return line


class Resources:
    """
    Класс наследования всех ресурсов.
    """
    def __init__(self, screen, image, name):
        """
        Конструктор класса resources.
        :param screen: поверхность отрисовки
        :param image: иллюстрация ресурса
        :param name: имя ресурса
        """
        self.name = name
        self.image = pygame.image.load(image)
        self.image_name = image
        self.surface = screen
        self.amount = 15
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def __str__(self):
        """
        :return: параметры объекта одной строкой с разделителем ";"
        """
        line = ";".join((self.name, self.image_name, str(self.width), str(self.height)))
        return line


class Taco(Resources):
    def __init__(self, screen):
        super(Taco, self).__init__(screen, "pics/taco.png", "taco")
