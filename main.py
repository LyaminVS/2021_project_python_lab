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

        self.map = [758, 2768]
        """
        показывает положение карты
        """

        self.inventory_opened = False
        """
        показывает открыт ли инвентарь
        """

        self.option_menu = False

        self.start_menu = start_screen.StartMenu()

        self.crafts = {objects.Taco(self.screen): [2, objects.Landau], objects.Landau(self.screen): [5, objects.Taco]}

    def line_to_object(self, line):
        """
        преобразовывает строку в объект класса Object
        :param line: строка файла
        :return:
        """

        name, image, x, y = line.split(";")
        new_object = objects.Objects(self.screen, image, name, int(x), int(y))
        return new_object

    def line_to_player(self, line):
        """
        преобразовывает строку в объект класса Player
        :param line: строка файла
        :return:
        """
        name, image, x, y = line.split(";")
        new_player = objects.Objects(self.screen, image, name, int(x), int(y))
        return new_player

    def get_player_from_file(self):
        """
        преобразовывает файл в объект класса Player
        :return: объект класса Player
        """
        player_file = open("player_save.txt")
        player_line = player_file.readline()
        player = self.line_to_player(player_line)
        player_file.close()
        return player

    def get_obj_from_file(self):
        """
        преобразовывает файла в объект класса Object
        :return: массив объектов класса Object
        """
        all_objects = []
        objects_in_file = open("objects_save.txt")
        for line in objects_in_file:
            new_obj = self.line_to_object(line)
            all_objects.append(new_obj)
        objects_in_file.close()
        return all_objects

    def create_start_position(self):
        """
        создается объект игрока, а также объекты зданий в первый кадр игры
        :return:
        """
        # params.player = get_player_from_file()

        self.all_objects = self.get_obj_from_file()

    def update_game(self, event):
        """
        функция обновляет состояние игры
        :return:
        """
        background.draw_map(self.screen, self.map[0], self.map[1], self.all_objects)
        self.player.draw()
        map_logic.event_checker(event.get(), self)
        if self.inventory_opened:
            self.player.inventory.int_update()

    def save_game(self):
        """
        функция сохраняет игру
        :return:
        """
        player_file = open("player_save.txt", "w")
        object_file = open("objects_save.txt", "w")
        player_file.write(str(self.player) + "\n")
        for obj in self.all_objects:
            object_file.write(str(obj) + "\n")
        player_file.write(str(self.player))
        player_file.close()
        object_file.close()

    def game_quit(self):
        """
        функция обрабатывает закрытие окна игры
        :return:
        """
        self.save_game()
        pygame.quit()

    def main(self):
        """
        основной цикл программы
        :return:
        """
        while not self.finished:
            pygame.display.update()
            if not self.game_started:
                self.screen.fill((255, 255, 255))
                self.finished, self.game_started, self.option_menu = self.start_menu.draw()
                map_logic.event_checker(pygame.event.get(), self)
            else:
                if not self.player_created:
                    self.create_start_position()
                    self.player_created = True
                self.update_game(pygame.event)
            self.clock.tick(self.FPS)
        self.game_quit()


if __name__ == "__main__":
    game = Game()
    game.player = objects.Player(game.screen, "name", 640, 360,
                                 menu.PlayerInventory(game.screen, game.crafts, [objects.Taco(game.screen), objects.Landau(game.screen)]))
    game.main()
