import pygame
import sys
import os

from database_api.database import DataBase
from game_field import game
from game_field import service
from game_field import edit_field

pygame.mixer.init()
pygame.init()

RED = (255, 0, 0)
CLASSIC = (194, 192, 192)
CLASSIC_Menu = (255, 255, 255)
BLACK = (0, 0, 0)
button_click = pygame.mixer.Sound('Sounds/9283.mp3')  # Путь к звуку клика

folder_path = "game_field/levels"  # Путь к уровням

users = 'Введите логин'
password = 'Введите пароль'
database = DataBase()

# Загружаем музыку
music_file = 'Sounds/за фрукты да.mp3'
pygame.mixer.music.load(music_file)

logging = True  # Переменная для смены логина и регистрации

count = 1  # Устанавливаем начальную громкость (от 0 до 1)
pygame.mixer.music.set_volume(count)

# Проигрываем музыку
pygame.mixer.music.play(-1)  # -1 указывает на повторное воспроизведение музыки

control: dict[str: int] = {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d,
    'bullet': pygame.K_SPACE
}


def title_text(scr, message, x, y, font_color=CLASSIC, font_size=150,
               font_type='../Styles/bitcell_memesbruh03.ttf'):  # Функция создания кнопки
    font_type = pygame.font.Font(font_type, font_size)  # Шрифт + Размер
    text = font_type.render(message, True, font_color)  # Текст + Цвет
    button_rect = text.get_rect(center=(x, y))  # Расположение
    scr.blit(text, button_rect.topleft)  # Отображение
    return button_rect  # Возвращаем координаты


