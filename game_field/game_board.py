import os
import pygame
from game_field import service


class Images:
    def __init__(self, cell_size: int) -> None:
        self.box = service.load_image('box.png', 'landscape', size=cell_size)
        self.patron = service.load_image('patron.png', 'tanks', size=cell_size // 4)
        self.default = service.load_image('dirt.png', 'landscape', size=cell_size)
        self.stone = service.load_image('cobblestone.png', 'landscape', size=cell_size)
        # self.user_tank = service.load_image('user_tank_1.png', 'tanks', 'users', size=cell_size)
        # self.enemy = service.load_image('enemy_tank_1.png',
        #                                 'tanks', 'enemy',
        #                                 size=cell_size,
        #                                 rotate=True)
        self.enemy = service.load_animation(True, 'tanks', 'enemy')
        self.user_tank = service.load_animation(False, 'tanks', 'users')


class Board(Images):
    def __init__(self, rows: int, cols: int) -> None:
        super().__init__(cell_size=32)
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
