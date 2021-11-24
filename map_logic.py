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

    """
    for checked_event in event_array:
        if checked_event.type == pygame.KEYDOWN:
            if checked_event.key in motion_keys_numbers:
                player_move(checked_event, class_params)
            elif checked_event.key == pygame.K_e:
                # функция для класса PlayerInventory()
                pass
        elif checked_event.type == pygame.MOUSEBUTTONUP or checked_event.type == pygame.MOUSEMOTION:
            pass


def player_move(motion_key_click_event, params_class):
    """
    Изменяет координату объекта относительно экрана и студента относительно карты
    Args:
    motion_key_click_event - обработка нажатий мыши и клавиатуры
    """
    if motion_key_click_event.key == pygame.K_w:
        for obj in params_class.all_objects:
            obj.y += params_class.player.vy
    elif motion_key_click_event.key == pygame.K_s:
        for obj in params_class.all_objects:
            obj.y -= params_class.player.vy
    elif motion_key_click_event.key == pygame.K_d:
        for obj in params_class.all_objects:
            obj.x -= params_class.player.vx
    elif motion_key_click_event.key == pygame.K_a:
        for obj in params_class.all_objects:
            obj.x += params_class.vx