def menu(username: str = str()):
    global count, users
    if username:
        users = username
    size = 1000, 820  # Размеры окна
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Меню')
    button_start = title_text(screen, 'Начать', 500, 150)  # Создаём рабочую площадь кнопки "Играть"
    button_music = title_text(screen, 'М', 100, 100, 0)  # Создаём рабочую площадь кнопки "Музыка"
    button_setting = title_text(screen, 'M', 100, 240, 0)  # Создаём рабочую площадь кнопки "Настройки"
    button_creator = title_text(screen, 'Творец', 500, 300)  # Создаём рабочую площадь кнопки "Творец"
    button_rait = title_text(screen, 'M', 100, 380, 0)  # Создаём рабочую площадь кнопки "Рейтинг"
    button_quit = title_text(screen, 'M', 850, 100, 10)  # Создаём рабочую площадь кнопки "Выйти"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:  # Срабатывание на ЛКМ
                if pygame.mouse.get_pressed()[0] == 1:
                    if button_start.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Играть"
                        pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                        choose_level()
                        pygame.quit()
                    elif button_music.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Музыка"
                        if count > 0:
                            count = 0
                        else:
                            count = 1
                        pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                        pygame.mixer.music.set_volume(count)  # Устанавливаем громкость
                    elif button_setting.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Настройки"
                        pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                        setting()
                        pygame.quit()
                    elif button_creator.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Творец"
                        pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                        edit_field.edit_window(users)
                        pygame.quit()
                    elif button_rait.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Рейтинг"
                        pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                        raits(username if username else users)
                        pygame.quit()
                    elif button_quit.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Выйти"
                        pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                        authorize()
                        pygame.quit()
                elif event.button == 4:  # Колесико мыши кручено вверх
                    if button_music.collidepoint(pygame.mouse.get_pos()):
                        count += 0.1
                        if count > 1:
                            count = 1
                        pygame.mixer.music.set_volume(count)
                elif event.button == 5:  # Колесико мыши кручено вниз

                    if button_music.collidepoint(pygame.mouse.get_pos()):
                        count -= 0.1
                        if count < 0:
                            count = 0
                    pygame.mixer.music.set_volume(count)

        mouse_pos = pygame.mouse.get_pos()  # Получаем координаты мыши

        # Играть
        button_starting = button_start.collidepoint(mouse_pos)  # Присваиваем

        # Выйти
        button_quits = button_quit.collidepoint(mouse_pos)  # Присваиваем

        # Громкость
        button_musics = button_music.collidepoint(mouse_pos)  # Присваиваем

        # Настройки
        button_settings = button_setting.collidepoint(mouse_pos)  # Присваиваем

        # Творец
        button_creators = button_creator.collidepoint(mouse_pos)  # Присваиваем

        # Рейтинг
        button_raits = button_rait.collidepoint(mouse_pos)  # Присваиваем

        background_image = pygame.image.load('pictures/2.jpg')  # Фоновая картинка(путь)
        screen.blit(background_image, (0, 0))  # Размещение картинки в окне

        if button_starting:  # Если курсор в поле кнопки "Играть"
            button_color_start = RED
            pygame.draw.polygon(screen, button_color_start, ((342, 188), (660, 188), (660, 195), (342, 195)))
        else:  # Если курсор не в поле кнопки "Играть"
            button_color_start = CLASSIC

        if button_creators:  # Если курсор в поле кнопки "Творец"
            button_color_create = RED
            pygame.draw.polygon(screen, button_color_create, ((335, 345), (678, 345), (678, 352), (335, 352)))
        else:  # Если курсор не в поле кнопки "Творец"
            button_color_create = CLASSIC

        if button_musics:  # Если курсор в поле кнопки "Музыка"
            button_color_music = RED
            text_music = str(int(count * 100))
            size_music = 60
        else:  # Если курсор не в поле кнопки "Музыка"
            button_color_music = CLASSIC
            text_music = 'Музыка'
            size_music = 30

        if button_settings:  # Если курсор в поле кнопки "Настройки"
            button_color_settings = RED
        else:  # Если курсор не в поле кнопки "Настройки"
            button_color_settings = CLASSIC

        if button_raits:  # Если курсор в поле кнопки "Рейтинг"
            button_color_raits = RED
        else:  # Если курсор не в поле кнопки "Рейтинг"
            button_color_raits = CLASSIC

        if button_quits:  # Если курсор в поле кнопки "Выйти"
            button_color_quit = RED
        else:  # Если курсор не в поле кнопки "Выйти"
            button_color_quit = CLASSIC

        title_text(screen, 'Tanchiki', 500, 750, (255, 255, 0), 190, 'Styles/Pentagra.ttf')

        title_text(screen, 'Начать', 505, 145,
                   button_color_start)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)

        title_text(screen, 'Творец', 505, 295,
                   button_color_create)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)

        # Музыка
        pygame.draw.polygon(screen, pygame.color.Color(42, 44, 92), ((50, 65), (157, 65), (157, 125), (50, 125)))
        pygame.draw.polygon(screen, pygame.color.Color('white'), ((50, 65), (157, 65), (157, 125), (50, 125)), 3)
        title_text(screen, text_music, 105, 95, button_color_music,
                   size_music)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)

        # Выйти
        pygame.draw.polygon(screen, pygame.color.Color(42, 44, 92), ((800, 65), (907, 65), (907, 125), (800, 125)))
        pygame.draw.polygon(screen, pygame.color.Color('white'), ((800, 65), (907, 65), (907, 125), (800, 125)), 3)
        title_text(screen, 'Выйти', 855, 95, button_color_quit,
                   30)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)

        pygame.draw.polygon(screen, pygame.color.Color(42, 44, 92), ((50, 180), (157, 180), (157, 240), (50, 240)))
        pygame.draw.polygon(screen, pygame.color.Color('white'), ((50, 180), (157, 180), (157, 240), (50, 240)), 3)
        title_text(screen, 'Настройки', 105, 210,
                   button_color_settings, 30)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)

        pygame.draw.polygon(screen, pygame.color.Color(42, 44, 92), ((50, 325), (157, 325), (157, 385), (50, 385)))
        pygame.draw.polygon(screen, pygame.color.Color('white'), ((50, 325), (157, 325), (157, 385), (50, 385)), 3)
        title_text(screen, 'Рейтинг', 105, 355,
                   button_color_raits, 30)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)

        pygame.display.flip()  # Отобразить всё на экране
        clock.tick(60)


