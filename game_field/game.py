import pygame
from game_field import service
from game_field.game_board import Images

all_sprite = pygame.sprite.Group()
box_sprite = pygame.sprite.Group()
user_sprite = pygame.sprite.Group()
dirt_sprite = pygame.sprite.Group()
stone_sprite = pygame.sprite.Group()
enemy_sprite = pygame.sprite.Group()
patron_sprite = pygame.sprite.Group()
left = 15
top = 20
cell_size = 32


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x_pos: int, y_pos: int, *groups) -> None:
        super().__init__(*groups)
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect().move(
            self.x_pos * cell_size + left,
            self.y_pos * cell_size + top
        )
        self.mask = pygame.mask.from_surface(self.image)


class UserTank(BaseSprite):
    def __init__(self, image: pygame.Surface, x_pos: int, y_pos: int) -> None:
        super().__init__(image, x_pos, y_pos, all_sprite, user_sprite)


class EnemyTank(BaseSprite):
    def __init__(self, image: pygame.Surface, x_pos: int, y_pos: int) -> None:
        super().__init__(image, x_pos, y_pos, all_sprite, user_sprite)


class Box(BaseSprite):
    def __init__(self, image: pygame.Surface, x_pos: int, y_pos: int) -> None:
        super().__init__(image, x_pos, y_pos, all_sprite, user_sprite)


class Patron(BaseSprite):
    def __init__(self, image: pygame.Surface, x_pos: int, y_pos: int) -> None:
        super().__init__(image, x_pos, y_pos, all_sprite, user_sprite)


class Stone(BaseSprite):
    def __init__(self, image: pygame.Surface, x_pos: int, y_pos: int) -> None:
        super().__init__(image, x_pos, y_pos, all_sprite, user_sprite)


class Dirt(BaseSprite):
    def __init__(self, image: pygame.Surface, x_pos: int, y_pos: int) -> None:
        super().__init__(image, x_pos, y_pos, all_sprite, user_sprite)


def sort_level(board_level: list[list[int]], images: Images) -> tuple[UserTank, int, int]:
    new_player = row = col = None
    for row, row_data in enumerate(board_level):
        for col, col_data in enumerate(row_data):
            match col_data:
                case pygame.K_0:
                    Dirt(image=images.default, x_pos=col, y_pos=row)
                    new_player = UserTank(image=images.user_tank, x_pos=col, y_pos=row)
                case pygame.K_1:
                    Stone(image=images.stone, x_pos=col, y_pos=row)
                case pygame.K_2:
                    Box(image=images.box, x_pos=col, y_pos=row)
                case pygame.K_3:
                    Dirt(image=images.default, x_pos=col, y_pos=row)
                    EnemyTank(image=images.enemy, x_pos=col, y_pos=row)
                case _:
                    Dirt(image=images.default, x_pos=col, y_pos=row)
    return new_player, row, col


def main(filename: str) -> None:
    pygame.init()
    size = 640, 640
    screen = pygame.display.set_mode(size)
    images = Images(cell_size=32)
    load_bord = service.load_level(filename=filename)
    player, x, y = sort_level(load_bord, images)
    clock = pygame.time.Clock()
    fps = 75
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(pygame.Color('black'))
        all_sprite.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main(filename='level_3.txt')
