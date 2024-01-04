import pygame
import service


class Board:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.tank_position = None
        self.board = [[0] * cols for _ in range(rows)]
        self.left = 15
        self.top = 20
        self.cell_size = 32

    def get_cell(self, mouse_pos: tuple[int, int]) -> None | tuple[int, int]:
        x, y = mouse_pos
        if self.left <= x <= self.left + self.cols * self.cell_size and \
                self.top <= y <= self.top + self.rows * self.cell_size:
            cell_x = (x - self.left) // self.cell_size
            cell_y = (y - self.top) // self.cell_size
            return cell_x, cell_y
        return

    def on_click(self, cell_coords: tuple[int, int], type_key: int) -> None:
        x, y = cell_coords
        self.board[y][x] = type_key if not self.board[y][x] else 0

    def get_click(self, mouse_pos: tuple[int, int], type_key: int) -> None:
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell, type_key)

    def save_to_file(self) -> None:
        max_level = service.top_level()
        print(max_level)
        with open(f'levels/level_{max_level + 1}.txt', 'w') as file:
            for row in self.board:
                file.write(','.join(map(str, row)))
                file.write('\n')


class EditableBoard(Board):
    def __init__(self, rows: int, cols: int) -> None:
        super().__init__(rows, cols)
        self.box = service.load_image('box.png', 'landscape', size=self.cell_size)
        self.patron = service.load_image('patron.png', 'tanks', size=self.cell_size // 4)
        self.default = service.load_image('dirt.png', 'landscape', size=self.cell_size)
        self.stone = service.load_image('cobblestone.png', 'landscape', size=self.cell_size)
        self.user_tank = service.load_image('user_tank_1.png', 'tanks', 'users', size=self.cell_size)
        self.enemy = service.load_image('enemy_tank_1.png',
                                        'tanks', 'enemy',
                                        size=self.cell_size,
                                        rotate=True)

    def render(self, surface: pygame.Surface) -> None:
        for y in range(self.rows):
            for x in range(self.cols):
                surface.blit(self.default,
                             (self.left + x * self.cell_size, self.top + y * self.cell_size),
                             (0, 0, self.cell_size, self.cell_size)
                             )
                if self.board[y][x] == pygame.K_1:
                    surface.blit(self.stone,
                                 (self.left + x * self.cell_size, self.top + y * self.cell_size),
                                 (0, 0, self.cell_size, self.cell_size)
                                 )
                elif self.board[y][x] == pygame.K_0:
                    surface.blit(self.user_tank,
                                 (self.left + x * self.cell_size, self.top + y * self.cell_size),
                                 (0, 0, self.cell_size, self.cell_size)
                                 )
                elif self.board[y][x] == pygame.K_2:
                    surface.blit(self.box,
                                 (self.left + x * self.cell_size, self.top + y * self.cell_size),
                                 (0, 0, self.cell_size, self.cell_size)
                                 )
                elif self.board[y][x] == pygame.K_3:
                    surface.blit(self.enemy,
                                 (self.left + x * self.cell_size, self.top + y * self.cell_size),
                                 (0, 0, self.cell_size, self.cell_size)
                                 )

    def patron_load(self, surface: pygame.Surface) -> None:
        surface.blit(self.patron,
                     (self.left + self.tank_position[0] * self.cell_size + self.cell_size // 4 + 4,
                      self.top + (self.tank_position[1] - 1) * self.cell_size + self.cell_size - 8),
                     (0, 0, self.cell_size // 4, self.cell_size // 4)
                     )


def main():
    pygame.init()
    size = 640, 640
    screen = pygame.display.set_mode(size)
    life = EditableBoard(19, 19)
    clock = pygame.time.Clock()
    fps = 75
    running = True
    key_mode = user_tank = None
    patron = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if key_mode:
                    if event.button == 1:  # Нажатие левой кнопки мыши
                        mouse_position = pygame.mouse.get_pos()
                        x, y = life.get_cell(mouse_position)
                        if key_mode == pygame.K_0:
                            if user_tank is None:
                                user_tank = (x, y)
                                life.get_click(mouse_position, key_mode)
                                life.tank_position = user_tank
                            elif (x, y) == user_tank:
                                user_tank = None
                                life.get_click(mouse_position, key_mode)
                        else:
                            life.get_click(mouse_position, key_mode)
            elif event.type == pygame.KEYDOWN:
                if event.key == key_mode:
                    key_mode = None
                elif event.key == pygame.K_1:
                    key_mode = pygame.K_1
                elif event.key == pygame.K_0:
                    key_mode = pygame.K_0
                elif event.key == pygame.K_2:
                    key_mode = pygame.K_2
                elif event.key == pygame.K_3:
                    key_mode = pygame.K_3
                elif event.key == pygame.K_SPACE:
                    patron = True
                elif event.key == pygame.K_s:
                    life.save_to_file()
        screen.fill(pygame.Color('black'))
        life.render(screen)
        if patron and user_tank:
            life.patron_load(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()


if __name__ == '__main__':
    main()
