import os
import re
import sys
import pygame


def load_image(name_file: str, *name_dir: str, color_key=None, size: int = 32, rotate: bool = False) -> pygame.Surface:
    fullname = os.path.join('../pictures', *name_dir, name_file)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    resized_image = pygame.transform.scale(image, (size, size))
    if rotate:
        resized_image = pygame.transform.rotate(resized_image, 180)
    return resized_image


def top_level(dir_name: str = 'levels') -> int:
    # Получаем список файлов в текущей директории
    file_names = os.listdir(dir_name)

    # Используем регулярное выражение для поиска чисел в названиях файлов
    numbers = [int(re.search(r'\d+', file_name).group()) for file_name in file_names]
    return max(numbers) if numbers else 0
