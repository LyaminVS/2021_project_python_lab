import pygame


def event_checker(event_array, game):
    """
    Обработка нажатий мышью и на клавиатуру:
    1. Клавиши W, S, A, D - движение на шаг вверх,вниз,влево, 
    вправо соответственно
    2. клавиша P - пауза
    3. кнопка закрытия - выход из игры
    2. Клавиша E - открытие и закрытие общего инвентаря
    3. Нажатие на объект при неоткрытом общем инвентаре - 
    открытие инвентаря объекта
    4. клавиша ESCAPE - закрытие инвентаря объектов, общего
    5. передвижение мыши или отпускание клавиши - перезагрузка инвентаря
    6. Shift (левый) - удвоение скорости
    Args:
        event_array - массив событий для обработки
        game - аргумент, которому должно присвоиться значение объекта game класса Game
    """
    motion(game)
    for checked_event in event_array:
        if (checked_event.type == pygame.KEYDOWN) and (checked_event.key == pygame.K_e):
            game.inventory_opened = not game.inventory_opened
        elif checked_event.type == pygame.QUIT:
            game.finished = True
        elif checked_event.type == pygame.MOUSEBUTTONDOWN and not game.inventory_opened:
            pos = pygame.mouse.get_pos()
            for obj in game.all_objects:
                obj.collide_rect = pygame.Rect(-game.map[0] + obj.x, -game.map[1] + obj.y, obj.width, obj.height)
                if obj.collide_rect.collidepoint(pos):
                    obj.inventory_opened = True
        elif (checked_event.type == pygame.KEYDOWN) and (checked_event.key == pygame.K_ESCAPE):
            if game.player.inventory.building:
                game.player.inventory.building = False
            elif game.inventory_opened:
                game.inventory_opened = False
            else:
                for obj in game.all_objects:
                    obj.inventory_opened = False
        elif checked_event.type == pygame.MOUSEBUTTONUP or checked_event.type == pygame.MOUSEMOTION:
            if game.player.inventory.building:
                for square in game.grid:
                    square.is_button_pressed(checked_event)
            if game.inventory_opened:
                game.player.inventory.visual_update(checked_event)
            for obj in game.all_objects:
                if obj.inventory_opened:
                    obj.inventory.visual_update(checked_event)
        elif (checked_event.type == pygame.KEYDOWN) and (checked_event.key == pygame.K_p):
            game.pause_menu_opened = True


def map_collision(game):
    """
    Совершает предварительное перемещение на number_of_steps шагов вперёд, проверяет вышел ли за игрок границы карты,
    и в зависимости от данного факта присваевает нулевое значение составляющим
    скорости игрока, после этого возвращает в исходное до предварительного перемещения состояние.
    Args:
        game - аргумент, которому должно присвоиться значение объекта game класса Game
    """
    number_of_steps = 1
    game.map[0] += number_of_steps * game.player.vx
    if game.map[0] <= 0 or game.map[0] >= (game.map_dimensions[0] - 1280):
        game.map[0] -= number_of_steps * game.player.vx
        game.player.vx = 0
        game.player.right = 0
    else:
        game.map[0] -= number_of_steps * game.player.vx
    game.map[1] -= number_of_steps * game.player.vy
    if game.map[1] <= 0 or game.map[1] >= (game.map_dimensions[1] - 720):
        game.map[1] += number_of_steps * game.player.vy
        game.player.vy = 0
        game.player.up = 0
    else:
        game.map[1] += number_of_steps * game.player.vy


