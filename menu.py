import pygame
import copy



# FIXME использую шрифт cambria, не уверен что он есть у всех и везде, без него очень плохо выглядят цифры
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (70, 70, 70)
GREY = (50, 50, 50)
DARK_GREY = (40, 40, 40)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
ORANGE = (220, 150, 40)  # FIXME цвет шрифта, но мне не нравится.


class OneInventorySlot:
    """
    отображение ячейки инвентаря
    """

    def __init__(self, x, y, screen):
        self.one_inventory_slot_width = self.one_inventory_slot_height = 64
        self.one_slot_x = x  # координата х левого верхнего угла у ячейки инвентаря.
        self.one_slot_y = y  # координата у левого верхнего угла у ячейки инвентаря.
        self.color = LIGHT_GREY  # цвет ячейки.
        self.pressed = False  # Нажата ли кнопка?
        self.screen = screen
        # экран, на который отрисовывается ячейка инвентаря.
        self.font = pygame.font.SysFont('cambria', 14)  # шрифт для счетчика количества предметов.
        self.number = ""  # текстовый вариант количества предметов в ячейке.
        self.number_place = None  # поверхность, на которой отрисуются числа.
        self.call = 0  # количество раз, когда была вызвана ячейка инвентаря.
        self.i = 0  # счетчик времени, отвечающий за время, которое слот горит серым от прикосновения.
        self.moving_object_from_slot = False  # Был ли из ячейки/в ячейку недавно перемещен объект.
        self.item = None  # объект, который лежит в ячейке.

    def one_inventory_slot(self):
        """
        Функция, отрисовывающая одну ячейку инвентаря.
        """
        pygame.draw.rect(self.screen, self.color, (
            self.one_slot_x, self.one_slot_y, self.one_inventory_slot_width, self.one_inventory_slot_height))
        pygame.draw.rect(self.screen, DARK_GREY, (
            self.one_slot_x, self.one_slot_y, self.one_inventory_slot_width, self.one_inventory_slot_height), 3)
        pygame.draw.rect(self.screen, BLACK, (
            self.one_slot_x, self.one_slot_y, self.one_inventory_slot_width, self.one_inventory_slot_height), 1)
        pygame.draw.rect(self.screen, BLACK, (
            3 + self.one_slot_x, 3 + self.one_slot_y, self.one_inventory_slot_width - 6,
            self.one_inventory_slot_height - 6), 1)

    def slot_pressed(self, event):
        """
        Функция, меняющая цвет в зависимости от того навел ли игрок курсор на инвентарь или нажал на него.
        :param event: событие, чтобы определить игрок нажал на слот или навел курсор на него.
        :return: Если нажали на слот, то DARK_GREY, если навели курсор на слот, то GREY, если ничего, то LIGHT_GREY
        """

        if self.i // 60 == 0 or self.i == 0:
            if self.one_slot_x <= event.pos[0] <= self.one_slot_x + self.one_inventory_slot_width and \
                    self.one_slot_y <= event.pos[1] <= self.one_slot_y + self.one_inventory_slot_height:
                if event.type == pygame.MOUSEMOTION and not self.pressed:
                    self.color = GREY
                    self.i += 1
                else:
                    self.color = DARK_GREY
                    self.pressed = True
                    self.i += 1  # запускает таймер возврата LIGHT_GREY цвета.

    def amount_of_items(self, item):
        """
        Функция, отвечающая за отображение количества элементов в каждой ячейке.
        :param item: отображаемый объект
        """
        item_in_work = ""  # объект, с которым будем работать. Если в ячейке что-то лежит, то работает с self.item,
        # если ячейка пустая и туда подается объект, то работаем с новым объектом,
        # если ничего не лежит и ничего не подается, то пропускаем.
        if self.item:
            item_in_work = self.item
        elif item:
            item_in_work = item
        else:
            pass

        self.number = self.font.render(str(item_in_work.amount), True, ORANGE)
        self.number_place = self.number.get_rect(
            topright=(self.one_slot_x + self.one_inventory_slot_width - 5, self.one_slot_y + 5))
        self.screen.blit(self.number, self.number_place)

    def scaling_item(self, item):
        """
        Функция, отвечающая за скейлинг обьекта, чтобы он не вылезал за рамки ячейки.
        :param item: объект, которому необходимо изменить размер.
        """
        scale_item = pygame.transform.scale(item.image, (
            self.one_inventory_slot_width * 3 // 4, self.one_inventory_slot_height * 3 // 4))

        self.item.image = scale_item  # картинка объекта становится сжатым

    def display_item(self, item):
        """
        Функция, отвечающая за отображение объекта в ячейке
        :param item: отображаемый объект
        """
        if item:  # Если на вход подается непустой объект.
            self.item = item
            self.scaling_item(item)
            self.screen.blit(self.item.image, (
                self.one_slot_x + self.one_inventory_slot_width // 8,
                self.one_slot_y + self.one_inventory_slot_height // 8))

            self.amount_of_items(item)

    def update_one_inventory_slot(self, item=None):
        """
        Функция, отвечающая за обновление инвентаря
        :param item: объект, который необходимо поместить в ячейку
        """
        if self.i > 0:  # таймер итераций, запускается в slot_pressed
            self.i += 1
        if self.i % 20 == 0:
            self.color = LIGHT_GREY
            self.pressed = False
            self.i = 0

        self.one_inventory_slot()
        if self.item and self.item.amount == 0:
            self.item = None
        if self.call == 0:  # если ни разу не запускали и подаем объект, то работать будем с ним
            self.display_item(item)
            self.call += 1
        else:
            self.display_item(self.item)  # если уже запускали, то работаем с сохраненным объектом


class Inventory:
    """
    Класс, отвечающий за создание инвентаря у объекта.
    """

    def __init__(self, screen, start_x=100, start_y=100, rows=1, columns=1, items=None, ):
        self.start_x = start_x  # левая верхняя координата х первой ячейки инвентаря.
        self.start_y = start_y  # левая верхняя координата y первой ячейки инвентаря.
        self.rows = rows  # количество строк в инвентаре
        self.columns = columns  # количество столбцов в инвентаре
        self.items = items  # объекты, которые должны лежать в инвентаре. Можно ничего не подавать, по умолчанию None.
        self.slots = []  # информация о ячейках инвентаря.
        self.moving_object = None  # перемещаемый объект
        self.moving_object_from_slot = False  # Перемещается ли сейчас какой-то объект?
        self.i = 0  # счетчик времени, который говорит можно ли двигать обьект в инвентаре. Можно после 40 итераций.
        self.screen = screen
        self.create_inventory()

    def fill_up_inventory(self, items):
        """
        Функция, отвечающая за наполнение инвентаря. Наполняет его элементами из self.items.
        """
        i = 0
        if items:
            for material in items:
                slot = self.slots[i]
                material.surface = slot.screen
                slot.update_one_inventory_slot(material)
                i += 1

    def create_inventory(self):
        """
        Функция, отвечающая за создание инвентаря у объекта в первый раз.
        """
        x = self.start_x
        y = self.start_y
        inventary_slot = OneInventorySlot(x, y, self.screen)
        for i in range(self.columns):
            for j in range(self.rows):
                inventary_slot = OneInventorySlot(x, y, self.screen)
                self.slots.append(inventary_slot)
                x += inventary_slot.one_inventory_slot_width
            x = self.start_x
            y += inventary_slot.one_inventory_slot_height
        self.fill_up_inventory(self.items)

    def moving_objects_in_inventory(self):
        """
        Функция, отвечающая за перемещение объектов внутри инвентаря.
        Для перемещения необходимо нажать левой кнопкой мыши на объект, который надо переместить и
        левой кнопкой мыши на ячейку, куда надо переместить.
        """
        for slot in self.slots:
            if slot.pressed and slot.item and not slot.moving_object_from_slot \
                    and not self.moving_object_from_slot and not self.moving_object:
                # Если пользователь хочет достать какой-то элемент из ячейки.
                self.moving_object = slot.item
                slot.item = None
                self.moving_object_from_slot = True
                slot.moving_object_from_slot = True  # Странно наверное так делать, но что поделать
            elif slot.pressed and not slot.item and self.moving_object \
                    and self.moving_object_from_slot and not slot.moving_object_from_slot:
                # Если пользователь хочет положить объект, который достали в новую ячейку.
                slot.item = self.moving_object
                self.moving_object = None
                slot.moving_object_from_slot = True
                self.i += 1  # запускает счетчик итераций, который потом отключает статус того, что перемещается объект
            elif slot.pressed and slot.item and self.moving_object and slot.item.name == self.moving_object.name \
                    and self.moving_object_from_slot and not slot.moving_object_from_slot:
                slot.item.amount += self.moving_object.amount
                self.moving_object = None
                slot.moving_object_from_slot = True
                self.i += 1


class ObjectInventory(Inventory):
    """
    инвентарь объектов
    """

    def __init__(self, screen, start_x=100, start_y=100, rows=1, columns=1, items=None):
        super().__init__(screen, start_x, start_y, rows, columns, items)

    def visual_update(self, event):
        for obj in self.slots:
            obj.slot_pressed(event)
        self.moving_objects_in_inventory()

    def int_update(self, items=None):
        if not items:
            items = []
        if self.i > 0:  # счетчик итераций. Включается в moving_objects_in_inventory
            self.i += 1
        if self.i % 41 == 0 and self.i != 0:
            self.moving_object_from_slot = False
            self.i = 0
        for obj in self.slots:
            obj.update_one_inventory_slot()
            if not self.moving_object_from_slot:
                # Если закончилось перетаскивание объектов, то выключаем его всем ячейкам.
                obj.moving_object_from_slot = False
        self.fill_up_inventory(items)

    def update(self, items=None):
        """
        Функция, отвечающая за обновление инвентаря.
        """
        self.int_update(items)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION:
                self.visual_update(event)


class Make(Inventory):
    """
    Класс, отвечающий за создание меню крафта.
    """

    def __init__(self, screen, start_x, start_y, rows, columns, makes):
        self.makes = makes  # объекты, которые можно скрафтить.
        super().__init__(screen, start_x, start_y, rows, columns, self.makes)
        self.making_items = []  # материалы, необходимые для крафта элемента, на который игрок нажал

    def int_update(self, font_size=64, text="craft"):
        pygame.draw.rect(self.screen, LIGHT_GREY, (self.start_x, self.start_y - 64, self.rows * 64, 64))
        pygame.draw.rect(self.screen, BLACK, (self.start_x, self.start_y - 64, self.rows * 64, 64), 1)
        pygame.draw.rect(self.screen, BLACK, (self.start_x + 3, self.start_y - 64 + 3, self.rows * 64 - 6, 64 - 6),
                         1)
        font = pygame.font.SysFont("Arial", font_size)
        words = font.render(text, True, (0, 0, 0))
        place = words.get_rect(center=(self.start_x + self.rows * 32, self.start_y - 32))
        self.screen.blit(words, place)
        for obj in self.slots:
            obj.update_one_inventory_slot()

    def visual_update(self, event):
        for obj in self.slots:
            obj.slot_pressed(event)
            if obj.pressed and obj.item and event.type != pygame.MOUSEMOTION:
                self.making_items = self.makes[obj.item]

    def update(self):
        """
        Функция, занимающаяся обновлением меню крафта и обработкой нажатий игрока
        """
        self.int_update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION:
                self.visual_update(event)


class Craft(Make):
    def __init__(self, screen, start_x, start_y, crafts):
        super(Craft, self).__init__(screen, start_x, start_y, 3, 3, crafts)

    def int_update(self, font_size=64, text="craft"):
        super().int_update(font_size, text)


class Build(Make):
    def __init__(self, screen, start_x, start_y, builds):
        super(Build, self).__init__(screen, start_x, start_y, 3, 2, builds)

    def int_update(self, font_size=64, text="Build"):
        super().int_update(font_size, text)


class PlayerInventory:
    """
    инвентарь игрока и его отрисовка
    """

    def __init__(self, screen, crafts, builds, materials=None):
        self.screen = screen
        self.inventory = ObjectInventory(screen, 500, 100, 7, 7, materials)
        self.craft_inventory = Craft(screen, 948, 164, crafts)
        self.build_inventory = Build(screen, 948, 420, builds)
        self.font_size = 64
        self.text = "craft"
        self.building = False  # Строит ли игрок сейчас?
        self.pressed_building = None
        self.building_pressed_item = None
        self.building_surface = None

    def craft_items(self):
        crafted_items = self.craft_inventory.making_items.copy()
        resource_checker = 0

        for i in range(2, len(crafted_items), 2):
            self.font_size = 64
            self.text = "craft"
            for slot in self.inventory.slots:
                if slot.item and slot.item.name == crafted_items[i] and slot.item.amount >= crafted_items[i - 1]:
                    resource_checker += 1
        if crafted_items and resource_checker >= (len(crafted_items) - 1) // 2:
            amount = crafted_items[0]
            for slot in self.inventory.slots:
                for i in range(2, len(crafted_items), 2):
                    if slot.item and crafted_items[-1] and slot.item.name == crafted_items[-1].name:
                        slot.item.amount += crafted_items[0]
                        crafted_items[-1] = None
                    elif slot.item and slot.item.name == crafted_items[i] and slot.item.amount >= crafted_items[i - 1]:
                        slot.item.amount -= crafted_items[i - 1]
                        crafted_items[i - 1] = 0
                    elif not slot.item:
                        slot.item = copy.copy(crafted_items[-1])
                        crafted_items[-1] = None
                        if slot.item:
                            slot.item.amount = amount
        elif crafted_items:
            self.font_size = 20
            self.text = "not enough materials"
        self.craft_inventory.making_items = []

    def animation(self, event, pressed_item):
        mouse_x = event.pos[0]
        mouse_y = event.pos[1]

        if pressed_item != self.building_pressed_item:
            scaling = 0
        else:
            scaling = 1

        if pressed_item and scaling == 0:
            self.building_pressed_item = copy.copy(pressed_item)
            self.building_pressed_item.image = pygame.transform.scale(pressed_item.image,
                                                                      (pressed_item.width, pressed_item.height))
        self.building_surface = self.building_pressed_item.image.get_rect(center=(mouse_x, mouse_y))

    def build_items(self):
        for slot in self.build_inventory.slots:
            if slot.pressed and slot.item:
                self.building = True
                self.pressed_building = slot.item

    def int_update(self, items=None):
        if not items:
            items = []
        if not self.building:
            self.craft_inventory.int_update(self.font_size, self.text)
            self.build_inventory.int_update()
            self.craft_items()
            self.build_items()
            self.inventory.int_update(items)
        elif self.building_pressed_item:
            for slot in self.build_inventory.slots:
                slot.pressed = False
            self.screen.blit(self.building_pressed_item.image, self.building_surface)

    def visual_update(self, event):

        if not self.building:
            self.craft_inventory.visual_update(event)
            self.build_inventory.visual_update(event)
            self.inventory.visual_update(event)
        else:
            if event.type == pygame.MOUSEMOTION:
                self.animation(event, self.pressed_building)

    def update_all(self, items):
        self.int_update(items)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION:
                self.inventory.visual_update(event)
                self.craft_inventory.visual_update(event)
