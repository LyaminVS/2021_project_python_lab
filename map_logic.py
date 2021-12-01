import pygame

motion_keys_numbers = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]


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
        if pygame.key.get_pressed() not in motion_keys_numbers:
            game.player.up = 0
            game.player.right = 0
        if pygame.key.get_pressed()[pygame.K_w]:
            game.player.vy = 2
        if pygame.key.get_pressed()[pygame.K_s]:
            game.player.vy = -2
        if pygame.key.get_pressed()[pygame.K_s] and pygame.key.get_pressed()[pygame.K_w]:
            game.player.vy = 0
        if pygame.key.get_pressed()[pygame.K_d]:
            game.player.vx = 2
        if pygame.key.get_pressed()[pygame.K_a]:
            game.player.vx = -2
        if pygame.key.get_pressed()[pygame.K_d] and pygame.key.get_pressed()[pygame.K_a]:
            game.player.vx = 0
        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            game.player.vx *= 2
            game.player.vy *= 2
        elif checked_event.type == pygame.MOUSEBUTTONUP or checked_event.type == pygame.MOUSEMOTION:
            game.player.inventory.visual_update(checked_event)
        if game.player.vx != 0 or game.player.vy != 0:
            collision(game)
            player_move(game)


def collision(game):
    """
    расчитывает коллизию
    """
    for obj in game.all_objects:
        number_of_steps = max(abs(game.player.vx), abs(game.player.vy))
        game.map[0] += number_of_steps * game.player.vx
        obj.collide_rect = pygame.Rect(-game.map[0] + obj.x, -game.map[1] + obj.y, obj.width, obj.height)
        if obj.collide_rect.colliderect(game.player.collide_rect):
            game.map[0] -= number_of_steps * game.player.vx
            game.player.vx = 0
        else:
            game.map[0] -= number_of_steps * game.player.vx
        game.map[1] -= number_of_steps * game.player.vy
        obj.collide_rect = pygame.Rect(-game.map[0] + obj.x, -game.map[1] + obj.y, obj.width, obj.height)
        if obj.collide_rect.colliderect(game.player.collide_rect):
            game.map[1] += number_of_steps * game.player.vy
            game.player.vy = 0
        else:
            game.map[1] += number_of_steps * game.player.vy
        game.map[0] += number_of_steps * game.player.vx
        game.map[1] -= number_of_steps * game.player.vy
        obj.collide_rect = pygame.Rect(-game.map[0] + obj.x, -game.map[1] + obj.y, obj.width, obj.height)
        if obj.collide_rect.colliderect(game.player.collide_rect):
            game.map[0] -= number_of_steps * game.player.vx
            game.player.vx = 0
            game.map[1] += number_of_steps * game.player.vy
            game.player.vy = 0
        else:
            game.map[0] -= number_of_steps * game.player.vx
            game.map[1] += number_of_steps * game.player.vy


def player_move(game):
    """
    Изменяет координату объекта относительно экрана и студента относительно карты
    Args:
    game - params из модуля main
    """
    game.player.up = game.player.vy
    game.player.right = game.player.vx
    game.map[0] += game.player.vx
    game.map[1] -= game.player.vy
    game.player.vx = 0
    game.player.vy = 0
