import pygame
import os
import shutil
import background
import map_logic
import menu
import objects
import start_screen
import constants


pygame.init()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        """
        Холст для рисования
        """

        self.map_dimensions = [6120, 5320]
        """
        Размеры используемой карты
        """

        self.FPS = 60
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

        self.map = [1500, 3000]
        """
        показывает положение карты
        """
        self.inventory_opened = False
        """
        показывает открыт ли инвентарь
        """
        self.option_menu = start_screen.OptionMenu(self.screen)
        """
        содержит меню настроек 
        """
        self.option_menu_opened = False
        """
        True если меню настроек открыто, иначе False
        """
        self.start_menu = start_screen.StartMenu(self.screen)
        """
        содержит стартовое меню
        """
        self.grid = background.create_grid(-self.map[0] + 1600, -self.map[1] + 3350, 2, 3, self.screen)
        """
        Сетка с местами, на которых можно строить
        """
        self.crafts = {
            objects.Taco(self.screen): [1, 2, "Landau", objects.Taco(self.screen)],
            objects.Landau(self.screen): [1, 3, "Taco", objects.Landau(self.screen)],
            objects.Brain(self.screen): [2, 5, "Taco", 5, "Landau", objects.Brain(self.screen)]
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
        """
        таймер показывающий когда должны появиться новые ресурсы в зданиях
        """
        self.id = 0
        """
        содержит id следующего здания для строительства
        """
        self.music = None

        self.pause_menu_opened = False
        """
        True если открыто меню паузы иначе False
        """
        self.pause_menu = start_screen.PauseMenu(self.screen)
        """
        содержит меню паузы
        """
        self.new_game = False
        """
        True если начата новая игра иначе False
        """
        self.main_path = "new_save_files"
        """
        показывает папку из которой берутся сохранения
        """
        self.music_on = True
        """
        True если фоновая музыка включена иначе False
        """
        self.continue_game = False
        """
        True если продолжена игра иначе False
        """
        self.resources_for_repair = [1, 100, "Brain", None]

    def set_building(self):
        """
        Функция, отвечающая за постройку здания на карте.
        Здание не будет строиться если игрок стоит в зоне коллизии будущей постройки.
        """
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

                    self.all_objects.append(new_object)
                    square.first_condition = self.player.inventory.building_pressed_item.image
                    square.second_condition = self.player.inventory.building_pressed_item.image
                    game.player.inventory.building = False

    def update_building_position(self):
        """
        Обновляет координаты сетки и построек на них
        """
        for square in self.grid:
            for obj in self.all_objects:
                if obj.x - 100 <= square.x + self.map[0] <= obj.x + 100 and \
                        obj.y - 100 <= square.y + self.map[1] <= obj.y + 100:
                    square.building_on = True

    def name_to_class(self, name):
        """
        переводит строку в объект
        :param name: строка с названием объекта
        :return: объект с названием name
        """
        if name == "taco":
            return objects.Taco(self.screen)
        if name == "landau":
            return objects.Landau(self.screen)
        if name == "brain":
            return objects.Brain(self.screen)

    def line_to_object(self, line, objs):
        """
        преобразовывает строку в объект класса Object
        :param line: строка файла
        :param objs: переменная содержит уже созданные объекты
        :return:
        """

        name, image, x, y = line.split(";")
        resources_in_file = []
        if os.path.exists(self.main_path + "/object_inventory_save/" + name + ".txt"):
            resources_in_file = open(self.main_path + "/object_inventory_save/" + name + ".txt")
        resources = []
        amount = []
        for line in resources_in_file:
            line = line.split(";")
            amount.append(int(line[1]))
            resources.append(self.name_to_class(line[0]))
        new_object = objects.Objects(self.screen, image, name, int(x), int(y))
        is_same_building = False
        if objs:
            for obj in objs:
                if len(obj.name.split("_")) == 2 and len(new_object.name.split("_")) == 2 \
                        and obj.name.split("_")[1] == new_object.name.split("_")[1]:
                    new_object.resources = obj.resources
                    new_object.inventory = obj.inventory
                    is_same_building = True
        if not is_same_building:
            new_object.resources = resources
            new_object.inventory = menu.ObjectInventory(self.screen, 100, 100, 4, 4, resources, amount)
        return new_object

    def line_to_player(self, line):
        """
        преобразовывает строку в объект класса Player
        :param line: строка файла
        :return:
        """
        resources_in_file = open(self.main_path + "/player_resources_save")
        resources = []
        amount = []
        for resource in resources_in_file:
            resource = resource.split(";")
            material = resource[0].strip()
            amount.append(int(resource[1]))
            resources.append(self.name_to_class(material))
        name, image, x, y = line.split(";")
        new_player = objects.Player(self.screen, name, int(x), int(y), resources)
        new_player.inventory = menu.PlayerInventory(self.screen, self.crafts, self.builds, resources, amount)
        return new_player

    def get_player_from_file(self):
        """
        преобразовывает файл в объект класса Player
        :return: объект класса Player
        """
        player_file = open(self.main_path + "/player_save.txt")
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
        objects_in_file = open(self.main_path + "/objects_save.txt")
        for line in objects_in_file:
            new_obj = self.line_to_object(line, all_objects)
            all_objects.append(new_obj)
        objects_in_file.close()
        return all_objects

    def get_map_from_file(self):
        """
        функция получает координаты игрока из файла map_save.txt
        :return: координаты игрока
        """
        map_array = []
        map_in_file = open(self.main_path + "/map_save.txt")
        for line in map_in_file:
            map_array.append(int(line))
        return map_array

    def get_id_from_file(self):
        """
        функция получает id последней постройки из файла id_save.txt
        :return: id последней постройки
        """

        id_in_file = open(self.main_path + "/id_save.txt")
        build_id = id_in_file.readline()
        id_in_file.close()
        return int(build_id)

    def create_start_position(self):
        """
        достает из файлов начальное состояние игрока карты, объектов и т д
        """
        self.map = self.get_map_from_file()
        self.player = self.get_player_from_file()
        self.all_objects = self.get_obj_from_file()
        self.id = self.get_id_from_file()
        for square in self.grid:
            square.first_condition = pygame.image.load("pics/build grass.png")
            square.second_condition = pygame.image.load("pics/build grass chosen.png")

    def repair_buildings(self):
        """
        функция проверяет хватает ли ресурсов для починки зданий и вычитает ресурсы если они необходимы для ремонта
        """
        for obj in self.all_objects:
            if menu.resource_checker(self.resources_for_repair, obj.inventory.slots) and obj.image_name.find("shadow_"):
                obj.image_name = obj.image_name.replace("shadow_", "")
                obj.image = pygame.image.load(obj.image_name).convert_alpha()
        for obj in self.all_objects:
            if menu.resource_checker(self.resources_for_repair, obj.inventory.slots) and obj.image_name.find("shadow_"):
                for slot in obj.inventory.slots:
                    if slot.item and slot.item.name == self.resources_for_repair[2]:
                        slot.item.amount -= self.resources_for_repair[1]

    def add_resources(self):
        """
        добавляет ресурсы в ksp и shawarma
        """
        self.timer += 1
        self.timer = self.timer % (3 * self.FPS)
        for obj in self.all_objects:
            if self.timer == 3 * self.FPS - 1:

                if (obj.name == "ksp" or obj.name.split("_")[0] == "shawarma") and len(obj.resources) < 16:
                    obj.resources.append(objects.Taco(self.screen))
                if obj.name == "ksp" and not obj.image_name.find("shadow_") and len(obj.resources) < 16:
                    obj.resources.append(objects.Taco(self.screen))

            if obj.inventory_opened:
                obj.inventory.int_update(obj.resources)

    def update_game(self, event):
        """
        функция отрисовывает игрока, карту, объекты на ней, места для сторительства, проверяет починку зданий
        :return:
        """
        self.repair_buildings()
        self.update_building_position()
        background.draw_map(self.screen, self.map[0], self.map[1])
        background.change_coord_grid(self.grid, self.map[0], self.map[1], 3)
        for square in self.grid:
            square.update()
        background.draw_objects(self.all_objects, self.map[0], self.map[1])
        if self.player.inventory.building:
            self.set_building()
        self.add_resources()
        map_logic.event_checker(event.get(), self)
        self.player.draw()
        if self.inventory_opened:
            self.player.inventory.int_update()

    def save_game(self):
        """
        функция сохраняет игрока, его инвентарь, объекты, инвентари объектов, id последнего построенного здания и
        положение игрока
        :return:
        """
        if os.path.exists("save_files"):
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
            obj.resources, amount = obj.inventory.objects_in_inventory()
            object_inventory_file = open("save_files/object_inventory_save/" + obj.name + ".txt", "w")
            number = 0
            for res in obj.resources:
                object_inventory_file.write((str(res.name)).lower() + ";" + str(amount[number]) + "\n")
                number += 1
            object_file.write(str(obj) + "\n")
        self.player.resources, player_amount = self.player.inventory.inventory.objects_in_inventory()
        number = 0
        for res in self.player.resources:
            player_resources_file.write((str(res.name)).lower() + ";" + str(player_amount[number]) + "\n")
            number += 1
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
        if self.player is not None:
            self.save_game()
        pygame.quit()

    def main(self):
        """
        основной цикл программы
        функция управляет открытием и закрытием различных окон меню (start_screen, pause_menu, option_menu, game)
        :return:
        """
        pygame.mixer.music.load("music/background_music.mp3")
        pygame.mixer.music.play(-1)
        while not self.finished:
            pygame.display.update()
            if self.start_menu_opened:
                self.screen.fill(constants.DARK_BLUE)
                self.finished, self.continue_game, self.option_menu_opened, self.new_game = self.start_menu.draw()
                if self.option_menu_opened or self.continue_game or self.new_game:
                    self.start_menu_opened = False
                if self.continue_game and os.path.exists("save_files"):
                    self.main_path = "save_files"
                if not self.player_created and (self.new_game or self.continue_game):
                    self.create_start_position()
                    self.update_game(pygame.event)
                    self.player_created = True
            elif self.option_menu_opened:
                self.screen.fill(constants.DARK_BLUE)
                self.finished, self.start_menu_opened, self.music = self.option_menu.draw()
                if self.start_menu_opened:
                    self.option_menu_opened = False
                if self.music:
                    self.music_on = not self.music_on
                    if self.music_on:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
            elif self.pause_menu_opened:
                self.finished, self.pause_menu_opened, self.option_menu_opened, self.start_menu_opened = \
                    self.pause_menu.draw()
                if self.option_menu_opened or self.start_menu_opened:
                    self.pause_menu_opened = False
            else:

                self.update_game(pygame.event)
            self.clock.tick(self.FPS)
        self.game_quit()


if __name__ == "__main__":
    game = Game()
    game.main()
