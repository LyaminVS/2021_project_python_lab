import pygame

START_MENU_SCREEN = pygame.display.set_mode((1280, 720))
GREY = (50, 50, 50)
DARK_BLUE = (1, 3, 20)


def writing(text: str, xcenter, ycenter, screen, font_size=16, font='Arial'):
    """
    Функция, отвечающая за написание текста на основном
    :param text: текст, который должен появиться
    :param xcenter: х координата центра
    :param ycenter: y координата центра
    :param font_size: размер шрифта, по умолчанию 16
    :param font: шрифт, который будет использован для надписи, по умолчанию Arial
    :param screen: экран, на котором будет отрисован текст
    """
    font = pygame.font.SysFont(font, font_size)
    words = font.render(text, True, (200, 0, 0))
    place = words.get_rect(center=(xcenter, ycenter))
    screen.blit(words, place)


class Button:
    """
    Класс, отвечающий за прорисовку кнопок на экране, а также взаимодействие с ними.
    """

    def __init__(self, x, y, length, width, text: str, screen):
        """
        :param x: горизонтальная координата левого верхнего угла кнопки.
        :param y: вертикальная координата левого верхнего угла кнопки.
        :param length: длина кнопки.
        :param width: ширина/высота кнопки.
        :param text: текст, который должен отображаться на кнопке.
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.text = text
        self.first_condition = pygame.image.load(
            "pics/startbuttonunpressed.png")  # картинка кнопки, когда она не нажата
        self.second_condition = pygame.image.load("pics/startbuttonpressed.png")  # картинка кнопки, когда она нажата
        self.image = self.first_condition  # изображение, которое отрисовывается на кнопке
        self.pressed = False  # Нажата ли сейчас кнопка?
        self.pressed_by_mouse = False  # Нажата ли кнопка мышкой?
        self.timer = 0  # Счетчик итераций, который включается во время нажатия кнопки и выключается после 7 циклов
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.picture_changed = 0  # Менялась ли картинка у кнопки
        self.building_on = False

    def scaling_image(self):
        """
        Функция, отвечающая за скейлинг изображения под необходимые размеры.
        """
        scale_item = pygame.transform.scale(self.image, (self.length, self.width))
        self.image = scale_item

    def update(self):
        """
        Функция, отвечающая за отображение кнопки и обновление ее состояний.
        """
        if self.pressed:
            self.image = self.second_condition
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        else:
            self.image = self.first_condition
            self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.scaling_image()
        self.screen.blit(self.image, self.rect)
        writing(self.text, self.x + self.length / 2, self.y + self.width / 2, self.screen)

        if self.timer > 0:
            self.timer += 1
        if self.timer % 7 == 0 and self.timer != 0:
            self.pressed = False
            self.pressed_by_mouse = False
            self.timer = 0

    def is_button_pressed(self, event):
        """
        Функция, отвечающая за проверку нажатия кнопки.
        :param event: событие нажатия, если подавать несвязанные с нажатием события, то выдаст ошибку.
        """
        if self.x < event.pos[0] < self.x + self.length and self.y < event.pos[1] < self.y + self.width:
            self.pressed = True
            self.timer = 1

            if event.type == pygame.MOUSEBUTTONUP:
                self.pressed_by_mouse = True


class Menu:
    """
    Функция, отвечающая за отрисовку основы меню.
    """

    def __init__(self, amount, texts: list, screen, buttons_images_up=None, buttons_images_down=None):
        """
        :param amount: количество планирующихся кнопок.
        :param texts: массив с текстами, которые необходимо разместить на кнопках
        """
        self.screen = screen
        self.finished = False  # Требуется ли выходить из программы?
        self.buttons = []  # массив, в котором хранятся все кнопки, последняя кнопка - это всегда выход из игры
        self.variables = []  # массив с переменными, отвечающими за переключение режимов игры(пауза, старт, конец)
        self.amount = amount
        self.buttons_images_down = buttons_images_down
        self.buttons_images_up = buttons_images_up
        for a in range(self.amount):
            self.buttons.append(
                Button(366, 200 + a * 100, 548, 78, texts[a], self.screen))  # размещает кнопки по центру экрана
            self.variables.append(False)  # задает всем переменным состояний игры изначально False значение.
            if self.buttons_images_down and self.buttons_images_up:
                self.buttons[a].first_condition = pygame.image.load(self.buttons_images_up[a])
                self.buttons[a].second_condition = pygame.image.load(self.buttons_images_down[a])

    def draw_background(self):
        """
        Функция, отвечающая за прорисовку заднего фона у меню. По умолчанию это серый прозрачный прямоугольник.
        """
        width = 250 + self.amount * 100
        background_surface = pygame.Surface((748, width))
        pygame.draw.rect(background_surface, DARK_BLUE, (0, 0, 748, width))
        background_surface.set_alpha(20)
        self.screen.blit(background_surface, (266, (720 - width) // 2))

    def create_menu(self, picture):
        """
        Функция, отвечающая за создание меню. Обновляет кнопки, проверяет нажатия на них, обновляет связанные
        с ними переменные.
        :param picture: название картинки, которая будет нарисовано над кнопками.
        """
        self.finished = False
        self.draw_background()
        self.screen.blit(pygame.image.load(picture), (225, 50))
        for i in range(len(self.variables)):
            self.variables[i] = False
        for button in self.buttons:
            button.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                for i in range(len(self.buttons)):  # проверяем какая кнопка была нажата.
                    self.buttons[i].is_button_pressed(event)
                    if self.buttons[i].pressed is True:  # обновляем переменные состояний игры, связанные с кнопками
                        self.variables[i] = True
                    else:
                        self.variables[i] = False
                    if i == len(self.variables) - 1 and self.variables[i] == 1:
                        # последняя кнопка - это всегда выход из игры
                        self.finished = True
            if event.type == pygame.QUIT:
                self.finished = True


class StartMenu(Menu):
    """
    Класс, отвечающий за отрисовку стартового меню.
    """

    def __init__(self, screen):
        buttons_up = ["pics/startbuttonunpressed.png", "pics/optionsbuttonunpressed.png",
                      "pics/exitbuttonunpressed.png"]
        buttons_down = ["pics/startbuttonpressed.png", "pics/optionsbuttonpressed.png", "pics/exitbuttonpressed.png"]
        super().__init__(3, ["", "", ""], screen, buttons_up, buttons_down)
        self.start = False  # Если True, то надо начать игру
        self.options = False  # Если True, то надо перейти в настройки

    def draw(self):
        """
        Функция, отвечающая за отрисовку стартового меню.
        :return: self.finished, self.start, self.options
        """
        super().create_menu("pics/gamename.png")
        self.start = self.variables[0]
        self.options = self.variables[1]
        return self.finished, not self.start, self.options


class OptionMenu(Menu):
    """
    Класс, отвечающий за отрисовку меню настроек
    """

    def __init__(self, screen):
        buttons_up = ["pics/continueunpressed.png", "pics/musicunpressed.png", "pics/exitbuttonunpressed.png"]
        buttons_down = ["pics/continuepressed.png", "pics/musicpressed.png", "pics/exitbuttonpressed.png"]
        super().__init__(3, ["", "", ""], screen, buttons_up, buttons_down)
        self.continues = False  # Если True, то продолжаем играть.
        self.music = False  # Если True, то надо перейти в меню выбора музыки.

    def draw(self):
        """
        Класс, отвечающий за отрисовку меню настроек.
        :return: self.finished, self.continues, self.music
        """
        super().create_menu("pics/options text.png")
        self.continues = self.variables[0]
        self.music = self.variables[1]
        return self.finished, self.continues, self.music


class PauseMenu(Menu):
    """
    Класс, отвечающий за отрисовку меню паузы.
    """

    def __init__(self, screen):
        buttons_up = ["pics/continueunpressed.png", "pics/optionsbuttonunpressed.png", "pics/startmenuunpressed.png",
                      "pics/exitbuttonunpressed.png"]
        buttons_down = ["pics/continuepressed.png", "pics/optionsbuttonpressed.png", "pics/startmenupressed.png",
                        "pics/exitbuttonpressed.png"]
        super().__init__(4, ["", "", "", ""], screen, buttons_up, buttons_down)
        self.continues = False  # Если True, то продолжаем игру
        self.options = False  # Если True, то переходим в меню настроек
        self.start_menu = False  # Если True, то возвращаемся в StartMenu

    def draw(self):
        """
        Функция, отвечающая за отрисовку меню паузы.
        :return: self.finished, self.continues, self.options, self.start_menu
        """
        super().create_menu("pics/paused.png")
        self.continues = self.variables[0]
        self.options = self.variables[1]
        self.start_menu = self.variables[2]
        return self.finished, not self.continues, self.options, self.start_menu
