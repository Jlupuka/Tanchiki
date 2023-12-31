import pygame
import config
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
degrees = (0, 180, 90, 270)
rotate_mapping = {key: degree for degree, key in zip(degrees, config.control.keys())}

count_destroyed_enemy = 0
count_destroyed_user = 0


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
        for sprite in box_sprite.sprites() + stone_sprite.sprites() + user_sprite.sprites():
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
                else:
                    count_destroyed_user += 1
                self.kill()
                sprite.kill()
                return True  # Столкновение с вражеским танком
        return False  # Нет столкновения


class Stone(BaseSprite):
    def __init__(self, image: pygame.Surface, x_pos: int, y_pos: int) -> None:
        super().__init__(image, x_pos, y_pos, all_sprite, stone_sprite)


class Dirt(BaseSprite):
    def __init__(self, image: pygame.Surface, x_pos: int, y_pos: int) -> None:
        super().__init__(image, x_pos, y_pos, all_sprite, dirt_sprite)


def sort_level(board_level: list[list[int]], images: Images) -> UserTank:
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
            if key == 'user':
                new_player = UserTank(image=images.user_tank, x_pos=value[0], y_pos=value[1])
            else:
                EnemyTank(image=images.enemy, x_pos=value[0], y_pos=value[1])
    return new_player


def main(filename: str) -> None:
    pygame.init()
    size = 640, 640
    screen = pygame.display.set_mode(size)
    images = Images(cell_size=32)
    load_bord = service.load_level(filename=filename)
    player = sort_level(load_bord, images)
    clock = pygame.time.Clock()
    fps = 75
    angle = target_angle = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Patron(images.patron, player.rect.x, player.rect.y, angle)
        for bullet in patron_sprite.sprites():
            bullet.move()
        keys = pygame.key.get_pressed()
        if keys[config.control['up']]:
            target_angle = rotate_mapping['up']
            player.move('up')
        elif keys[config.control['down']]:
            target_angle = rotate_mapping['down']
            player.move('down')
        elif keys[config.control['left']]:
            target_angle = rotate_mapping['left']
            player.move('left')
        elif keys[config.control['right']]:
            target_angle = rotate_mapping['right']
            player.move('right')
        if target_angle != angle:
            angle = target_angle
            player.flip(angle)
        screen.fill(pygame.Color('black'))
        all_sprite.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main(filename='level_3.txt')