def objects_collision(game):
    """
    Совершает предварительное перемещение на number_of_steps шагов вперёд, проверяет столкнулся ли игрок с каким-то
    объектом, и в зависимости от данного факта присваевает нулевое значение составляющим
    скорости игрока, после этого возвращает в исходное до предварительного перемещения состояние.
    Args:
        game - аргумент, которому должно присвоиться значение объекта game класса Game
    """
    number_of_steps = 1
    for obj in game.all_objects:
        game.map[0] += number_of_steps * game.player.vx
        obj.collide_rect = pygame.Rect(-game.map[0] + obj.x, -game.map[1] + obj.y, obj.width, obj.height)
        if obj.collide_rect.colliderect(game.player.collide_rect):
            game.map[0] -= number_of_steps * game.player.vx
            game.player.vx = 0
            game.player.right = 0
        else:
            game.map[0] -= number_of_steps * game.player.vx
        game.map[1] -= number_of_steps * game.player.vy
        obj.collide_rect = pygame.Rect(-game.map[0] + obj.x, -game.map[1] + obj.y, obj.width, obj.height)
        if obj.collide_rect.colliderect(game.player.collide_rect):
            game.map[1] += number_of_steps * game.player.vy
            game.player.vy = 0
            game.player.up = 0
        else:
            game.map[1] += number_of_steps * game.player.vy
        game.map[0] += number_of_steps * game.player.vx
        game.map[1] -= number_of_steps * game.player.vy
        obj.collide_rect = pygame.Rect(-game.map[0] + obj.x, -game.map[1] + obj.y, obj.width, obj.height)
        if obj.collide_rect.colliderect(game.player.collide_rect):
            game.map[0] -= number_of_steps * game.player.vx
            game.player.vx = 0
            game.player.right = 0
            game.map[1] += number_of_steps * game.player.vy
            game.player.vy = 0
            game.player.up = 0
        else:
            game.map[0] -= number_of_steps * game.player.vx
            game.map[1] += number_of_steps * game.player.vy


def collision(game):
    """
    Обращает скорость в ноль при столкновении с объектами и границами карты
    Args:
        game - аргумент, которому должно присвоиться значение объекта game класса Game
    """
    map_collision(game)
    objects_collision(game)


def player_move(game):
    """
    Изменяет координату карты относительно экрана
    Args:
        game - аргумент, которому должно присвоиться значение объекта game класса Game
    """
    game.map[0] += game.player.vx
    game.map[1] -= game.player.vy
    game.player.vx = 0
    game.player.vy = 0


def keys_checker_general(game, keys, key1, key2, dimension, direction):
    """
    В зависимости от нажатых клавиш меняет скин и скорость игрока в общем случае
    Args:
        game - аргумент, которому должно присвоиться значение объекта game класса Game
        keys - массив нажатых клавиш
        key1 - клавиша 1 (w для вертикали и d для горизонтали)
        key2 - клавиша 2 (s для вертикали и a для горизонтали)
        dimension - значение скина (up/right)
        direction - направление движения 'x'/'y'
    """
    if keys[key1] and not keys[key2]:
        speed_dimension = game.player.v_max
        if dimension == 1:
            dimension = 2
        else:
            dimension = 1
    elif keys[key2] and not keys[key1]:
        speed_dimension = -game.player.v_max
        if dimension == -1:
            dimension = -2
        else:
            dimension = -1
    else:
        dimension = 0
        speed_dimension = 0
    if keys[pygame.K_LSHIFT]:
        speed_dimension *= 2
    if direction == 'x':
        game.player.vx = speed_dimension
        game.player.right = dimension
    elif direction == 'y':
        game.player.vy = speed_dimension
        game.player.up = dimension


def keys_checker(game):
    """
    В зависимости от нажатых клавиш меняет скин и скорость игрока
    Args:
        game - аргумент, которому должно присвоиться значение объекта game класса Game
    """
    keys = pygame.key.get_pressed()
    keys_checker_general(game, keys, pygame.K_d, pygame.K_a, game.player.right, 'x')
    keys_checker_general(game, keys, pygame.K_w, pygame.K_s, game.player.up, 'y')


def motion(game):
    """
    Проверяет зажатие клавиш, коллизию и передвигает игрока в случае надобности
    Args:
        game - аргумент, которому должно присвоиться значение объекта game класса Game
    """
    keys_checker(game)
    if game.player.vx != 0 or game.player.vy != 0:
        collision(game)
        player_move(game)


if __name__ == "__main__":
    print("This module is not for direct call!")
