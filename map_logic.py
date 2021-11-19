motion_keys_numbers = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]

def collision():
    """
    расчитывает коллизию
    return:
    """
    pass


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
            player_move(event)
        elif event.key == pygame.K_e:
            #функция для класса PlayerInventory()
            pass
        elif event.key == pygame.K_ESCAPE:
            open_start_menu()
    elif event.type == pygame.MOUSEBUTTONDOWN:
        #взаимодействие с объектами
        pass


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
