import pygame
motion_keys_numbers = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]

def collision(all_objects, player_class):
    """
    расчитывает коллизию
    """
    for obj in all_objects():
        if player_class.colliderect(obj.rect):
            if ((player_class.y+player_class.height) > obj.y) and (player_class.y < obj.y):
                player.y = obj.y-player.height
            if ((player_class.y + player_class.height) > (obj.y+obj.height)) and (player_class.y > obj.y):
                player.y = obj.y - player.height
            if ((player_class.y+player_class.height) > obj.y) and (player_class.y < obj.y):
                player.y = obj.y-player.height
            if ((player_class.y + player_class.height) > (obj.y+obj.height)) and (player_class.y > obj.y):
                player.y = obj.y - player.height


def event_checker(event_array, class_params, class_player, def_finish):
    """
    Обработка нажатий мышью и на клавиатуру
    Args:
    
    """
    for checked_event in event_array:
        if checked_event.type == pygame.KEYDOWN:
            if checked_event.key in motion_keys_numbers:
                player_move(event, all_objects)
            elif checked_event.key == pygame.K_e:
                # функция для класса PlayerInventory()
                pass
            elif checked_event.key == pygame.K_ESCAPE:
                open_start_menu()
        elif checked_event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION:
            for obj in slots:
                obj.slot_pressed(event)


def player_move(motion_key_click_event):
    """
    Изменяет координату объекта относительно экрана и студента относительно карты
    Args:
    motion_key_click_event - обработка нажатий мыши и клавиатуры
    """
    if motion_key_click_event.key == pygame.K_w:
        player.y -= player_speed*dt
        for obj in all_objects:
            obj.y += player_speed*dt
    elif motion_key_click_event.key==pygame.K_s:
        player.y += player_speed*dt
        for obj in all_objects:
            obj.y -= player_speed*dt
    elif motion_key_click_event.key==pygame.K_d:
        player.x += player_speed*dt
        for obj in all_objects:
            obj.x -= player_speed*dt
    elif motion_key_click_event.key==pygame.K_a:
        player.x -= player_speed*dt
        for obj in all_objects:
            obj.x += player_speed*dt
