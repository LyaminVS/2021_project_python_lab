import pygame

START_MENU_SCREEN = pygame.display.set_mode((1280, 720))
GREY = (50, 50, 50)


def writing(text: str, xcenter, ycenter, font_size=16, font='Arial'):
    """
    writes text on screen
    :param text: text to appear on screen
    :param xcenter: x coordinate of center
    :param ycenter: y coordinate of center
    :param font_size: size of the font, which is standart Arial
    :param font: шрифт, который будет использован для надписи
    """
    font = pygame.font.SysFont(font, font_size)
    words = font.render(text, True, (200, 0, 0))
    place = words.get_rect(center=(xcenter, ycenter))
    START_MENU_SCREEN.blit(words, place)


class Button:
    """
    class of buttons on the screen.
    """

    def __init__(self, x, y, length, width, text: str, ):
        """
        constructor of button class.
        :param x: horizontal coordinate of a button
        :param y: vertical coordinate of a button
        :param length: length of a button
        :param width: width of a button
        :param text: text displayed on a button
        """
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.text = text
        self.first_condition = pygame.image.load("pics/cat4.png")
        self.second_condition = pygame.image.load("pics/cat5.png")
        self.image = self.first_condition
        self.pressed = False
        self.timer = 0
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def scaling_image(self):
        scale_item = pygame.transform.scale(self.image, (self.length, self.width))
        self.image = scale_item

    def update(self):
        """
        function drawing the button on a screen.
        """
        if self.pressed is True:
            self.image = self.second_condition
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        else:
            self.image = self.first_condition
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.scaling_image()
        START_MENU_SCREEN.blit(self.image, self.rect)
        writing(self.text, self.x + self.length / 2, self.y + self.width / 2)

        if self.timer > 0:
            self.timer += 1
        if self.timer % 30 == 0:
            self.pressed = False

    def is_button_pressed(self, event):
        """
        checks if button is pressed.
        """

        if self.x < event.pos[0] < self.x + self.length and self.y < event.pos[1] < self.y + self.width:
            self.pressed = True
            self.timer = 1


class Menu:
    def __init__(self, amount, texts: list):
        self.finished = False
        self.buttons = []
        self.variables = []
        self.amount = amount
        for a in range(amount):
            self.buttons.append(Button(540, 200 + a * 100, 200, 75, texts[a]))
            self.variables.append(False)

    def draw_background(self):
        background_surface = pygame.Surface((400, 250 + self.amount * 100))
        background = pygame.draw.rect(background_surface, GREY, (440, 20, 400, self.amount * 100))
        background_surface.set_alpha(100)
        START_MENU_SCREEN.blit(background_surface, background)

    def create_menu(self, text: str):
        self.finished = False
        self.draw_background()
        writing(text, 640, 100, 64, "Impact")

        for button in self.buttons:
            button.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                for i in range(len(self.buttons)):
                    self.buttons[i].is_button_pressed(event)
                    if self.buttons[i].pressed is True:
                        self.variables[i] = True
                    else:
                        self.variables[i] = False
                    if i == len(self.variables) - 1 and self.variables[i] == 1:  # последний - это всегда выход из игры
                        self.finished = True
            if event.type == pygame.QUIT:
                self.finished = True


class StartMenu(Menu):
    def __init__(self):
        super().__init__(3, ["start", "options", "exit"])
        self.start = False
        self.options = False

    def draw(self):
        super().create_menu("DOLGOPIO")
        self.start = self.variables[0]
        self.options = self.variables[1]
        return self.finished, self.start, self.options


class OptionMenu(Menu):  # continue, music, exit
    def __init__(self):
        super().__init__(3, ["continue", "music", "exit"])
        self.continues = False
        self.music = False

    def draw(self):
        super().create_menu("OPTIONS")
        self.continues = self.variables[0]
        self.music = self.variables[1]
        return self.finished, self.continues, self.music


class PauseMenu(Menu):  # continue, options, start_menu ,exit
    def __init__(self):
        super().__init__(4, ["continue", "options", "start_menu", "exit"])
        self.continues = False
        self.options = False
        self.start_menu = False

    def draw(self):
        super().create_menu("PAUSED")
        self.continues = self.variables[0]
        self.options = self.variables[1]
        self.start_menu = self.variables[2]
        return self.finished, self.continues, self.options, self.start_menu
