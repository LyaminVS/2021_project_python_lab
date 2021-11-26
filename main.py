import pygame
import background
import map_logic
import menu
import objects
# import sound
import start_screen

pygame.init()


class Game:
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

        self.game_started = True
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

        self.map = [758, 2768]
        """
        показывает положение карты
        """

        self.inventory_opened = False
        """
        показывает открыт ли инвентарь
        """


def open_start_menu():
    """
    открывает стартовое меню игры
    """
    start_menu = start_screen.StartMenu(game.screen)
    start_menu.draw()


def line_to_object(line):
    """
    преобразовывает строку в объект класса Object
    :param line: строка файла
    :return:
    """

    name, image, x, y = line.split(";")
    new_object = objects.Objects(game.screen, image, name, int(x), int(y))
    return new_object


def line_to_player(line):
    """
    преобразовывает строку в объект класса Player
    :param line: строка файла
    :return:
    """
    name, image, x, y = line.split(";")
    new_player = objects.Objects(game.screen, image, name, int(x), int(y))
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
    # params.player = get_player_from_file()

    game.all_objects = get_obj_from_file()


def update_game(event):
    """
    функция обновляет состояние игры
    :return:
    """
    background.draw_map(game.screen, game.map[0], game.map[1], game.all_objects)
    game.player.draw()
    map_logic.event_checker(event.get(), game)
    if game.inventory_opened:
        game.player.inventory.int_update()


def save_game():
    """
    функция сохраняет игру
    :return:
    """
    player_file = open("player_save.txt", "w")
    object_file = open("objects_save.txt", "w")
    player_file.write(str(game.player) + "\n")
    for obj in game.all_objects:
        object_file.write(str(obj) + "\n")
    player_file.write(str(game.player))
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
    while not game.finished:
        pygame.display.update()
        if not game.game_started:
            open_start_menu()
        else:
            if not game.player_created:
                create_start_position()
                game.player_created = True
            update_game(pygame.event)
        game.clock.tick(game.FPS)

    game_quit()


if __name__ == "__main__":
    game = Game()
    game.player = objects.Player(game.screen, "name", 640, 360, menu.PlayerInventory(None))
    main()
