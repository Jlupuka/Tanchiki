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
