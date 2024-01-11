import pygame
import game_field
import sys

pygame.mixer.init()
pygame.init()

RED = (255, 0, 0)
CLASSIC = (194, 192, 192)

button_click = pygame.mixer.Sound('Sounds/9283.mp3')


def title_text(scr, message, x, y, font_color=CLASSIC, font_size=150,
               font_type='Styles/bitcell_memesbruh03.ttf'):  # Функция создания кнопки
    font_type = pygame.font.Font(font_type, font_size)  # Шрифт + Размер
    text = font_type.render(message, True, font_color)  # Текст + Цвет
    button_rect = text.get_rect(center=(x, y))  # Расположение
    scr.blit(text, button_rect.topleft)  # Отображение
    return button_rect  # Возвращаем координаты


def menu():
    size = 1000, 820  # Размеры окна
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    # Загружаем музыку
    music_file = 'Sounds/за фрукты да.mp3'
    pygame.mixer.music.load(music_file)

    # Проигрываем музыку
    pygame.mixer.music.play(-1)  # -1 указывает на повторное воспроизведение музыки

    count = 1  # Устанавливаем начальную громкость (от 0 до 1)
    pygame.mixer.music.set_volume(count)

    button_start = title_text(screen, 'Начать', 500, 150)  # Создаём рабочую площадь кнопки "Играть"
    button_music = title_text(screen, 'М', 100, 100, 1)  # Создаём рабочую площадь кнопки "Музыка"
    button_setting = title_text(screen, 'M', 100, 240, 1)  # Создаём рабочую площадь кнопки "Настройки"
    button_creator = title_text(screen, 'Творец', 500, 300)  # Создаём рабочую площадь кнопки "Творец"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:  # Срабатывание на ЛКМ
                if pygame.mouse.get_pressed()[0] == 1:
                    if button_start.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Играть"
                        print("Кнопка 'Играть' нажата")
                        game_field.game.main('level_4.txtd')
                        pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                    elif button_music.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Музыка"
                        print("Кнопка 'Музыка' нажата")
                        if count > 0:
                            count = 0
                        else:
                            count = 1
                        pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                        pygame.mixer.music.set_volume(count)  # Устанавливаем громкость
                    elif button_setting.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Настройки"
                        print("Кнопка 'Настройки' нажата")
                        pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
                    elif button_creator.collidepoint(pygame.mouse.get_pos()):  # Если клик был на кнопке "Творец"
                        print("Кнопка 'Творец' нажата")
                        game_field.edit_field.main()
                        pygame.mixer.Sound.play(button_click)  # Звук при нажатии на кнопку
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

        # Громкость
        button_musics = button_music.collidepoint(mouse_pos)  # Присваиваем

        # Настройки
        button_settings = button_setting.collidepoint(mouse_pos)  # Присваиваем

        # Творец
        button_creators = button_creator.collidepoint(mouse_pos)  # Присваиваем

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
        else:  # Если курсор не в поле кнопки "Играть"
            button_color_music = CLASSIC
            text_music = 'Музыка'
            size_music = 30

        if button_settings:  # Если курсор в поле кнопки "Настройки"
            button_color_settings = RED
        else:  # Если курсор не в поле кнопки "Настройки"
            button_color_settings = CLASSIC

        title_text(screen, 'Tanchiki', 500, 750, (255, 255, 0), 190, 'Styles/Pentagra.ttf')

        title_text(screen, 'Начать', 505, 145,
                   button_color_start)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)

        title_text(screen, 'Творец', 505, 295,
                   button_color_create)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)

        pygame.draw.polygon(screen, pygame.color.Color(42, 44, 92), ((50, 65), (157, 65), (157, 125), (50, 125)))
        pygame.draw.polygon(screen, pygame.color.Color('white'), ((50, 65), (157, 65), (157, 125), (50, 125)), 3)
        title_text(screen, text_music, 105, 95, button_color_music, size_music)

        pygame.draw.polygon(screen, pygame.color.Color(42, 44, 92), ((50, 180), (157, 180), (157, 240), (50, 240)))
        pygame.draw.polygon(screen, pygame.color.Color('white'), ((50, 180), (157, 180), (157, 240), (50, 240)), 3)
        title_text(screen, 'Настройки', 105, 210,
                   button_color_settings, 30)  # Создание текста кнопки (X+5, Y-5 для текста по кнопке)

        pygame.display.flip()  # Отобразить всё на экране
        clock.tick(60)


if __name__ == '__main__':  # Самый старт
    menu()  # Вызыв меню
