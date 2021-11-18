import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
tick = pygame.USEREVENT + 1
pygame.time.set_timer(tick, 1000)
# размеры инвентаря 640х576
# использую шрифт cambria, не уверен что он есть у всех и везде, без него очень плохо выглядят цифры
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (70, 70, 70)
GREY = (50, 50, 50)
DARK_GREY = (40, 40, 40)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
ORANGE = (220, 150, 40)  # цвет шрифта, но мне не нравится.
clock = pygame.time.Clock()


# testclass
class Redrect:
    def __init__(self, surface, image: str):
        self.amount = 15
        self.image = pygame.image.load(image)
        self.surface = surface
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.image.set_colorkey(WHITE)

    def draw(self, x, y):
        self.surface.blit(self.image, (x, y))


# Testclass

class OneInventorySlot:
    """
    отображение инвентаря
    """

    def __init__(self, x, y):
        self.one_inventory_slot_width = 64
        self.one_inventory_slot_height = 64
        self.one_slot_x = x
        self.one_slot_y = y
        self.color = LIGHT_GREY
        self.pressed = False
        self.one_inventory_slot_screen = pygame.Surface((self.one_inventory_slot_width, self.one_inventory_slot_height))
        self.font = pygame.font.SysFont('cambria', 14)
        self.words = ""
        self.words_place = []
        self.call = 0
        self.i = 0  # счетчик времени, отвечающий за время, которое слот горит серым от прикосновения
        self.moving_object_from_slot = False
        self.item = None

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
                    self.i += 1

    def amount_of_items(self, item):
        """
        Функция, отвечающая за отображение количества элементов в каждой ячейке.
        :param item: отображаемый объект
        """
        item_in_work = ""
        if self.item is not None:
            item_in_work = self.item
        elif item is not None:
            item_in_work = item
        else:
            pass

        self.words = self.font.render(str(item_in_work.amount), True, ORANGE)
        self.words_place = self.words.get_rect(
            topright=(self.one_inventory_slot_width - 5, 5))

        self.one_inventory_slot_screen.blit(self.words, self.words_place)

    def scaling_item(self, item):
        """
        Функция, отвечающая за скейлинг обьекта, чтобы он не вылезал за рамки ячейки.
        :param item: объект, которому необходимо изменить размер.
        """
        scale_item = pygame.transform.scale(item.image, (
            self.one_inventory_slot_width * 3 // 4, self.one_inventory_slot_height * 3 // 4))

        self.item.image = scale_item

    def display_item(self, item):
        """
        Функция, отвечающая за отображение объекта в ячейке
        :param item: отображаемый объект
        """
        if item is not None:
            self.item = item
            self.scaling_item(item)
            self.one_inventory_slot_screen.blit(self.item.image,
                                                (self.one_inventory_slot_width // 8,
                                                 self.one_inventory_slot_height // 8))

            self.amount_of_items(item)

    def rendering(self):  # не используется пока что
        """
        Функция, отвечающая за обновление экрана у инвентаря.
        """
        self.one_inventory_slot()
        screen.blit(self.one_inventory_slot_screen, (self.one_slot_x, self.one_slot_y))

    def update_one_inventory_slot(self, item=None):
        if self.i > 0:
            self.i += 1
        if self.i % 30 == 0:
            self.color = LIGHT_GREY
            self.pressed = False
            self.i = 0
        self.one_inventory_slot()
        if self.call == 0:
            self.display_item(item)
            self.call += 1
        else:
            self.display_item(self.item)
        screen.blit(self.one_inventory_slot_screen, (self.one_slot_x, self.one_slot_y))


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


class Craft(OneInventorySlot):
    """
    меню крафта
    """
    pass


class Inventory:
    def __init__(self, start_x, start_y, rows, columns, items=None):
        self.start_x = start_x
        self.start_y = start_y
        self.rows = rows
        self.columns = columns
        self.items = items
        self.slots = []
        self.moving_objects = []
        self.moving_object_from_slot = False
        self.i = 0  # счетчик времени, отвечающий за то сколько можно ли двигать обьект в инвентаре.
        # Если прошло 40 итераций, то можно

    def fill_up_inventory(self):
        i = 0

        for material in self.items:
            slot = self.slots[i]
            slot.update_one_inventory_slot(material)
            i += 1
            if i > len(self.slots):
                print("Инвентарь переполнен")

    def create_inventory(self):
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
        return self.slots

    def moving_objects_in_inventory(self):
        for slot in self.slots:
            if slot.pressed is True and slot.item is not None and slot.moving_object_from_slot is False \
                    and self.moving_object_from_slot is False and len(self.moving_objects) == 0:
                self.moving_objects.append(slot.item)
                slot.item = None
                self.moving_object_from_slot = True
                slot.moving_object_from_slot = True  # Странно наверное так делать, но что поделать
            if slot.pressed is True and slot.item is None and len(
                    self.moving_objects) > 0 and self.moving_object_from_slot is True \
                    and slot.moving_object_from_slot is False:
                slot.item = self.moving_objects[0]
                self.moving_objects.pop(0)
                slot.moving_object_from_slot = True
                self.i += 1
        return self.slots

    def update_inventory(self):
        if self.i > 0:
            self.i += 1
        if self.i % 30 == 0 and self.i != 0:
            self.moving_object_from_slot = False
            self.i = 0


finished = False
inv = OneInventorySlot(0, 0)
red1 = Redrect(inv.one_inventory_slot_screen, "cat.png")
red2 = Redrect(inv.one_inventory_slot_screen, "cat2.png")
red3 = Redrect(inv.one_inventory_slot_screen, "cat3.png")
materials = [red1, red3, red3, red2, red1, red1, red3]
inventory = Inventory(100, 100, 5, 7, materials)
slots = inventory.create_inventory()

while not finished:
    clock.tick(30)
    screen.fill(WHITE)
    inventory.update_inventory()
    for obj in slots:
        obj.update_one_inventory_slot()
        if inventory.moving_object_from_slot is False:
            obj.moving_object_from_slot = False
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION:
            for obj in slots:
                obj.slot_pressed(event)
                if obj.pressed is True:
                    print(obj.item, obj.moving_object_from_slot, obj.j)
    slots = inventory.moving_objects_in_inventory()
    pygame.display.update()
