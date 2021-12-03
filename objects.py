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
        self.image = pygame.image.load(image).convert_alpha()
        self.image_name = image
        self.surface = screen
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x_0
        self.y = y_0
        self.inventory = None
        self.collide_rect = pygame.Rect(0, 0, 0, 0)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.resources = []
        self.inventory_opened = False

    def draw(self, x, y):
        """
        Функция отрисовки объекта.
        :param x: координата отрисовки по х (левая верхняя)
        :param y: координата отрисовки по у (правая верхняя)
        """
        self.collide_rect = pygame.Rect(-x + self.x, -y + self.y, self.width, self.height)
        self.surface.blit(self.image, (-x + self.x, -y + self.y))

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

    def __init__(self, screen, name, x_0, y_0, resources=[]):
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
        self.x = x_0
        self.y = y_0
        self.vx = 0
        self.vy = 0
        self.v_max = 4
        self.image = pygame.image.load("pics/skin run right1.png").convert_alpha()
        self.image_name = "pics/skin run right1.png"
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.inventory = None
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.collide_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.resources = resources
        self.up = 0
        self.right = 0
    
    def draw(self):
        """
        Функция отрисовки игрока.
        """
        self.collide_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.right == 0 and self.up == 0:
            self.image = pygame.image.load("pics/skin stay.png")
            self.image_name = "pics/skin run stay.png"
        elif self.right == 0:
            if self.up == 1:
                self.image = pygame.image.load("pics/skin run up1.png")
                self.image_name = "pics/skin run up1.png"
            elif self.up == 2:
                self.image = pygame.image.load("pics/skin run up2.png")
                self.image_name = "pics/skin run up2.png"
            if self.up == -1:
                self.image = pygame.image.load("pics/skin run down1.png")
                self.image_name = "pics/skin run down1.png"
            elif self.up == -2:
                self.image = pygame.image.load("pics/skin run down2.png")
                self.image_name = "pics/skin run down2.png"
        elif self.right != 0:
            if self.right == 1:
                self.image = pygame.image.load("pics/skin run right1.png")
                self.image_name = "pics/skin run right1.png"
            elif self.right == 2:
                self.image = pygame.image.load("pics/skin run right2.png")
                self.image_name = "pics/skin run right2.png"
            if self.right == -1:
                self.image = pygame.image.load("pics/skin run left1.png")
                self.image_name = "pics/skin run left1.png"
            elif self.right == -2:
                self.image = pygame.image.load("pics/skin run left2.png")
                self.image_name = "pics/skin run left2.png"
        self.surface.blit(self.image, self.rect)

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

    def __init__(self, screen, image, name, is_building):
        """
        Конструктор класса resources.
        :param screen: поверхность отрисовки
        :param image: иллюстрация ресурса
        :param name: имя ресурса
        """
        self.name = name
        self.image = pygame.image.load(image).convert_alpha()
        self.image_name = image
        self.width = self.image.get_width()
        self.height = self.image.get_width()
        self.surface = screen
        self.amount = 15
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.is_building = is_building

    def __str__(self):
        """
        :return: параметры объекта одной строкой с разделителем ";"
        """
        line = ";".join((self.name, self.image_name, str(self.width), str(self.height)))
        return line


class Taco(Resources):
    def __init__(self, screen):
        super(Taco, self).__init__(screen, "pics/taco.png", "Taco", False)


class Landau(Resources):
    def __init__(self, screen):
        super(Landau, self).__init__(screen, "pics/landavshiz.png", "Landau", False)


class Brain(Resources):
    def __init__(self, screen):
        super(Brain, self).__init__(screen, "pics/cat.png", "Brain", False)


class Palatka(Resources):
    def __init__(self, screen):
        super(Palatka, self).__init__(screen, "pics/shawarma.png", "Palatka", True)