def setting():
    global control
    size = 1000, 820  # Размеры окна
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Настройки')

    button_forward = title_text(screen, 'W', 140, 80, 100)  # Создаём рабочую площадь кнопки "Вперед"
    button_left = title_text(screen, 'L', 140, 230, 100)  # Создаём рабочую площадь кнопки "Влево"
    button_right = title_text(screen, 'R', 140, 380, 100)  # Создаём рабочую площадь кнопки "Вправо"
    button_back = title_text(screen, 'B', 140, 530, 100)  # Создаём рабочую площадь кнопки "Назад"
    button_fire = title_text(screen, 'F', 140, 680, 100)  # Создаём рабочую площадь кнопки "Огонь"
    button_return = title_text(screen, 'Вера', 850, 50, 10)  # Создаём рабочую площадь кнопки "Вернуться"

    controllers = list(map(pygame.key.name, control.values()))

    waiting_for_input = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:  # Срабатывание на ЛКМ
                if button_forward.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Вперед"
                    pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                    controllers[0] = '?'
                    waiting_for_input = True
                elif button_left.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Влево"
                    pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                    controllers[1] = '?'
                    waiting_for_input = True
                elif button_right.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Влево"
                    pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                    controllers[2] = '?'
                    waiting_for_input = True
                elif button_back.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Влево"
                    pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                    controllers[3] = '?'
                    waiting_for_input = True
                elif button_fire.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Огонь"
                    pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                    controllers[4] = '?'
                    waiting_for_input = True
                elif button_return.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Вернуться"
                    pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                    menu()
                    pygame.quit()

            elif event.type == pygame.KEYDOWN and waiting_for_input:
                pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                for key in range(len(controllers)):  # Ловим кнопку потерявшую управление
                    if controllers[key] == '?':
                        if key == 0:
                            control['up'] = event.key
                        elif key == 1:
                            control['down'] = event.key
                        elif key == 2:
                            control['left'] = event.key
                        elif key == 3:
                            control['right'] = event.key
                        elif key == 4:
                            control['bullet'] = event.key
                        controllers[key] = str(pygame.key.name(event.key))
                waiting_for_input = False

        mouse_pos = pygame.mouse.get_pos()  # Получаем координаты мыши

        # Вперед
        button_forwards = button_forward.collidepoint(mouse_pos)  # Присваиваем

        # Влево
        button_lefts = button_left.collidepoint(mouse_pos)  # Присваиваем

        # Вправо
        button_rights = button_right.collidepoint(mouse_pos)  # Присваиваем

        # Назад
        button_backs = button_back.collidepoint(mouse_pos)  # Присваиваем

        # Огонь
        button_fires = button_fire.collidepoint(mouse_pos)  # Присваиваем

        # Назад
        button_returns = button_return.collidepoint(mouse_pos)  # Присваиваем

        if button_forwards:  # Если курсор в поле кнопки "Вперед"
            button_color_forwards = RED
        else:  # Если курсор не в поле кнопки "Вперед"
            button_color_forwards = CLASSIC

        if button_lefts:  # Если курсор в поле кнопки "Влево"
            button_color_lefts = RED
        else:  # Если курсор не в поле кнопки "Влево"
            button_color_lefts = CLASSIC

        if button_rights:  # Если курсор в поле кнопки "Вправо"
            button_color_rights = RED
        else:  # Если курсор не в поле кнопки "Вправо"
            button_color_rights = CLASSIC

        if button_backs:  # Если курсор в поле кнопки "Назад"
            button_color_backs = RED
        else:  # Если курсор не в поле кнопки "Назад"
            button_color_backs = CLASSIC

        if button_fires:  # Если курсор в поле кнопки "Огонь"
            button_color_fires = RED
        else:  # Если курсор не в поле кнопки "Огонь"
            button_color_fires = CLASSIC

        if button_returns:  # Если курсор в поле кнопки "Вернуться"
            button_color_returns = RED
        else:  # Если курсор не в поле кнопки "Вернуться"
            button_color_returns = CLASSIC

        background_image = pygame.image.load('pictures/2.jpg')  # Фоновая картинка(путь)
        screen.blit(background_image, (0, 0))  # Размещение картинки в окне

        title_text(screen, controllers[0], 145, 85,
                   button_color_forwards, 100)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)
        title_text(screen, controllers[1], 145, 235,
                   button_color_lefts, 100)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)
        title_text(screen, controllers[2], 145, 385,
                   button_color_rights, 100)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)
        title_text(screen, controllers[3], 145, 535,
                   button_color_backs, 100)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)
        title_text(screen, controllers[4], 145, 685,
                   button_color_fires, 100)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)
        title_text(screen, 'Вернуться', 855, 55,
                   button_color_returns, 50)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)

        title_text(screen, '- Вперед', 365, 88,
                   CLASSIC_Menu, 100)  # Создание текста (X+120, Y-2 для текста по кнопке)
        title_text(screen, '- Назад', 365, 238,
                   CLASSIC_Menu, 100)  # Создание текста (X+120, Y-2 для текста по кнопке)
        title_text(screen, '- Влево', 365, 388,
                   CLASSIC_Menu, 100)  # Создание текста (X+120, Y-2 для текста по кнопке)
        title_text(screen, '- Вправо ', 365, 538,
                   CLASSIC_Menu, 100)  # Создание текста (X+120, Y-2 для текста по кнопке)
        title_text(screen, '- Огонь ', 365, 688,
                   CLASSIC_Menu, 100)  # Создание текста (X+120, Y-2 для текста по кнопке)

        pygame.display.flip()  # Отобразить всё на экране
        clock.tick(60)


