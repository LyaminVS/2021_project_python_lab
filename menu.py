import pygame

import objects

pygame.init()
screen = pygame.display.set_mode((1280, 720))
# FIXME ОЧЕНЬ НАДО ДОБАВИТЬ В MAIN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
tick = pygame.USEREVENT + 1
pygame.time.set_timer(tick, 1000)
# FIXME использую шрифт cambria, не уверен что он есть у всех и везде, без него очень плохо выглядят цифры
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (70, 70, 70)
GREY = (50, 50, 50)
DARK_GREY = (40, 40, 40)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
ORANGE = (220, 150, 40)  # FIXME цвет шрифта, но мне не нравится.
clock = pygame.time.Clock()


class OneInventorySlot:
    """
    отображение ячейки инвентаря
    """

    def __init__(self, x, y):
        self.one_inventory_slot_width = self.one_inventory_slot_height = 64
        self.one_slot_x = x  # координата х левого верхнего угла у ячейки инвентаря.
        self.one_slot_y = y  # координата у левого верхнего угла у ячейки инвентаря.
        self.color = LIGHT_GREY  # цвет ячейки.
        self.pressed = False  # Нажата ли кнопка?
        self.one_inventory_slot_screen = pygame.Surface((self.one_inventory_slot_width, self.one_inventory_slot_height))
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
        pygame.draw.rect(self.one_inventory_slot_screen, self.color,
                         (0, 0, self.one_inventory_slot_width, self.one_inventory_slot_height))
        pygame.draw.rect(self.one_inventory_slot_screen, DARK_GREY,
                         (0, 0, self.one_inventory_slot_width, self.one_inventory_slot_height), 3)
        pygame.draw.rect(self.one_inventory_slot_screen, BLACK,
                         (0, 0, self.one_inventory_slot_width, self.one_inventory_slot_height), 1)
        pygame.draw.rect(self.one_inventory_slot_screen, BLACK,
                         (3, 3, self.one_inventory_slot_width - 6, self.one_inventory_slot_height - 6), 1)

    def slot_pressed(self, event):
        """
        Функция, меняющая цвет в зависимости от того навел ли игрок курсор на инвентарь или нажал на него.
        :param event: событие, чтобы определить игрок нажал на слот или навел курсор на него.
        :return: Если нажали на слот, то DARK_GREY, если навели курсор на слот, то GREY, если ничего, то LIGHT_GREY
        """

        if self.i % 60 != 0 or self.i == 0 and event.type != tick:
            if self.one_slot_x <= event.pos[0] <= self.one_slot_x + self.one_inventory_slot_width and \
                    self.one_slot_y <= event.pos[1] <= self.one_slot_y + self.one_inventory_slot_height:
                if event.type == pygame.MOUSEMOTION and self.pressed is False:
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
        if self.item is not None:
            item_in_work = self.item
        elif item is not None:
            item_in_work = item
        else:
            pass

        self.number = self.font.render(str(item_in_work.amount), True, ORANGE)
        self.number_place = self.number.get_rect(
            topright=(self.one_inventory_slot_width - 5, 5))
        self.one_inventory_slot_screen.blit(self.number, self.number_place)

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
        if item is not None:  # Если на вход подается непустой объект.
            self.item = item
            self.scaling_item(item)
            self.one_inventory_slot_screen.blit(self.item.image, (
                self.one_inventory_slot_width // 8, self.one_inventory_slot_height // 8))

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

        if self.call == 0:  # если ни разу не запускали и подаем объект, то работать будем с ним
            self.display_item(item)
            self.call += 1
        else:
            self.display_item(self.item)  # если уже запускали, то работаем с сохраненным объектом

        screen.blit(self.one_inventory_slot_screen, (self.one_slot_x, self.one_slot_y))


class Inventory:
    """
    Класс, отвечающий за создание инвентаря у объекта.
    """

    def __init__(self, start_x=100, start_y=100, rows=1, columns=1, items=None):
        self.start_x = start_x  # левая верхняя координата х первой ячейки инвентаря.
        self.start_y = start_y  # левая верхняя координата y первой ячейки инвентаря.
        self.rows = rows  # количество строк в инвентаре
        self.columns = columns  # количество столбцов в инвентаре
        self.items = items  # объекты, которые должны лежать в инвентаре. Можно ничего не подавать, по умолчанию None.
        self.slots = []  # информация о ячейках инвентаря.
        self.moving_object = None  # перемещаемый объект
        self.moving_object_from_slot = False  # Перемещается ли сейчас какой-то объект?
        self.i = 0  # счетчик времени, который говорит можно ли двигать обьект в инвентаре. Можно после 40 итераций.

    def fill_up_inventory(self):
        """
        Функция, отвечающая за наполнение инвентаря. Наполняет его элементами из self.items.
        """
        i = 0
        if self.items is not None:
            for material in self.items:
                slot = self.slots[i]
                material.surface = slot.one_inventory_slot_screen
                slot.update_one_inventory_slot(material)
                i += 1

    def create_inventory(self):
        """
        Функция, отвечающая за создание инвентаря у объекта в первый раз.
        """
        x = self.start_x
        y = self.start_y
        inventary_slot = OneInventorySlot(x, y)
        for i in range(self.columns):
            for j in range(self.rows):
                inventary_slot = OneInventorySlot(x, y)
                self.slots.append(inventary_slot)
                x += inventary_slot.one_inventory_slot_width
            x = self.start_x
            y += inventary_slot.one_inventory_slot_height
        self.fill_up_inventory()

    def moving_objects_in_inventory(self):
        """
        Функция, отвечающая за перемещение объектов внутри инвентаря.
        Для перемещения необходимо нажать левой кнопкой мыши на объект, который надо переместить и
        левой кнопкой мыши на ячейку, куда надо переместить.
        """
        for slot in self.slots:
            if slot.pressed is True and slot.item is not None and slot.moving_object_from_slot is False \
                    and self.moving_object_from_slot is False and self.moving_object is None:
                # Если пользователь хочет достать какой-то элемент из ячейки.
                self.moving_object = slot.item
                slot.item = None
                self.moving_object_from_slot = True
                slot.moving_object_from_slot = True  # Странно наверное так делать, но что поделать
            elif slot.pressed is True and slot.item is None and self.moving_object is not None \
                    and self.moving_object_from_slot is True and slot.moving_object_from_slot is False:
                # Если пользователь хочет положить объект, который достали в новую ячейку.
                slot.item = self.moving_object
                self.moving_object = None
                slot.moving_object_from_slot = True
                self.i += 1  # запускает счетчик итераций, который потом отключает статус того, что перемещается объект

    def update_inventory(self):
        """
        Функция, отвечающая за обновление инвентаря.
        """

        if self.i > 0:  # счетчик итераций. Включается в moving_objects_in_inventory
            self.i += 1
        if self.i % 21 == 0 and self.i != 0:
            self.moving_object_from_slot = False
            self.i = 0

        for obj in self.slots:
            obj.update_one_inventory_slot()
            if inventory.moving_object_from_slot is False:
                # Если закончилось перетаскивание объектов, то выключаем его всем ячейкам.
                obj.moving_object_from_slot = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION:
                for obj in self.slots:
                    obj.slot_pressed(event)
        self.moving_objects_in_inventory()  # двигаем объекты в инвентаре


class Craft(Inventory):
    """
    Класс, отвечающий за создание меню крафта.
    """

    def __init__(self, start_x, start_y, crafts):
        self.crafts = crafts # объекты, которые можно скрафтить.
        super().__init__(start_x, start_y, 3, 3, self.crafts)
        self.craft_items = [] #материалы, необходимые для крафта элемента, на который игрок нажал

    def updating(self):
        """
        Функция, занимающаяся обновлением меню крафта и обработкой нажатий игрока
        """
        for obj in self.slots:
            obj.update_one_inventory_slot()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION:
                for obj in self.slots:
                    obj.slot_pressed(event)
                    if obj.pressed is True:
                        for material in all_materials:
                            if obj.item.name == material.name:
                                self.craft_items = crafts[obj.item]


class PlayerInventory(OneInventorySlot):
    """
    инвентарь игрока и его отрисовка
    """
    pass


class ObjectInventory(OneInventorySlot):
    """
    инвентарь объектов
    """
    pass


finished = False

taco1 = objects.Taco(screen)
landau = objects.Landau(screen)
all_materials = [objects.Taco(screen), objects.Landau(screen)]  # FIXME Реально надо добавить в main, я не шучу...
materials = [taco1, landau]
crafts = {objects.Taco(screen): [2, objects.Landau], objects.Landau(screen): [5, objects.Taco]}

craft = Craft(400, 400, crafts)
craft.create_inventory()

inventory = Inventory(100, 100, 4, 3, materials)
inventory.create_inventory()

while not finished:
    clock.tick(45)
    screen.fill(WHITE)

    craft.updating()
    inventory.update_inventory()
    pygame.display.update()

#FIXME Заменить счетчики итераций на таймеры, иначе крафт и инвентарь одновременно не работают.