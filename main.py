import pygame
import background
import map_logic
import menu
import objects
# import sound
import start_screen
import os.path
import constants
import os
import shutil

pygame.init()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        """
        Холст для рисования
        """

        self.map_dimensions = [5120, 4320]
        """
        Размеры используемой карты
        """

        self.FPS = 30
        """
        Количество кадров в секунду
        """

        self.finished = False
        """
        False если программа завершена, иначе True
        """

        self.clock = pygame.time.Clock()
        """
        часы pygame
        """

        self.start_menu_opened = True
        """
        если была нажата кнопка старт на стартовом экране то True, иначе False
        """
        self.player_building = False
        """
        True если игрок запустил строительство, False если нет.
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

        self.map = [1500, 3000]  # было 758, 2986
        """
        показывает положение карты
        """
        self.inventory_opened = False
        """
        показывает открыт ли инвентарь
        """

        self.option_menu = start_screen.OptionMenu(self.screen)

        self.option_menu_opened = False

        self.start_menu = start_screen.StartMenu(self.screen)

        self.grid = background.create_grid(-self.map[0] + 1600, -self.map[1] + 3350, 2, 3, self.screen)
        """
        Сетка с местами, на которых можно строить
        """
        self.crafts = {
            objects.Taco(self.screen): [1, 2, "Landau", objects.Taco(self.screen)],
            objects.Landau(self.screen): [1, 3, "Taco", objects.Landau(self.screen)],
            objects.Brain(self.screen): [1, 5, "Taco", 5, "Landau", objects.Brain(self.screen)]
        }
        """
        словарь содержащий все рецепты крафта
        """
        self.builds = {
            objects.Palatka(self.screen): [1, 15, "Landau", objects.Palatka(self.screen)]
        }
        """
        словарь содержащий все рецепты строительства
        """

        self.timer = 0

        self.id = 0

        self.music = None

        self.pause_menu_opened = False

        self.pause_menu = start_screen.PauseMenu(self.screen)

    def set_building(self):
        for square in self.grid:
            if square.pressed_by_mouse and not square.building_on:
                image = pygame.image.load(self.player.inventory.building_pressed_item.image_name)
                width = image.get_width()
                height = image.get_height()
                collide_rect = pygame.Rect(square.x, square.y, width, height)
                if not collide_rect.colliderect(self.player.collide_rect):
                    new_object = objects.Objects(self.screen, self.player.inventory.building_pressed_item.image_name,
                                                 "shawarma_" + str(self.id), self.map[0] + square.x,
                                                 self.map[1] + square.y)
                    self.id += 1
                    square.pressed_by_mouse = False
                    new_object.resources = []
                    new_object.inventory = menu.ObjectInventory(self.screen, 100, 100, 4, 4)
                    print()
                    self.all_objects.append(new_object)
                    square.first_condition = self.player.inventory.building_pressed_item.image
                    square.second_condition = self.player.inventory.building_pressed_item.image

    def update_building_position(self):
        for square in self.grid:
            for obj in self.all_objects:
                if obj.x - 100 <= square.x + self.map[0] <= obj.x + 100 and \
                        obj.y - 100 <= square.y + self.map[1] <= obj.y + 100:
                    square.building_on = True

    def name_to_class(self, name):
        if name == "taco":
            return objects.Taco(self.screen)
        if name == "landau":
            return objects.Landau(self.screen)
        if name == "brain":
            return objects.Brain(self.screen)

    def line_to_object(self, line):
        """
        преобразовывает строку в объект класса Object
        :param line: строка файла
        :return:
        """

        name, image, x, y = line.split(";")
        resources_in_file = []
        if os.path.exists("save_files/object_inventory_save/" + name + ".txt"):
            resources_in_file = open("save_files/object_inventory_save/" + name + ".txt")
        resources = []
        for line in resources_in_file:
            line = line.strip()
            resources.append(self.name_to_class(line))
        new_object = objects.Objects(self.screen, image, name, int(x), int(y))
        new_object.resources = resources
        new_object.inventory = menu.ObjectInventory(self.screen, 100, 100, 4, 4, resources)
        return new_object

    def line_to_player(self, line):
        """
        преобразовывает строку в объект класса Player
        :param line: строка файла
        :return:
        """
        resources_in_file = open("save_files/player_resources_save")
        resources = []
        for resource in resources_in_file:
            resource = resource.strip()
            resources.append(self.name_to_class(resource))
        name, image, x, y = line.split(";")
        new_player = objects.Player(self.screen, name, int(x), int(y), resources)
        new_player.inventory = menu.PlayerInventory(self.screen, self.crafts, self.builds, resources)
        return new_player

    def get_player_from_file(self):
        """
        преобразовывает файл в объект класса Player
        :return: объект класса Player
        """
        player_file = open("save_files/player_save.txt")
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
        objects_in_file = open("save_files/objects_save.txt")
        for line in objects_in_file:
            new_obj = self.line_to_object(line)
            all_objects.append(new_obj)
        objects_in_file.close()
        return all_objects

    def get_map_from_file(self):
        map_array = []
        map_in_file = open("save_files/map_save.txt")
        for line in map_in_file:
            map_array.append(int(line))
        return map_array

    def get_id_from_file(self):
        id_in_file = open("save_files/id_save.txt")
        build_id = id_in_file.readline()
        id_in_file.close()
        return int(build_id)

    def create_start_position(self):
        """
        создается объект игрока, а также объекты зданий в первый кадр игры
        :return:
        """
        self.map = self.get_map_from_file()
        self.player = self.get_player_from_file()
        self.all_objects = self.get_obj_from_file()
        self.id = self.get_id_from_file()

    def update_game(self, event):
        """
        функция обновляет состояние игры
        :return:
        """
        self.update_building_position()
        background.draw_map(self.screen, self.map[0], self.map[1])
        background.change_coord_grid(self.grid, self.map[0], self.map[1], 2, 3)
        for square in self.grid:
            square.update()
        background.draw_objects(self.all_objects, self.map[0], self.map[1])

        if self.player.inventory.building:
            self.set_building()

        self.timer = (self.timer + 1) % self.FPS
        for obj in self.all_objects:
            if self.timer == self.FPS - 1:
                if (obj.name == "ksp" or obj.name.split("_")[0] == "shawarma") and len(obj.resources) < 16:
                    obj.resources.append(objects.Taco(self.screen))
            if obj.inventory_opened:
                obj.inventory.int_update(obj.resources)
        map_logic.event_checker(event.get(), self)

        self.player.draw()
        if self.inventory_opened:
            self.player.inventory.int_update()

    def save_game(self):
        """
        функция сохраняет игру
        :return:
        """
        shutil.rmtree("save_files")
        os.mkdir("save_files")
        os.mkdir("save_files/object_inventory_save")
        id_file = open("save_files/id_save.txt", "w")
        player_file = open("save_files/player_save.txt", "w")
        object_file = open("save_files/objects_save.txt", "w")
        player_resources_file = open("save_files/player_resources_save", "w")
        map_file = open("save_files/map_save.txt", "w")
        map_file.write(str(self.map[0]) + "\n" + str(self.map[1]))
        player_file.write(str(self.player) + "\n")
        for obj in self.all_objects:
            object_inventory_file = open("save_files/object_inventory_save/" + obj.name + ".txt", "w")
            for res in obj.resources:
                object_inventory_file.write((str(res.name)).lower() + "\n")
            object_file.write(str(obj) + "\n")
        for res in self.player.resources:
            player_resources_file.write((str(res.name)).lower() + "\n")
        id_file.write(str(self.id))
        player_resources_file.close()
        id_file.close()
        player_file.close()
        object_file.close()
        map_file.close()

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
        for square in self.grid:
            square.first_condition = pygame.image.load("pics/build grass.png")
            square.second_condition = pygame.image.load("pics/green.png")

        while not self.finished:
            if not self.player_created:
                self.create_start_position()
                self.player_created = True
            pygame.display.update()
            if self.start_menu_opened:
                self.screen.fill(constants.DARK_BLUE)
                self.finished, self.start_menu_opened, self.option_menu_opened = self.start_menu.draw()
                if self.option_menu_opened:
                    self.start_menu_opened = False
            elif self.option_menu_opened:
                self.screen.fill(constants.DARK_BLUE)
                self.finished, self.start_menu_opened, self.music = self.option_menu.draw()
                if self.start_menu_opened:
                    self.option_menu_opened = False
            elif self.pause_menu_opened:

                self.finished, self.pause_menu_opened, \
                    self.option_menu_opened, self.start_menu_opened = self.pause_menu.draw()
                if self.option_menu_opened or self.start_menu_opened:
                    self.pause_menu_opened = False
            else:
                self.update_game(pygame.event)
            self.clock.tick(self.FPS)
        self.game_quit()


if __name__ == "__main__":
    game = Game()
    game.main()
