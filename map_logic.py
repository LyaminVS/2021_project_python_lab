import pygame

motion_keys_numbers = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]


def collision(all_objects, player_class):
    """
    расчитывает коллизию
    """
    for obj in all_objects():
        if player_class.colliderect(obj.rect):
            if ((player_class.y + player_class.height) > obj.y) and (player_class.y < obj.y):
                player_class.y = obj.y - player_class.height
            if ((player_class.y + player_class.height) > (obj.y + obj.height)) and (player_class.y > obj.y):
                player_class.y = obj.y - player_class.height
            if ((player_class.y + player_class.height) > obj.y) and (player_class.y < obj.y):
                player_class.y = obj.y - player_class.height
            if ((player_class.y + player_class.height) > (obj.y + obj.height)) and (player_class.y > obj.y):
                player_class.y = obj.y - player_class.height


def event_checker(event_array, class_params):
    """
    Обработка нажатий мышью и на клавиатуру
    Args:
    
    """
    for checked_event in event_array:
        if checked_event.type == pygame.KEYDOWN:
            if checked_event.key in motion_keys_numbers:
                player_move(checked_event, class_params.all_objects)
            elif checked_event.key == pygame.K_e:
                # функция для класса PlayerInventory()
                pass
        elif checked_event.type == pygame.MOUSEBUTTONUP or checked_event.type == pygame.MOUSEMOTION:
            for obj in class_params.slots:
                obj.slot_pressed(checked_event)


def player_move(motion_key_click_event, player_class, params_array):
    """
    Изменяет координату объекта относительно экрана и студента относительно карты
    Args:
    motion_key_click_event - обработка нажатий мыши и клавиатуры
    """
    if motion_key_click_event.key == pygame.K_w:
        player_class.y -= player_class.speed 
        for obj in params_array.all_objects:
            obj.y += player_class.speed
    elif motion_key_click_event.key == pygame.K_s:
        player_class.y += player_class.speed
        for obj in params_array.all_objects:
            obj.y -= player_class.speed
    elif motion_key_click_event.key == pygame.K_d:
        player_class.x += player_class.speed
        for obj in params_array.all_objects:
            obj.x -= player_class.speed
    elif motion_key_click_event.key == pygame.K_a:
        player_class.x -= player_class.speed
        for obj in params_array.all_objects:
            obj.x += player_class.speed
