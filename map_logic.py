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
        if (checked_event.type == pygame.KEYDOWN) and (checked_event.key == pygame.K_e):
            class_params.inventory_opened = not class_params.inventory_opened
        if checked_event.type == pygame.QUIT:
            class_params.finished = True
        if checked_event.type == pygame.KEYUP:
            class_params.player.move = 0
        if pygame.key.get_pressed()[pygame.K_w]:
            class_params.player.vy = 2
        if pygame.key.get_pressed()[pygame.K_s]:
            class_params.player.vy = -2
        if pygame.key.get_pressed()[pygame.K_d]:
            class_params.player.vx = 2
        if pygame.key.get_pressed()[pygame.K_a]:
            class_params.player.vx = -2
        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            class_params.player.vx *= 2
            class_params.player.vy *= 2
        elif checked_event.type == pygame.MOUSEBUTTONUP or checked_event.type == pygame.MOUSEMOTION:
            class_params.player.inventory.visual_update(checked_event)
        if class_params.player.vx != 0 or class_params.player.vy != 0:
            player_move(class_params)


def player_move(params_class):
    """
    Изменяет координату объекта относительно экрана и студента относительно карты
    Args:
    params_class - params из модуля main
    """
    if params_class.player.vx != 0:
        params_class.map[0] += params_class.player.vx
        params_class.player.right = (params_class.player.right + 1) % 2
    if params_class.player.vy != 0:
        params_class.map[1] -= params_class.player.vy
        params_class.player.right = (params_class.player.right + 1) % 2
    params_class.player.vx = 0
    params_class.player.vy = 0
            
