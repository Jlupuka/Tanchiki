from typing import Any
import pygame
import datetime

import main
from database_api.database import DataBase
from game_field import service
from game_field.game_board import Images

width, height = 640, 640
left, top = 15, 20
cell_size = 32
count_destroyed_enemy = 0
count_destroyed_user = 0
degrees_enemy = (180, 0, 270, 90)
rotate_mapping_enemy = {key: degree for degree, key in zip(degrees_enemy,
                                                           {'up': pygame.K_w,
                                                            'down': pygame.K_s,
                                                            'left': pygame.K_d,
                                                            'right': pygame.K_a,
                                                            'bullet': pygame.K_SPACE})}


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface | list[pygame.Surface], x_pos: int, y_pos: int, *groups) -> None:
        super().__init__(*groups)
        self.image = image if isinstance(image, pygame.Surface) else image[0]
        self.orig_image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect().move(
            self.x_pos * cell_size + left,
            self.y_pos * cell_size + top
        )
        self.mask = pygame.mask.from_surface(self.image)


class UserTank(BaseSprite):
    def __init__(self, image: list[pygame.Surface], x_pos: int, y_pos: int, *sprites) -> None:
        super().__init__(image, x_pos, y_pos, *sprites[-2:])
        self.index_image = 0
        self.angle = 0
        self.image = self.orig_image[self.index_image]
        self.rank_move = 1
        sprite_names = ['box_sprite', 'stone_sprite', 'enemy_sprite', 'user_sprite', 'all_sprite']
        for sprite, name in zip(sprites[:-2], sprite_names):
            setattr(self, name, sprite)

    def move(self, type_move: str) -> None:
        new_x, new_y = self.rect.x, self.rect.y  # Сначала предполагаем, что новые координаты будут совпадать с текущими
        match type_move:
            case 'up':
                new_y -= self.rank_move
            case 'down':
                new_y += self.rank_move
            case 'left':
                new_x -= self.rank_move
            case 'right':
                new_x += self.rank_move
        # Проверяем, не сталкивается ли танк с какими-либо объектами
        if not self.check_collision(new_x, new_y) and 0 + left <= new_x <= (
                width - cell_size - left) and 0 + top <= new_y <= (
                height - cell_size - top // 2):
            self.rect.topleft = (new_x, new_y)
            self.index_image = (self.index_image + 1) % len(self.orig_image)
            self.flip(self.angle)

    def check_collision(self, x: int, y: int) -> bool:
        new_rect = self.rect.copy()
        new_rect.topleft = (x, y)
        for sprite in getattr(self, 'box_sprite').sprites(

        ) + getattr(self, 'stone_sprite').sprites() + getattr(self, 'enemy_sprite').sprites():
            if new_rect.colliderect(sprite.rect):
                return True  # Столкновение с объектом
        return False  # Нет столкновения

    def flip(self, angle: int = None) -> None:
        self.image = pygame.transform.rotate(self.orig_image[self.index_image], angle)
        self.angle = angle


class EnemyTank(BaseSprite):
    def __init__(self, image: list[pygame.Surface], x_pos: int, y_pos: int, *sprites) -> None:
        super().__init__(image, x_pos, y_pos, *sprites[-2:])
        self.index_image = 0
        self.angle = 0
        self.image = self.orig_image[self.index_image]
        self.rank_move = 1
        self.target = None
        self.time_bullet = datetime.datetime.now()
        self.images = Images(cell_size=cell_size)
        sprite_names = ['patron_sprite', 'box_sprite', 'stone_sprite', 'user_sprite', 'enemy_sprite', 'all_sprite']
        for sprite, name in zip(sprites, sprite_names):
            setattr(self, name, sprite)

    def find_nearest_user(self) -> UserTank:
        nearest_user = None
        nearest_distance = float('inf')
        for user in getattr(self, 'user_sprite').sprites():
            distance = ((user.x_pos - self.x_pos) ** 2 + (user.y_pos - self.y_pos) ** 2) ** 0.5
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_user = user
        return nearest_user

    def move(self) -> None:
        self.target = self.find_nearest_user()
        type_move = None
        flag_bullet = False
        if self.target is not None:
            dx, dy = self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance > cell_size:  # Only move if the target is at least one cell away
                if dx > 0:
                    type_move = 'right'
                elif dx < 0:
                    type_move = 'left'
                if type_move:
                    self.flip(rotate_mapping_enemy[type_move])
                if dx == 0 and datetime.datetime.now() - self.time_bullet >= datetime.timedelta(milliseconds=550):
                    Patron(self.images.patron,
                           self.rect.x,
                           self.rect.y,
                           self.angle + 180,
                           getattr(self, 'box_sprite'),
                           getattr(self, 'stone_sprite'),
                           getattr(self, 'user_sprite'),
                           getattr(self, 'enemy_sprite'),
                           getattr(self, 'patron_sprite'),
                           getattr(self, 'all_sprite'),
                           user=False)
                    flag_bullet = True
                self.move_tank(type_move)
                if dy > 0:
                    type_move = 'down'
                elif dy < 0:
                    type_move = 'up'
                if type_move:
                    self.flip(rotate_mapping_enemy[type_move])
                if dy == 0 and datetime.datetime.now() - self.time_bullet >= datetime.timedelta(milliseconds=500):
                    Patron(self.images.patron,
                           self.rect.x,
                           self.rect.y,
                           self.angle + 180,
                           getattr(self, 'box_sprite'),
                           getattr(self, 'stone_sprite'),
                           getattr(self, 'user_sprite'),
                           getattr(self, 'enemy_sprite'),
                           getattr(self, 'patron_sprite'),
                           getattr(self, 'all_sprite'),
                           user=False)
                    flag_bullet = True
                if flag_bullet:
                    self.time_bullet = datetime.datetime.now()
                self.move_tank(type_move)

    def move_tank(self, type_move: str) -> None:
        new_x, new_y = self.rect.x, self.rect.y  # Сначала предполагаем, что новые координаты будут совпадать с текущими
        if type_move is not None:
            match type_move:
                case 'up':
                    new_y -= self.rank_move
                case 'down':
                    new_y += self.rank_move
                case 'left':
                    new_x -= self.rank_move
                case 'right':
                    new_x += self.rank_move
        # Проверяем, не сталкивается ли танк с какими-либо объектами
        if not self.check_collision(new_x, new_y) and 0 + left <= new_x <= (
                width - cell_size - left) and 0 + top <= new_y <= (
                height - cell_size - top // 2):
            self.rect.topleft = (new_x, new_y)
            self.index_image = (self.index_image + 1) % len(self.orig_image)
            self.flip(self.angle)

    def check_collision(self, x: int, y: int) -> bool:
        new_rect = self.rect.copy()
        new_rect.topleft = (x, y)
        for sprite in getattr(self, 'box_sprite').sprites(

        ) + getattr(self, 'stone_sprite').sprites(

        ) + getattr(self, 'user_sprite').sprites() + getattr(self, 'enemy_sprite').sprites():
            if self != sprite:
                if new_rect.colliderect(sprite.rect):
                    return True  # Столкновение с объектом
        return False  # Нет столкновения

    def flip(self, angle: int = None) -> None:
        self.image = pygame.transform.rotate(self.orig_image[self.index_image], angle)
        self.angle = angle


class Box(BaseSprite):
    def __init__(self, image: pygame.Surface, x_pos: int, y_pos: int, *sprites) -> None:
        super().__init__(image, x_pos, y_pos, *sprites)


class Patron(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x_pos: int, y_pos: int, angle: int, *sprites, user: bool = True) -> None:
        super().__init__(*sprites[-2:])
        self.user = user
        self.image = image
        self.rect = self.image.get_rect().move(
            x_pos, y_pos
        )
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = angle
        self.wx = False
        self.wy = False
        sprite_names = ['box_sprite', 'stone_sprite', 'user_sprite', 'enemy_sprite', 'patron_sprite', 'all_sprite']
        for sprite, name in zip(sprites[:-2], sprite_names):
            setattr(self, name, sprite)
        self.angle_move()

    def angle_move(self) -> None:
        if self.angle == 0:
            self.rect.x += 12
            self.rect.y -= 10
            self.wy = -4
        elif self.angle == 90:
            self.rect.x -= 10
            self.rect.y += 12
            self.wx = -4
        elif self.angle == 180:
            self.rect.x += 12
            self.rect.y += 34
            self.wy = 4
        elif self.angle == 270:
            self.rect.x += 34
            self.rect.y += 12
            self.wx = 4
        self.image = pygame.transform.rotate(self.image, self.angle)

    def move(self) -> None:
        new_x, new_y = self.rect.x, self.rect.y

        if self.wx:
            new_x += self.wx
        elif self.wy:
            new_y += self.wy

        # Проверяем, не сталкивается ли танк с какими-либо объектами
        if not self.check_collision(new_x, new_y) and 0 + left <= new_x <= (
                width - cell_size + left - 6) and 0 + top <= new_y <= (
                height - cell_size + top - 6):
            self.rect.topleft = (new_x, new_y)
        if (self.rect.bottomleft[1] >= height - cell_size + top - 1 or
                self.rect.bottomleft[0] <= 0 + left + 4 or
                self.rect.bottomleft[0] >= width - cell_size + 6 or
                self.rect.bottomleft[1] <= 0 + top + 12):
            self.kill()

    def check_collision(self, x: int, y: int) -> bool:
        global count_destroyed_enemy, count_destroyed_user
        new_rect = self.rect.copy()
        new_rect.topleft = (x, y)
        for sprite in getattr(self, 'stone_sprite').sprites():
            if new_rect.colliderect(sprite.rect):
                self.kill()
                return True  # Столкновение с камнем
        for sprite in getattr(self, 'box_sprite').sprites():
            if new_rect.colliderect(sprite.rect):
                self.kill()
                sprite.kill()
                return True  # Столкновение с коробкой
        for sprite in getattr(self, 'enemy_sprite').sprites():
            if new_rect.colliderect(sprite.rect):
                if self.user:
                    count_destroyed_enemy += 1
                self.kill()
                if self.user:
                    sprite.kill()
                return True  # Столкновение с вражеским танком
        for sprite in getattr(self, 'user_sprite').sprites():
            if new_rect.colliderect(sprite.rect):
                if not self.user:
                    count_destroyed_user += 1
                self.kill()
                if not self.user:
                    sprite.kill()
                return True  # Столкновение с вражеским танком
        return False  # Нет столкновения


class Stone(BaseSprite):
    def __init__(self, image: pygame.Surface, x_pos: int, y_pos: int, *sprites) -> None:
        super().__init__(image, x_pos, y_pos, *sprites)


class Dirt(BaseSprite):
    def __init__(self, image: pygame.Surface, x_pos: int, y_pos: int, *sprites) -> None:
        super().__init__(image, x_pos, y_pos, *sprites)


class LifeUser(BaseSprite):
    def __init__(self, image: pygame.Surface, x_pos: int, y_pos: int, *sprites) -> None:
        super().__init__(image, x_pos, y_pos, *sprites)

    def image_update(self) -> None:
        self.image = self.orig_image[1]


class PauseMenu(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, *sprites) -> None:
        super().__init__(*sprites)
        print('da')
        self.image = image
        self.rect = self.image.get_rect(center=(width // 2, height // 2))

    def click(self, mouse_position: tuple[int, int]) -> str:
        if self.rect.collidepoint(mouse_position):  # Проверяем, был ли клик мыши в зоне спрайта
            relative_x = mouse_position[0] - self.rect.left  # Относительная координата X в пределах спрайта
            relative_y = mouse_position[1] - self.rect.top  # Относительная координата Y в пределах спрайта
            if 37 <= relative_x <= 200 and 182 <= relative_y <= 222:
                return 'back_menu'
            elif 356 <= relative_x <= 476 and 182 <= relative_y <= 222:
                return 'back_game'


def sort_level(board_level: list[list[int]], images: Images, all_sprite,
               box_sprite,
               user_sprite,
               dirt_sprite,
               stone_sprite,
               enemy_sprite,
               patron_sprite) -> list[Any]:
    tanks = {
        'user': list(),
        'enemy': list()
    }
    for row, row_data in enumerate(board_level):
        for col, col_data in enumerate(row_data):
            Dirt(images.default, col, row, all_sprite, dirt_sprite)
            match col_data:
                case pygame.K_0:
                    tanks['user'].append((col, row))
                case pygame.K_1:
                    Stone(images.stone, col, row, all_sprite, stone_sprite)
                case pygame.K_2:
                    Box(images.box, col, row, all_sprite, box_sprite)
                case pygame.K_3:
                    Dirt(images.default, col, row, all_sprite, dirt_sprite)
                    tanks['enemy'].append((col, row))
    for key in tanks.keys():
        for value in tanks[key]:
            if key == 'enemy':
                EnemyTank(images.enemy, value[0], value[1],
                          patron_sprite,
                          box_sprite,
                          stone_sprite,
                          user_sprite,
                          enemy_sprite,
                          all_sprite)
    return tanks['user'][0]


def game(filename: str, control: dict[str: int], username: str, database: DataBase) -> None:
    """
    Запускает игровое окно
    :param filename: Название уровня, который находится в папке game_field/levels (str)
    :param control: Словарь с клавишами управления (dict[str: int])
    :param username: Логин пользователя (str)
    :param database: Сессия базы данных (database_api.database.DataBase)
    :return: None
    """
    global count_destroyed_enemy, count_destroyed_user
    all_sprite = pygame.sprite.Group()
    box_sprite = pygame.sprite.Group()
    user_sprite = pygame.sprite.Group()
    dirt_sprite = pygame.sprite.Group()
    stone_sprite = pygame.sprite.Group()
    enemy_sprite = pygame.sprite.Group()
    patron_sprite = pygame.sprite.Group()
    life_sprite = pygame.sprite.Group()
    pause_sprite = pygame.sprite.Group()
    size = 800, 640
    degrees_user = (0, 180, 90, 270)
    rotate_mapping_user = {key: degree for degree, key in zip(degrees_user, control.keys())}
    database = database
    screen = pygame.display.set_mode(size)
    images = Images(cell_size=cell_size)
    LifeUser(images.life, 19, 1, all_sprite, life_sprite)
    LifeUser(images.life, 21, 1, all_sprite, life_sprite)
    LifeUser(images.life, 23, 1, all_sprite, life_sprite)
    patron_sprite.__str__()
    load_bord = service.load_level(filename=filename)
    flag_pause = False
    player_start_pos = sort_level(load_bord, images,
                                  all_sprite=all_sprite,
                                  box_sprite=box_sprite,
                                  user_sprite=user_sprite,
                                  dirt_sprite=dirt_sprite,
                                  stone_sprite=stone_sprite,
                                  enemy_sprite=enemy_sprite,
                                  patron_sprite=patron_sprite)
    player_life = 3
    count_destroyed_enemy = 0
    count_destroyed_user = 0
    clock = pygame.time.Clock()
    fps = 75
    angle = target_angle = 0
    running = True
    player = UserTank(images.user_tank,
                      player_start_pos[0],
                      player_start_pos[1],
                      box_sprite,
                      stone_sprite,
                      enemy_sprite,
                      user_sprite,
                      all_sprite)
    while running:
        if flag_pause is False:
            if count_destroyed_user in (1, 2) and len(user_sprite.sprites()) < 1:
                player_life -= 1
                life_sprite.sprites()[player_life].image_update()
                player = UserTank(images.user_tank,
                                  player_start_pos[0],
                                  player_start_pos[1],
                                  box_sprite,
                                  stone_sprite,
                                  enemy_sprite,
                                  user_sprite,
                                  all_sprite)
            if count_destroyed_user == 3:
                running = False
                pygame.quit()
                database.update_data(username=username, user=player_life, enemy=count_destroyed_enemy)
                pygame.mixer.init()
                pygame.init()
                main.menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        Patron(images.patron, player.rect.x, player.rect.y, angle, box_sprite,
                               stone_sprite,
                               user_sprite,
                               enemy_sprite,
                               patron_sprite,
                               all_sprite)
                    elif event.key == pygame.K_ESCAPE:
                        flag_pause = not flag_pause
                        pause = PauseMenu(images.pause, pause_sprite, all_sprite)
            keys = pygame.key.get_pressed()
            for bullet in patron_sprite.sprites():
                bullet.move()
            for enemy in enemy_sprite.sprites():
                enemy.move()
            if keys[control['up']]:
                target_angle = rotate_mapping_user['up']
                player.move('up')
            elif keys[control['down']]:
                target_angle = rotate_mapping_user['down']
                player.move('down')
            elif keys[control['left']]:
                target_angle = rotate_mapping_user['left']
                player.move('left')
            elif keys[control['right']]:
                target_angle = rotate_mapping_user['right']
                player.move('right')
            if target_angle != angle:
                angle = target_angle
                player.flip(angle)
            screen.fill(pygame.Color('black'))
            all_sprite.draw(screen)
            pygame.display.flip()
            clock.tick(fps)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        all_sprite.remove(pause_sprite.sprites()[0])
                        pause_sprite.empty()
                        flag_pause = not flag_pause
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        result = pause.click(pygame.mouse.get_pos())
                        if result == 'back_menu':
                            pygame.quit()
                            pygame.init()

                            main.menu()
                        elif result == 'back_game':
                            all_sprite.remove(pause_sprite.sprites()[0])
                            pause_sprite.empty()
                            flag_pause = not flag_pause


if __name__ == '__main__':
    game(filename='level_4.txt', control={'up': pygame.K_w,
                                          'down': pygame.K_s,
                                          'right': pygame.K_d,
                                          'left': pygame.K_a,
                                          'bullet': pygame.K_SPACE},
         username='admin', database=DataBase())