def choose_level():
    size = 1000, 820  # Размеры окна
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Выбор уровня')

    file_list = list()

    # Проверяем наличие указанной папки
    if os.path.exists(folder_path):
        # Перебираем все файлы и папки в указанной папке
        for file_name in os.listdir(folder_path):
            # Проверяем, является ли объект файлом
            if os.path.isfile(os.path.join(folder_path, file_name)):
                # Проверяем расширение файла
                if file_name.endswith(".txt"):
                    file_list.append(file_name)
    file_list.sort()
    lvl = 0
    check_left = False
    check_right = False

    button_right = title_text(screen, 'L', 670, 295, 100)  # Создаём рабочую площадь кнопки "Вправо"
    button_left = title_text(screen, 'L', 330, 295, 100)  # Создаём рабочую площадь кнопки "Влево"
    button_choose = title_text(screen, 'Выбра', 500, 505, 0)  # Создаём рабочую площадь кнопки "Выбрать"
    button_return = title_text(screen, 'Вера', 850, 50, 10)  # Создаём рабочую площадь кнопки "Вернуться"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Срабатывание на ЛКМ
                if button_return.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Вернуться"
                    pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                    menu()
                    pygame.quit()
                elif button_right.collidepoint(
                        pygame.mouse.get_pos()) and check_right is False:  # Если клик был на кнопке "Вправо"
                    pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                    lvl += 1
                elif button_left.collidepoint(
                        pygame.mouse.get_pos()) and check_left is False:  # Если клик был на кнопке "Влево"
                    pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                    lvl -= 1
                elif button_choose.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Выбрать"
                    pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                    game.game(filename=str(file_list[lvl]), control=control, username=users, database=database)
                    pygame.quit()

        mouse_pos = pygame.mouse.get_pos()  # Получаем координаты мыши

        # Назад
        button_returns = button_return.collidepoint(mouse_pos)  # Присваиваем

        # Выбрать
        button_chooses = button_choose.collidepoint(mouse_pos)  # Присваиваем

        # Вправо
        button_rights = button_right.collidepoint(mouse_pos)  # Присваиваем

        # Влево
        button_lefts = button_left.collidepoint(mouse_pos)  # Присваиваем

        if button_returns:  # Если курсор в поле кнопки "Вернуться"
            button_color_returns = RED
        else:  # Если курсор не в поле кнопки "Вернуться"
            button_color_returns = CLASSIC

        if button_rights:  # Если курсор в поле кнопки "Вправо"
            button_color_rights = RED
        else:  # Если курсор не в поле кнопки "Влево"
            button_color_rights = CLASSIC

        if button_lefts:  # Если курсор в поле кнопки "Влево"
            button_color_lefts = RED
        else:  # Если курсор не в поле кнопки "Влево"
            button_color_lefts = CLASSIC

        if button_chooses:  # Если курсор в поле кнопки "Выбрать"
            button_color_chooses = RED
        else:  # Если курсор не в поле кнопки "Выбрать"
            button_color_chooses = CLASSIC_Menu

        background_image = pygame.image.load('pictures/2.jpg')  # Фоновая картинка(путь)
        screen.blit(background_image, (0, 0))  # Размещение картинки в окне

        pygame.draw.polygon(screen, pygame.color.Color(42, 44, 92), ((400, 210), (600, 210), (600, 410), (400, 410)))
        pygame.draw.polygon(screen, pygame.color.Color('white'), ((400, 210), (600, 210), (600, 410), (400, 410)), 3)

        title_text(screen, 'Вернуться', 855, 55,
                   button_color_returns, 50)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)
        if lvl != 0:
            title_text(screen, '<', 335, 300,
                       button_color_lefts, 100)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)
            check_left = False
        else:
            check_left = True

        if lvl != len(file_list) - 1:
            title_text(screen, '>', 675, 300,
                       button_color_rights, 100)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)
            check_right = False
        else:
            check_right = True

        pygame.draw.polygon(screen, pygame.color.Color(23, 163, 28), ((355, 460), (650, 460), (650, 550), (355, 550)))
        pygame.draw.polygon(screen, pygame.color.Color('dark gray'), ((355, 460), (650, 460), (650, 550), (355, 550)),
                            3)
        title_text(screen, 'Выбрать', 505, 500,
                   button_color_chooses, 100)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)

        title_text(screen, 'Выбрать уровень', 505, 180,
                   CLASSIC_Menu, 40)  # Создание текста кнопки (X+120, Y-2 для текста по кнопке)
        title_text(screen, file_list[lvl].replace('.txt', '').replace('level_', ''), 500, 300, CLASSIC)

        pygame.display.flip()  # Отобразить всё на экране
        clock.tick(60)


