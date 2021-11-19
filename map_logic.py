import pygame
motion_keys_numbers = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]

def collision():
    """
    расчитывает коллизию
    return:
    collision_of_player_and_objects - массив данных, о том столкнулся ли игрок с объектом
    """
    collision_of_player_and_objects = []
    for obj in all_objects():
        if player.colliderect(obj.rect):
            collision_of_player_and_objects.append(1)
        else:
            collision_of_player_and_objects.append(0)
    return collision_of_player_and_objects


def player_toggle_inventory():
    pass


def player_toggle_object_inventory():
    pass


def event_checker(event):
    """
    Обработка нажатий мышью и на клавиатуру
    Args:
    event - событие на проверку
    """
    if event.type == pygame.KEYDOWN:
        if event.key in motion_keys_numbers:
            player_move(event, all_objects)
        elif event.key == pygame.K_e:
            # функция для класса PlayerInventory()
            pass
        elif event.key == pygame.K_ESCAPE:
            open_start_menu()
    elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION:
        for obj in slots:
            obj.slot_pressed(event)


def player_move(motion_key_click_event):
    """
    Изменяет координату объекта относительно экрана и студента относительно карты
    Args:
    motion_key_click_event - нажатие события на активную клавишу
    обработка нажатий мыши и клавиатуры"""
    if motion_key_click_event.key == pygame.K_w:
        for obj in all_objects:
            obj.y += player_speed
    elif motion_key_click_event.key == pygame.K_s:
        for obj in all_objects:
            obj.y -= player_speed
    elif motion_key_click_event.key == pygame.K_d:
        for obj in all_objects:
            obj.x -= player_speed
    elif motion_key_click_event.key == pygame.K_a:
        for obj in all_objects:
            obj.x += player_speed
