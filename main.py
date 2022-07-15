import pygame as pg
from cell import Cell
from app import App
from random import choice


class SudokuGenerator(App):
    large_tiles = {}
    small_tiles = {}
    n_rows = n_cols = 9

    @classmethod
    def gen_tiles(cls, large_size, small_size, font_name='monospace'):
        large_font = pg.font.SysFont(font_name, large_size)
        small_font = pg.font.SysFont(font_name, small_size)

        Cell.large_tiles = {}
        Cell.small_tiles = {}
        for i in range(1, 10):
            Cell.large_tiles[i] = large_font.render(str(i), True, (0, 0, 0))
            Cell.small_tiles[i] = small_font.render(str(i), True, (0, 0, 0))

    def __init__(self):
        super().__init__()

        self.cell_size = int(self.width/self.n_rows)

        self.gen_tiles(self.cell_size, self.cell_size//3)

        self.board = [
            Cell(self.screen, i, j, pg.Rect(
                i * self.cell_size,
                j * self.cell_size,
                self.cell_size,
                self.cell_size
            )) for j in range(self.n_rows) for i in range(self.n_cols)
        ]
        self.non_collapsed = self.board.copy()
        self.current_cell: Cell = self.non_collapsed[0]
        self.next_cell: Cell = self.current_cell
        self.stack: list[Cell] = []

    def update(self, dt):
        if not self.pause and len(self.non_collapsed):

            least_entropy_list = []
            for cell in self.non_collapsed:
                if cell.entropy != self.non_collapsed[0].entropy:
                    break
                least_entropy_list.append(cell)

            print("------BEFORE------")
            print(f"Non Collapsed = {self.non_collapsed}")
            print(f"New List      = {least_entropy_list}")

            self.current_cell = choice(least_entropy_list)
            self.collapse(self.current_cell)
            self.adjust_possibilities(self.current_cell)
            self.pause = True

            print("------AFTER------")
            self.non_collapsed.sort(key=lambda x: x.entropy)
            least_entropy_list.sort(key=lambda x: x.entropy)

            print(f"Non Collapsed = {self.non_collapsed}")
            print(f"New List      = {least_entropy_list}")
            print("------NEXT------")

    def adjust_possibilities(self, source_cell):
        value = source_cell.value

        # Adjust possibilities in row of cell
        for col in range(9):
            index = col + (source_cell.row * self.n_cols)
            if self.board[index] is not source_cell:
                self.board[index].remove_possibility(value)

        # Adjust possibilities in column of cell
        for row in range(9):
            index = source_cell.col + (row * self.n_cols)
            if self.board[index] is not source_cell:
                self.board[index].remove_possibility(value)

        # Adjust possibilities in box of cell
        box_row = (source_cell.row // 3) * 3
        box_col = (source_cell.col // 3) * 3
        for row in range(3):
            for col in range(3):
                index = box_col + col + ((box_row + row) * self.n_cols)
                if self.board[index] is not source_cell:
                    self.board[index].remove_possibility(value)

    def collapse(self, cell: Cell):
        cell.value = choice(cell.possibilities)
        self.non_collapsed.remove(cell)

    def event_handler(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.pause = False

    def draw(self):
        self.screen.fill((255, 255, 255))
        # Draw vertical THIN lines
        for i in range(self.n_rows-1):
            cell = self.board[i]
            p1 = pg.Vector2(cell.rect.right, 0)
            p2 = pg.Vector2(cell.rect.right, self.height)
            pg.draw.line(self.screen, (0, 0, 0), p1, p2)

        # Draw horizontal THIN lines
        for i in range(self.n_rows-1):
            cell = self.board[i*self.n_cols]
            p1 = pg.Vector2(0, cell.rect.bottom)
            p2 = pg.Vector2(self.width, cell.rect.bottom)
            pg.draw.line(self.screen, (0, 0, 0), p1, p2)

        # Draw vertical THICK lines
        for i in range(2, 6, 3):
            cell = self.board[i]
            p1 = pg.Vector2(cell.rect.right, 0)
            p2 = pg.Vector2(cell.rect.right, self.height)
            pg.draw.line(self.screen, (0, 0, 0), p1, p2, 3)

        # Draw horizontal THICK lines
        for i in range(2, 6, 3):
            cell = self.board[i*self.n_cols]
            p1 = pg.Vector2(0, cell.rect.bottom)
            p2 = pg.Vector2(self.width, cell.rect.bottom)
            pg.draw.line(self.screen, (0, 0, 0), p1, p2, 3)

        for cell in self.board:
            cell.draw()


if __name__ == '__main__':
    SudokuGenerator().run()
    pass