def authorize():
    global logging
    global count
    size = 1000, 820  # Размеры окна
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Авторизация')

    button_signin = title_text(screen, 'Вход', 500, 150)  # Создаём рабочую площадь кнопки "Войти"
    button_signup = title_text(screen, 'Регистрация', 500, 300)  # Создаём рабочую площадь кнопки "Регистрация"
    button_music = title_text(screen, 'М', 100, 100, 0)  # Создаём рабочую площадь кнопки "Музыка"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Срабатывание на ЛКМ
                if pygame.mouse.get_pressed()[0] == 1:
                    if button_signin.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Войти"
                        pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                        logging = True
                        login_register()
                        pygame.quit()
                    elif button_signup.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Регистрация"
                        pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                        logging = False
                        login_register()
                        pygame.quit()
                    elif button_music.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Музыка"
                        if count > 0:
                            count = 0
                        else:
                            count = 1
                        pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                        pygame.mixer.music.set_volume(count)  # Устанавливаем громкость
                elif event.button == 4:  # Колесико мыши кручено вверх
                    if button_music.collidepoint(pygame.mouse.get_pos()):
                        count += 0.1
                        if count > 1:
                            count = 1
                        pygame.mixer.music.set_volume(count)
                elif event.button == 5:  # Колесико мыши кручено вниз

                    if button_music.collidepoint(pygame.mouse.get_pos()):
                        count -= 0.1
                        if count < 0:
                            count = 0
                    pygame.mixer.music.set_volume(count)

        mouse_pos = pygame.mouse.get_pos()  # Получаем координаты мыши

        # Вход
        button_signins = button_signin.collidepoint(mouse_pos)  # Присваиваем

        # Регистрация
        button_signups = button_signup.collidepoint(mouse_pos)  # Присваиваем

        # Громкость
        button_musics = button_music.collidepoint(mouse_pos)  # Присваиваем

        if button_signins:  # Если курсор в поле кнопки "Войти"
            button_color_signin = RED
        else:  # Если курсор не в поле кнопки "Войти"
            button_color_signin = CLASSIC

        if button_signups:  # Если курсор в поле кнопки "Регистрация"
            button_color_signup = RED
        else:  # Если курсор не в поле кнопки "Регистрация"
            button_color_signup = CLASSIC

        if button_musics:  # Если курсор в поле кнопки "Музыка"
            button_color_music = RED
            text_music = str(int(count * 100))
            size_music = 60
        else:  # Если курсор не в поле кнопки "Музыка"
            button_color_music = CLASSIC
            text_music = 'Музыка'
            size_music = 30

        background_image = pygame.image.load('pictures/2.jpg')  # Фоновая картинка(путь)
        screen.blit(background_image, (0, 0))  # Размещение картинки в окне

        # Музыка
        pygame.draw.polygon(screen, pygame.color.Color(42, 44, 92), ((50, 65), (157, 65), (157, 125), (50, 125)))
        pygame.draw.polygon(screen, pygame.color.Color('white'), ((50, 65), (157, 65), (157, 125), (50, 125)), 3)
        title_text(screen, text_music, 105, 95, button_color_music, size_music)

        title_text(screen, 'Вход', 505, 145,
                   button_color_signin)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)

        title_text(screen, 'Регистрация', 505, 295,
                   button_color_signup)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)

        title_text(screen, 'Tanchiki', 500, 750, (255, 255, 0), 190, 'Styles/Pentagra.ttf')

        pygame.display.flip()  # Отобразить всё на экране
        clock.tick(60)


