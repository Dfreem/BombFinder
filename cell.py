import pygame
from typing import Tuple, List
import settings


class Cell:
    def __init__(self, window: pygame.Surface, grid_index: Tuple[int, int], value=0):

        self.name: str
        self.id: int
        self.size = settings.Sizes.CELL_SIZE.value
        self.surf = pygame.Surface((self.size, self.size))
        self.grid_index = self.col, self.row = grid_index
        self.location = (self.x, self.y) = (self.col * self.size + settings.Placement.MARGIN_WIDTH.value // 2,
                                            self.row * self.size + settings.Placement.MARGIN_WIDTH.value // 2)
        self.is_flagged = False
        self.was_clicked = False
        self.value = 0 if value is None else value
        self.neighbors: List[Cell] = []
        self.parent_window = window
        self.visited = False

    def draw(self):
        font_path = pygame.font.match_font(settings.Style.FONT_NAME.value)
        font = pygame.font.Font(font_path, 16)
        if self.is_flagged:
            self.surf.fill(settings.Style.FLAGGED_CELL_COLOR.value)
        elif self.was_clicked:
            self.surf.fill(settings.Style.CLICKED_CELL_COLOR.value)
        else:
            self.surf.fill(settings.Style.NORMAL_CELL_COLOR.value)
        outline = pygame.draw.rect(self.surf, "#222222", self.surf.get_rect(), width=1)
        self.parent_window.blit(self.surf, ((self.x,
                                             self.y),
                                            (self.size, self.size)))
        if self.was_clicked and self.value > -1:
            cell_number = font.render(f"{self.value}", True, settings.Style.CELL_FONT_COLOR.value)
            self.parent_window.blit(cell_number, (self.x + (self.size // 3),
                                                  self.y + (self.size // 4),
                                                  self.size,
                                                  self.size))
        return outline

    def get_neighbors(self, board):
        """
        refresh this cell's neighbors list. The list on this cell is updated, nothing is returned.

        :type board: List[List[Cell]]
        :param board: a 2-d list of :class:`Cell` representing the game board
        :return: None
        """

        self.neighbors.clear()

        # the surrounding cells are in the rows and the columns immediately in front and behind this cell.
        rows = [self.row - 1, self.row, self.row + 1]
        cols = [self.col - 1, self.col, self.col + 1]

        # remove negative index if we are on an edge
        if rows[0] < 0:
            rows = rows[1:]
        elif rows[-1] >= len(board):
            rows = rows[:-1]
        if cols[0] < 0:
            cols = cols[1:]
        elif cols[-1] >= len(board[0]):
            cols = cols[:-1]
        for row in rows:
            for col in cols:
                current = board[row][col]
                self.neighbors.append(current)

    def clicked(self):
        if not self.is_flagged and not self.was_clicked:
            self.was_clicked = True
        self.draw()
        return self.value
