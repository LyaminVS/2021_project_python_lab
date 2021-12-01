import pygame


def event_checker(event_array, game):
    """
    Обработка нажатий мышью и на клавиатуру
    Args:
    event_array - массив событий для обработки
    game - params из модуля main
    """
    for checked_event in event_array:
        if (checked_event.type == pygame.KEYDOWN) and (checked_event.key == pygame.K_e):
            game.inventory_opened = not game.inventory_opened
        if checked_event.type == pygame.QUIT:
            game.finished = True
        if checked_event.type == pygame.KEYUP:
            game.player.move = 0
        if pygame.key.get_pressed()[pygame.K_w]:
            game.player.vy = 2
            if game.player.up == 1:
                game.player.up = 2
            else:
                game.player.up = 1
        if pygame.key.get_pressed()[pygame.K_s]:
            game.player.vy = -2
            if game.player.up == -1:
                game.player.up = -2
            else:
                game.player.up = -1
        if pygame.key.get_pressed()[pygame.K_s] and pygame.key.get_pressed()[pygame.K_w]:
            game.player.vy = 0
            game.player.up = 0
        if pygame.key.get_pressed()[pygame.K_d]:
            game.player.vx = 2
            if game.player.right == 1:
                game.player.right = 2
            else:
                game.player.right = 1
        if pygame.key.get_pressed()[pygame.K_a]:
            game.player.vx = -2
            if game.player.right == -1:
                game.player.right = -2
            else:
                game.player.right = -1
        if pygame.key.get_pressed()[pygame.K_d] and pygame.key.get_pressed()[pygame.K_a]:
            game.player.vx = 0
            game.player.right = 0
        if game.player.vx == 0:
            game.player.right = 0
        if game.player.vy == 0:
            game.player.up = 0
        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            game.player.vx *= 2
            game.player.vy *= 2
        if checked_event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for obj in game.all_objects:
                if obj.x < pos[0] + game.map[0] < obj.x + obj.width and obj.y < pos[1] + game.map[1] < obj.y + obj.height:
                    obj.inventory_opened = True
        elif checked_event.type == pygame.MOUSEBUTTONUP or checked_event.type == pygame.MOUSEMOTION:
            game.player.inventory.visual_update(checked_event)
        if game.player.vx != 0 or game.player.vy != 0:
            collision(game)
            player_move(game)
        # for obj in game.all_objects:
        #     if obj.inventory_opened:
        #         obj.inventory.visual_update(pygame.event)

        
def collision(game):
    """
    Совершает предварительное перемещение на number_of_steps шагов вперёд, проверяет столкнулся ли игрок с каким-то
    объектом или вышел ли за границы карты, и в зависимости от данного факта присваевает нулевое значение составляющим
    скорости игрока, после этого возвращает в исходное до предварительного перемещения состояние.
    Args:
        game - аргумент, которому должно присвоиться значение объекта game класса Game
    """
    number_of_steps = 1
    game.map[0] += number_of_steps * game.player.vx
    if game.map[0] <= 0 or game.map[0] >= (5120-1280):
        game.map[0] -= number_of_steps * game.player.vx
        game.player.vx = 0
        game.player.right = 0
    else:
        game.map[0] -= number_of_steps * game.player.vx
    game.map[1] -= number_of_steps * game.player.vy
    if game.map[1] <= 0 or game.map[1] >= (5040-720):
        game.map[1] += number_of_steps * game.player.vy
        game.player.vy = 0
        game.player.up = 0
    else:
        game.map[1] += number_of_steps * game.player.vy
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


def player_move(game):
    """
    Изменяет координату объекта относительно экрана и студента относительно карты
    Args:
    game - params из модуля main
    """
    game.map[0] += game.player.vx
    game.map[1] -= game.player.vy
    game.player.vx = 0
    game.player.vy = 0