def login_register():
    global users
    global password
    size = 1000, 820  # Размеры окна
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    if logging:
        pygame.display.set_caption('Вход')
    else:
        pygame.display.set_caption('Регистрация')

    button_login = title_text(screen, '--------', 500, 250)  # Создаём рабочую площадь кнопки "Логин"
    button_password = title_text(screen, '--------', 500, 400)  # Создаём рабочую площадь кнопки "Пароль"
    button_confirm = title_text(screen, 'Подтве', 500, 550)  # Создаём рабочую площадь кнопки "Подтвердить"
    button_return = title_text(screen, 'Вера', 850, 50, 10)  # Создаём рабочую площадь кнопки "Вернуться"

    stop_list = ['tab', 'caps lock', 'left shift', 'left ctrl', 'left alt',
                 'escape', 'delete', 'end', 'page down', 'insert', 'home', 'page up',
                 'numlock', '[/]', '[*]', '[-]', '[+]', 'enter', 'left meta',
                 'right ctrl', 'right alt', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12']

    helper = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:  # Срабатывание на ЛКМ
                if button_login.collidepoint(pygame.mouse.get_pos()):  # Если клик был в поле "Логин"
                    pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                    users = ''
                    helper = True
                elif button_password.collidepoint(pygame.mouse.get_pos()):  # Если клик был в поле "Пароль"
                    pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                    password = ''
                    helper = False
                elif button_return.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Вернуться"
                    pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                    users = 'Введите логин'
                    password = 'Введите пароль'
                    authorize()
                    pygame.quit()
                elif button_confirm.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Подтвердить"
                    pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                    if users != '' and users != 'Введите логин' and password != '' and password != 'Введите пароль':
                        if database.check_username(str(users)) and logging:  # Проверяет есть ли users в бд
                            if database.check_password(str(users),
                                                       str(password)):  # Проверяет правильность ввода пароля
                                menu()
                                pygame.quit()
                        if database.check_username(str(users)) == False and logging == False:
                            database.create_account(str(users), str(password))  # Если нет аккаунта, то регистрация
                            menu()
                            pygame.quit()

            elif event.type == pygame.KEYDOWN:
                pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                if helper:
                    if str(pygame.key.name(event.key)) == 'backspace':
                        if len(users) > 0:
                            users = users[:-1]
                    elif str(pygame.key.name(event.key)) == 'space':
                        users += ' '
                    elif str(pygame.key.name(event.key)) not in stop_list:
                        users += pygame.key.name(event.key)
                else:
                    if str(pygame.key.name(event.key)) == 'backspace':
                        if len(password) > 0:
                            password = password[:-1]
                    elif str(pygame.key.name(event.key)) == 'space':
                        if len(password) < 20:
                            password += ' '

                    elif str(pygame.key.name(event.key)) not in stop_list:
                        if len(password) < 20:
                            password += pygame.key.name(event.key)

        mouse_pos = pygame.mouse.get_pos()  # Получаем координаты мыши

        # Подтердить
        button_confirms = button_confirm.collidepoint(mouse_pos)  # Присваиваем

        # Вернуться
        button_returns = button_return.collidepoint(mouse_pos)  # Присваиваем

        if button_confirms:  # Если курсор в поле кнопки "Подтвердить"
            button_color_confirm = RED
        else:  # Если курсор не в поле кнопки "Подтвердить"
            button_color_confirm = CLASSIC_Menu

        if button_returns:  # Если курсор в поле кнопки "Вернуться"
            button_color_return = RED
        else:  # Если курсор не в поле кнопки "Вернуться"
            button_color_return = CLASSIC

        background_image = pygame.image.load('pictures/2.jpg')  # Фоновая картинка(путь)
        screen.blit(background_image, (0, 0))  # Размещение картинки в окне

        title_text(screen, 'Вернуться', 855, 55,
                   button_color_return, 50)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)
        # Логин
        pygame.draw.polygon(screen, pygame.color.Color(42, 44, 92), ((320, 175), (680, 175), (680, 225), (320, 225)))
        pygame.draw.polygon(screen, pygame.color.Color('white'), ((320, 175), (680, 175), (680, 225), (320, 225)), 3)
        title_text(screen, users, 500, 200,
                   CLASSIC, 50)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)

        # Пароль
        pygame.draw.polygon(screen, pygame.color.Color(42, 44, 92), ((320, 325), (680, 325), (680, 375), (320, 375)))
        pygame.draw.polygon(screen, pygame.color.Color('white'), ((320, 325), (680, 325), (680, 375), (320, 375)), 3)
        title_text(screen, password, 500, 350,
                   CLASSIC, 50)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)

        # Подтвердить
        pygame.draw.polygon(screen, pygame.color.Color(23, 163, 28), ((320, 515), (680, 515), (680, 585), (320, 585)))
        pygame.draw.polygon(screen, pygame.color.Color('dark gray'), ((320, 515), (680, 515), (680, 585), (320, 585)),
                            3)
        title_text(screen, 'Подтвердить', 505, 545,
                   button_color_confirm, 80)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)

        pygame.display.flip()  # Отобразить всё на экране
        clock.tick(60)


