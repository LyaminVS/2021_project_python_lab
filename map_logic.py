import pygame

motion_keys_numbers = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]


def collision(params_class):
    """
    расчитывает коллизию
    """
    for obj in params_class.all_objects():
        if params_class.player.colliderect(obj.rect):
            if ((params_class.player.y + params_class.player.height) > obj.y) and (params_class.player.y < obj.y):
                params_class.player.y = obj.y - params_class.player.height
            if ((params_class.player.y + params_class.player.height) > (obj.y + obj.height)) and (params_class.player.y > obj.y):
                params_class.player.y = obj.y - params_class.player.height
            if ((params_class.player.y + params_class.player.height) > obj.y) and (params_class.player.y < obj.y):
                params_class.player.y = obj.y - params_class.player.height
            if ((params_class.player.y + params_class.player.height) > (obj.y + obj.height)) and (params_class.player.y > obj.y):
                params_class.player.y = obj.y - params_class.player.height


def event_checker(event_array, class_params):
    """
    Обработка нажатий мышью и на клавиатуру
    Args:
    event_array - массив событий для обработки
    params_class - params из модуля main
    """
    for checked_event in event_array:
        if checked_event.type == pygame.QUIT:
            pygame.quit()
        if checked_event.type == pygame.KEYUP:
            class_params.player.move = 0
        if (checked_event.type == pygame.KEYDOWN) and (checked_event.key in motion_keys_numbers):
            class_params.player.move = 1
            class_params.player.move_direction = checked_event.key
        if class_params.player.move == 1:
            player_move(class_params)
        elif checked_event.type == pygame.MOUSEBUTTONUP or checked_event.type == pygame.MOUSEMOTION:
            pass


def player_move(params_class):
    """
    Изменяет координату объекта относительно экрана и студента относительно карты
    Args:
    params_class - params из модуля main
    """
    if params_class.player.move_direction == pygame.K_w:
        for obj in params_class.all_objects:
            obj.y -= params_class.player.vy
    elif params_class.player.move_direction == pygame.K_s:
        for obj in params_class.all_objects:
            obj.y += params_class.player.vy
    elif params_class.player.move_direction == pygame.K_d:
        for obj in params_class.all_objects:
            obj.x += params_class.player.vx
    elif params_class.player.move_direction == pygame.K_a:
        for obj in params_class.all_objects:
            obj.x -= params_class.player.vx
            
