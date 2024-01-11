import pygame
from . import service
from . import game_board


class EditableBoard(game_board.Board):
    def __init__(self, rows: int, cols: int) -> None:
        super().__init__(rows, cols)

    def patron_load(self, surface: pygame.Surface) -> None:
        surface.blit(self.patron,
                     (self.left + self.tank_position[0] * self.cell_size + self.cell_size // 4 + 4,
                      self.top + (self.tank_position[1] - 1) * self.cell_size + self.cell_size - 8),
                     (0, 0, self.cell_size // 4, self.cell_size // 4)
                     )

    def save_to_file(self) -> None:
        max_level = service.top_level()
        print(max_level)
        with open(f'levels/level_{max_level + 1}.txt', 'w') as file:
            for row in self.board:
                file.write(','.join(map(str, row)))
                file.write('\n')


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
                        if bool(cord := life.get_cell(mouse_position)):
                            x, y = cord
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
