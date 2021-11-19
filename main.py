import pygame
import background
import map_logic
# import menu
import objects
# import sound
import start_screen

pygame.init()


class Params:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        """
        Холст для рисования
        """

        self.FPS = 30
        """
        Количество кадров в секунду
        """

        self.finished = False
        """
        False если программа завешшена, иначе True
        """

        self.clock = pygame.time.Clock()
        """
        часы pygame
        """

        self.game_started = False
        """
        если была нажата кнопка старт на стартовом экране то True, иначе False
        """

        self.player_created = False
        """
        True если игрок создан, иначе False
        """

        self.player = None
        """
        пееменная содержащая объект игрока
        """

        self.all_objects = []
        """
        все объекты на карте
        """

        self.menu = "start_menu"
        """
        переменная показывает в каком меню находится игрок
        """


def open_start_menu():
    """
    открывает стартовое меню игры
    """
    start_menu = start_screen.StartMenu(params.screen)
    start_menu.draw()


def line_to_object(line):
    """
    преобразовывает строку в объект класса Object
    :param line: строка файла
    :return:
    """
    name, image, x, y = line.split(";")
    new_object = objects.Objects(params.screen, image, name, x, y)
    return new_object


def line_to_player(line):
    """
    преобразовывает строку в объект класса Player
    :param line: строка файла
    :return:
    """
    name, image, x, y = line.split(";")
    new_player = objects.Objects(params.screen, image, name, x, y)
    return new_player


def get_player_from_file():
    """
    преобразовывает файл в объект класса Player
    :return: объект класса Player
    """
    player_file = open("player_save.txt")
    player_line = player_file.readline()
    player = line_to_player(player_line)
    player_file.close()
    return player


def get_obj_from_file():
    """
    преобразовывает файла в объект класса Object
    :return: массив объектов класса Object
    """
    all_objects = []
    objects_in_file = open("objects_save.txt")
    for line in objects_in_file:
        new_obj = line_to_object(line)
        all_objects.append(new_obj)
    objects_in_file.close()
    return all_objects


def create_start_position():
    """
    создается объект игрока, а также объекты зданий в первый кадр игры
    :return:
    """
    params.player = get_player_from_file()
    params.objects = get_obj_from_file()


def update_game(event):
    """
    функция обновляет состояние игры
    :return:
    """
    background.draw_map()
    background.draw_objects()
    map_logic.event_checker(event)
    map_logic.player_move(params.player, params.all_objects)


def save_game():
    """
    функция сохраняет игру
    :return:
    """
    player_file = open("player_save.txt", "w")
    object_file = open("objects_save.txt", "w")
    player_file.write(str(params.player) + "\n")
    for obj in params.all_objects:
        object_file.write(str(obj) + "\n")
    player_file.write(str(params.player))
    player_file.close()
    object_file.close()


def game_quit():
    """
    функция обрабатывает закрытие окна игры
    :return:
    """
    save_game()
    pygame.quit()


def main():
    """
    основной цикл программы
    :return:
    """
    while not params.finished:
        if not params.game_started:
            open_start_menu()
        else:
            if not params.player_created:
                create_start_position()
            update_game(pygame.event)
        params.clock.tick(params.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                params.finished = True
    game_quit()


if __name__ == "__main__":
    params = Params()
    params.all_objects.append(objects.Objects(params.screen, "pics/cat.png", "name", 100, 100))
    main()
