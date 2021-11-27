import pygame

motion_keys_numbers = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]


def collision(game):
    """
    расчитывает коллизию
    """
    for obj in game.all_objects:
        if obj.collide_rect.colliderect(game.player.collide_rect):
            game.map[0] -= 1.5*game.player.vx
            if obj.collide_rect.colliderect(game.player.collide_rect):
                game.map[0] += 1.5*game.player.vx_for_collision
                game.map[1] += 1.5*game.player.vy_for_collision
                if obj.collide_rect.colliderect(game.player.collide_rect):
                    game.map[0] -= 1.5*game.player.vx_for_collision
                    if obj.collide_rect.colliderect(game.player.collide_rect):
                        game.map[0] -= 3*game.player.vx_direction_for_collision
                        if obj.collide_rect.colliderect(game.player.collide_rect):
                            game.map[0] += 3 * game.player.vx_direction_for_collision
                            game.map[1] += 3 * game.player.vy_direction_for_collision
                            if obj.collide_rect.colliderect(game.player.collide_rect):
                                game.map[0] -= 3 * game.player.vx_direction_for_collision
                    else:
                        game.player.vx_for_collision = 0
                        game.player.vx = 0
                        game.player.vy_for_collision = 0
                        game.player.vy = 0
                else:
                    game.player.vy_for_collision = 0
                    game.player.vy = 0
            else:
                game.player.vx_for_collision = 0
                game.player.vx = 0


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
        if pygame.key.get_pressed()[pygame.K_s]:
            game.player.vy = -2
        if pygame.key.get_pressed()[pygame.K_d]:
            game.player.vx = 2
        if pygame.key.get_pressed()[pygame.K_a]:
            game.player.vx = -2
        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            game.player.vx *= 2
            game.player.vy *= 2
        elif checked_event.type == pygame.MOUSEBUTTONUP or checked_event.type == pygame.MOUSEMOTION:
            game.player.inventory.visual_update(checked_event)
        if game.player.vx != 0 or game.player.vy != 0:
            player_move(game)
        collision(game)


def player_move(game):
    """
    Изменяет координату объекта относительно экрана и студента относительно карты
    Args:
    game - params из модуля main
    """
    collision(game)
    game.map[0] += game.player.vx
    game.map[1] -= game.player.vy
    game.player.vx = 0
    game.player.vy = 0
    collision(game)