def raits(users: str = str()):
    size = 1000, 820  # Размеры окна
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Рейтинг')

    button_return = title_text(screen, 'Вера', 850, 50, 10)
    # Создаём рабочую площадь кнопки "Вернуться"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:  # Срабатывание на ЛКМ
                if button_return.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Вернуться"
                    pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                    menu()
                    pygame.quit()

        mouse_pos = pygame.mouse.get_pos()  # Получаем координаты мыши

        # Вернуться
        button_returns = button_return.collidepoint(mouse_pos)  # Присваиваем

        if button_returns:  # Если курсор в поле кнопки "Вернуться"
            button_color_return = RED
        else:  # Если курсор не в поле кнопки "Вернуться"
            button_color_return = CLASSIC

        background_image = pygame.image.load('pictures/2.jpg')  # Фоновая картинка(путь)
        screen.blit(background_image, (0, 0))  # Размещение картинки в окне

        title_text(screen, 'Вернуться', 855, 55,
                   button_color_return, 50)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)

        title_text(screen, 'Ваш рейтинг:', 300, 105,
                   CLASSIC, 100)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)

        title_text(screen, str(service.percent_win(database.get_data(users)[0], database.get_data(users)[1])), 620, 105,
                   CLASSIC_Menu, 100)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)

        title_text(screen, 'Ваши поражения:', 250, 205,
                   CLASSIC, 50)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)

        title_text(screen, str(database.get_data(users)[0]), 530, 205,
                   CLASSIC_Menu, 100)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)

        title_text(screen, 'Уничтоженные танки:', 285, 305,
                   CLASSIC, 50)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)

        title_text(screen, str(database.get_data(users)[1]), 565, 305,
                   CLASSIC_Menu, 100)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)

        pygame.display.flip()  # Отобразить всё на экране
        clock.tick(60)


if __name__ == '__main__':  # Самый старт
    authorize()  # Вызыв авторизации
