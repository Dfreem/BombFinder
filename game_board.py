from typing import Tuple
import settings
from random import Random
import pygame
from typing import List
from cell import Cell


class GameBoard:

    def __init__(self, board_size: Tuple[int, int], window, num_mines=-1):
        """
        the minefield

        :type window: pygame.Surface
        :param window: the main game window
        :type num_mines: int
        :param num_mines: the number of mines on the board
        """

        # region instance variables
        self.parent_window = window
        '''the containing window that this game-board and all the cells belong to'''
        self.size = (self.cells_x, self.cells_y) = board_size
        '''the number of cells along either axis, ie size = [ width, height ]'''
        self.num_mines: int = num_mines
        '''number of mines on the board'''
        self.cells = [[
            Cell(window, (row, col))
            for row in range(self.cells_y)]
            for col in range(self.cells_x)
        ]
        '''a 2-d matrix of :class:`Cell`'s representing the game board'''
        # endregion

        self.build()
        # self.traverse(print)

    def build(self):
        rand = Random()
        dom = Random()
        mines_left = self.num_mines

        # populate new game-board with mines
        while mines_left > 0:
            row = rand.randint(0, len(self.cells) - 1)
            col = dom.randint(0, len(self.cells[0]) - 1)
            self.cells[row][col].value = settings.MINE
            mines_left -= 1
        for row in self.cells:
            for cell in row:
                if cell.value != -1:
                    cell.get_neighbors(self.cells)
                    for neighbor in cell.neighbors:
                        if neighbor.value == -1:
                            cell.value += 1
                    print(cell.value)

    def draw(self):
        """
        draw the game board and call each cells draw method. This method should be called once a frame

        :return: None
        """

        font_path = pygame.font.match_font(settings.Style.FONT_NAME.value)
        font = pygame.font.Font(font_path, 14)

        # draw a cell to it's own surface
        for row in self.cells:
            for cell in row:
                cell.draw()

        # score card telling how many mines are left to mark
        _ = pygame.draw.rect(self.parent_window,
                             settings.Style.POPUP_BG_COLOR.value,
                             (10, 5, 125, 30),
                             border_radius=5)
        _ = pygame.draw.rect(self.parent_window,
                             settings.Style.POPUP_FONT_COLOR.value,
                             (10, 5, 125, 30),
                             width=1,
                             border_radius=5)

        # mines left label
        mines_label = font.render("mines left: ", True, settings.Style.CELL_FONT_COLOR.value)
        mines_number = font.render(f"{self.num_mines}", True, settings.Style.MINE_COLOR.value)

        # copy to screen
        self.parent_window.blit(mines_label, (20, 10, 40, 40))
        self.parent_window.blit(mines_number, (100, 10, 40, 40))
        pygame.display.flip()

    def handle_click(self, buttons: Tuple[bool, bool, bool], pos: Tuple[int, int]):
        """
        handler method called when any mouse button is clicked. On normal click, calls to calculate value of cell

        :param buttons: a tuple of boolean values indicating which mouse buttons where clicked. 0=left, 1=middle,
        2=right
        :param pos: the position on screen that was clicked, (x, y)
        :return: the cell that was clicked or None
        """
        if buttons[0]:
            col, row = pos[0] // settings.Sizes.CELL_SIZE.value[0] - 1, pos[1] // settings.Sizes.CELL_SIZE.value[1] - 1
            cell = self.cells[row][col]
            if not cell.was_clicked and not cell.is_flagged:
                cell.clicked()
                self.get_adjacent_mines(cell)
                if cell.value > 0:
                    self.draw()
                elif cell.value == 0:
                    cell.get_neighbors(self.cells)
                    self.find_zeroes(cell)
                elif cell.value == -1:
                    self.reveal_mines()
                return cell

        elif buttons[2]:
            x, y = pos
            col, row = x // settings.Sizes.CELL_SIZE.value[0] - 1, y // settings.Sizes.CELL_SIZE.value[1] - 1
            current = self.cells[row][col]
            print("before", current.is_flagged)
            current.is_flagged = not current.is_flagged
            print("after", current.is_flagged)
            if current.is_flagged:
                self.num_mines -= 1
            elif not current.is_flagged:
                self.num_mines += 1

        return None

    def clear_visited(self):
        for row in self.cells:
            for cell in row:
                cell.visited = False

    def get_adjacent_mines(self, cell: Cell):
        """
        set the indicated cells value to the number of immidiatly adjacent mines touching it.

        :param cell: The cell to start with, the cell we want to check surroundings of.
        :return: None
        """

        if cell.value == settings.MINE:
            return
        cell.get_neighbors(self.cells)
        cell.value = 0
        for neighbor in cell.neighbors:
            if neighbor.value == settings.MINE:
                cell.value += 1

    def reveal_mines(self):
        """
        Show all the mines on the game board.

        :return: None
        """

        bomb_img = pygame.image.load("images/mine.png").convert_alpha()
        bomb_img = pygame.transform.scale(bomb_img, settings.Sizes.CELL_SIZE.value)
        for row in self.cells:
            for cell in row:
                if cell.value == -1:
                    self.parent_window.fill(settings.Style.MINE_COLOR.value, (cell.location, cell.size))
                    _ = pygame.draw.rect(self.parent_window, "black", (cell.location, cell.size), 1)
                    self.parent_window.blit(bomb_img, (cell.location, cell.size))

        pygame.display.flip()

    def find_zeroes(self, cell):
        """
        find all the zero value cells in the same grouping as cell

        :param cell: the zero value cell that was clicked
        :return: None
        """

        neighbors = cell.neighbors
        self.clear_visited()
        self._find_zeroes_rec(neighbors)

    def _find_zeroes_rec(self, neighbors) -> None:
        """
        private recursive helper method for finding all the connecting zeroes,
        Board must be built prior to calling this method.

        :type neighbors: List[Cell]
        :param neighbors: a list of adjacent cells
        :returns: recursive method continues calling itself until its complete
        """

        if len(neighbors) > 0:
            current = neighbors.pop(0)

            #  if we haven't checked this cell already, mark it as visited, refresh it's neighbors list, then search
            #  the list for zeroes.
            if not current.visited and not current.was_clicked:
                current.visited = True
                current.get_neighbors(self.cells)
                for cell in current.neighbors:
                    if cell.value == 0:
                        neighbors.append(cell)
                        neighbors.extend(cell.neighbors)
                        cell.clicked()
                    else:
                        for neighbor in cell.neighbors:
                            if neighbor.value == 0:
                                neighbor.clicked()
                return self._find_zeroes_rec(neighbors)
        return None
