from typing import Tuple, List, Any

import pygame
import config
import datetime
from game_field import service
from game_field.game_board import Images

all_sprite = pygame.sprite.Group()
box_sprite = pygame.sprite.Group()
user_sprite = pygame.sprite.Group()
dirt_sprite = pygame.sprite.Group()
stone_sprite = pygame.sprite.Group()
enemy_sprite = pygame.sprite.Group()
patron_sprite = pygame.sprite.Group()
width, height = 640, 640
left, top = 15, 20
cell_size = 32
degrees_user = (0, 180, 90, 270)
rotate_mapping_user = {key: degree for degree, key in zip(degrees_user, config.control.keys())}
degrees_enemy = (180, 0, 270, 90)
rotate_mapping_enemy = {key: degree for degree, key in zip(degrees_enemy, config.control.keys())}

count_destroyed_enemy = 0
count_destroyed_user = 0


def check_collision_at_direction(sprite: pygame.sprite, direction_x: int, direction_y: int) -> bool:
    new_rect = sprite.rect.copy()
    new_rect.x += direction_x * cell_size
    new_rect.y += direction_y * cell_size
    for sprite_group in (box_sprite, stone_sprite):
        for sprite_to_check in sprite_group.sprites():
            if sprite_to_check.rect.colliderect(new_rect):
                return True
    return False


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
    def __init__(self, image: list[pygame.Surface], x_pos: int, y_pos: int) -> None:
        super().__init__(image, x_pos, y_pos, all_sprite, user_sprite)
        self.index_image = 0
        self.angle = 0
        self.image = self.orig_image[self.index_image]
        self.rank_move = 1

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
        for sprite in box_sprite.sprites() + stone_sprite.sprites() + enemy_sprite.sprites():
            if new_rect.colliderect(sprite.rect):
                return True  # Столкновение с объектом
        return False  # Нет столкновения

    def flip(self, angle: int = None) -> None:
        self.image = pygame.transform.rotate(self.orig_image[self.index_image], angle)
        self.angle = angle


class EnemyTank(BaseSprite):
    def __init__(self, image: list[pygame.Surface], x_pos: int, y_pos: int) -> None:
        super().__init__(image, x_pos, y_pos, all_sprite, enemy_sprite)
        self.index_image = 0
        self.angle = 0
        self.image = self.orig_image[self.index_image]
        self.rank_move = 1
        self.target = None
        self.time_bullet = datetime.datetime.now()
        self.images = Images(cell_size=cell_size)

    def find_nearest_user(self) -> UserTank:
        nearest_user = None
        nearest_distance = float('inf')
        for user in user_sprite.sprites():
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
                    Patron(image=self.images.patron,
                           x_pos=self.rect.x,
                           y_pos=self.rect.y,
                           angle=self.angle + 180,
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
                    Patron(image=self.images.patron,
                           x_pos=self.rect.x,
                           y_pos=self.rect.y,
                           angle=self.angle + 180,
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
        for sprite in box_sprite.sprites() + stone_sprite.sprites() + user_sprite.sprites() + enemy_sprite.sprites():
            if self != sprite:
                if new_rect.colliderect(sprite.rect):
                    return True  # Столкновение с объектом
        return False  # Нет столкновения

    def flip(self, angle: int = None) -> None:
        self.image = pygame.transform.rotate(self.orig_image[self.index_image], angle)
        self.angle = angle


class Box(BaseSprite):
    def __init__(self, image: pygame.Surface, x_pos: int, y_pos: int) -> None:
        super().__init__(image, x_pos, y_pos, all_sprite, box_sprite)


class Patron(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x_pos: int, y_pos: int, angle: int, user: bool = True) -> None:
        super().__init__(all_sprite, patron_sprite)
        self.user = user
        self.image = image
        self.rect = self.image.get_rect().move(
            x_pos, y_pos
        )
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = angle
        self.wx = False
        self.wy = False
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
        for sprite in stone_sprite.sprites():
            if new_rect.colliderect(sprite.rect):
                self.kill()
                return True  # Столкновение с камнем
        for sprite in box_sprite.sprites():
            if new_rect.colliderect(sprite.rect):
                self.kill()
                sprite.kill()
                return True  # Столкновение с коробкой
        for sprite in enemy_sprite.sprites():
            if new_rect.colliderect(sprite.rect):
                if self.user:
                    count_destroyed_enemy += 1
                self.kill()
                if self.user:
                    sprite.kill()
                return True  # Столкновение с вражеским танком
        for sprite in user_sprite.sprites():
            if new_rect.colliderect(sprite.rect):
                if not self.user:
                    count_destroyed_user += 1
                self.kill()
                if not self.user:
                    sprite.kill()
                return True  # Столкновение с вражеским танком
        return False  # Нет столкновения


class Stone(BaseSprite):
    def __init__(self, image: pygame.Surface, x_pos: int, y_pos: int) -> None:
        super().__init__(image, x_pos, y_pos, all_sprite, stone_sprite)


class Dirt(BaseSprite):
    def __init__(self, image: pygame.Surface, x_pos: int, y_pos: int) -> None:
        super().__init__(image, x_pos, y_pos, all_sprite, dirt_sprite)


def sort_level(board_level: list[list[int]], images: Images) -> list[Any]:
    new_player = None
    tanks = {
        'user': list(),
        'enemy': list()
    }
    for row, row_data in enumerate(board_level):
        for col, col_data in enumerate(row_data):
            Dirt(image=images.default, x_pos=col, y_pos=row)
            match col_data:
                case pygame.K_0:
                    tanks['user'].append((col, row))
                case pygame.K_1:
                    Stone(image=images.stone, x_pos=col, y_pos=row)
                case pygame.K_2:
                    Box(image=images.box, x_pos=col, y_pos=row)
                case pygame.K_3:
                    Dirt(image=images.default, x_pos=col, y_pos=row)
                    tanks['enemy'].append((col, row))
    for key in tanks.keys():
        for value in tanks[key]:
            if key == 'enemy':
                EnemyTank(image=images.enemy, x_pos=value[0], y_pos=value[1])
    return tanks['user'][0]


def main(filename: str) -> None:
    pygame.init()
    size = 800, 640
    screen = pygame.display.set_mode(size)
    images = Images(cell_size=cell_size)
    load_bord = service.load_level(filename=filename)
    player_start_pos = sort_level(load_bord, images)
    player_life = 3
    clock = pygame.time.Clock()
    fps = 75
    angle = target_angle = 0
    running = True
    while running:
        if count_destroyed_user in (0, 1, 2) and len(user_sprite.sprites()) < 1:
            player_life -= 1
            player = UserTank(image=images.user_tank, x_pos=player_start_pos[0], y_pos=player_start_pos[1])
        if count_destroyed_user == 3:
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Patron(images.patron, player.rect.x, player.rect.y, angle)
        for bullet in patron_sprite.sprites():
            bullet.move()
        for enemy in enemy_sprite.sprites():
            enemy.move()
        keys = pygame.key.get_pressed()
        if keys[config.control['up']]:
            target_angle = rotate_mapping_user['up']
            player.move('up')
        elif keys[config.control['down']]:
            target_angle = rotate_mapping_user['down']
            player.move('down')
        elif keys[config.control['left']]:
            target_angle = rotate_mapping_user['left']
            player.move('left')
        elif keys[config.control['right']]:
            target_angle = rotate_mapping_user['right']
            player.move('right')
        if target_angle != angle:
            angle = target_angle
            player.flip(angle)
        screen.fill(pygame.Color('black'))
        all_sprite.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main(filename='level_4.txt')
