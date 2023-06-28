from typing import Tuple
import settings
from random import Random
import pygame
from typing import List
from cell import Cell


def get_adjacent_mines(cell: Cell):
    """
    set the indicated cells value to the number of immediately adjacent mines touching it.

    :param cell: The cell to start with, the cell we want to check surroundings of.
    :return: None
    """
    # print(f"cell value before get_adjacent_mine: {cell.value}")
    if cell.value == settings.MINE:
        return
    num_mines = 0
    for neighbor in cell.neighbors:
        # print(f"neighbor value [GameBoard: line 21]: {neighbor.value}\nNeighbors left: "
        #       f"{cell.neighbors.index(neighbor)}")
        if neighbor.value == settings.MINE:
            num_mines += 1
    cell.value = num_mines


class BombField:

    def __init__(self, board_size: int, window, num_mines=-1):
        """
        A call to BombField's :method:`draw()` method should happen once a frame.

        :type window: pygame.Surface
        :param window: the main game window
        :type num_mines: int
        :param num_mines: the number of mines on the board
        """

        # region instance variables
        self.parent_window = window
        '''the containing window that this game-board and all the cells belong to'''
        self.size = board_size
        '''the number of cells along either axis, ie size = [ width, height ]'''
        self.start_mines: int
        '''keep track of how many mines the game starts with'''
        self.num_mines: int
        '''number of mines on the board'''
        self.num_mines = self.start_mines = num_mines

        self.cells = [[
            Cell(window, (row, col))
            for row in range(self.size)]
            for col in range(self.size)
        ]
        '''a 2-d matrix of :class:`Cell`'s representing the game board'''
        for cell in self.cells:
            print(cell[0].value)
        self.running = False
        # endregion

        self._build()

    def _build(self):
        """
        Fill the game board with the specified number of mines in settings.py.

        :return: None
        """

        # use two instances of random because it makes me feel better
        rand = Random()
        dom = Random()
        mines_left = self.num_mines
        # print(f"num_mines in _build \n[GameBoard: line 68")
        # populate new game-board with mines
        while mines_left >= 0:
            row = rand.randint(0, len(self.cells) - 1)
            col = dom.randint(0, len(self.cells[0]) - 1)
            if self.cells[row][col].value != settings.MINE:
                self.cells[row][col].value = settings.MINE
                current = self.cells[row][col]
                print(f"cell value in _build after seeding: {(row, col)}: {current.value}")
                mines_left -= 1

        for row in self.cells:
            for cell in row:
                # print(f"cell value in build \n[GameBoard: line 79]: {cell.value}")
                if cell.value != -1:
                    cell.get_neighbors(self.cells)
                    get_adjacent_mines(cell)

    def draw(self):
        """
        draw the game board and call each cells draw method. This method should be called once a frame

        :return: None
        """

        font_path = pygame.font.match_font(settings.Style.FONT_NAME.value)
        font = pygame.font.Font(font_path, 14)

        # draw a cell to its own surface
        for row in self.cells:
            for cell in row:
                cell.draw()

        # scorecard telling how many mines are left to mark
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
        Process the location and which mouse button (left, middle, right) was pressed when a mouse click happens

        :param buttons: a tuple of boolean values indicating which mouse buttons where clicked
        :param pos: the position on screen that was clicked, (x, y)
        :return: the cell that was clicked or None
        """
        # normal left mouse click to reveal a cell
        if buttons[0]:
            row = (pos[1] // settings.Sizes.CELL_SIZE.value) - 1
            col = (pos[0] // settings.Sizes.CELL_SIZE.value) - 1
            cell = self.cells[row][col]
            print(pos)
            # ignore cells that have been dealt with
            if not cell.was_clicked and not cell.is_flagged:

                # refresh cell value then reveal
                # get_adjacent_mines(cell)
                cell.clicked()
                if cell.value > 0:
                    self.draw()
                elif cell.value == 0:
                    self.find_zeroes(cell)
                elif cell.value == settings.MINE:
                    self.reveal_mines()
                return cell

        # mouse_button[2] == right mouse. Flag the cell as possible bomb.
        elif buttons[2]:
            x, y = pos
            col, row = x // settings.Sizes.CELL_SIZE.value - 1, y // settings.Sizes.CELL_SIZE.value- 1
            current = self.cells[row][col]

            # toggle flagged ivar, changes color
            current.is_flagged = not current.is_flagged

            # mine counter tracking
            if current.is_flagged:
                self.num_mines -= 1
            elif not current.is_flagged:
                self.num_mines += 1

        return None

    def reveal_mines(self):
        """
        Show all the mines on the game board.

        :return: None
        """

        bomb_img = pygame.image.load("images/mine.png").convert_alpha()
        bomb_img = pygame.transform.scale(bomb_img, (settings.Sizes.CELL_SIZE.value, settings.Sizes.CELL_SIZE.value))
        for row in self.cells:
            for cell in row:
                if cell.value == -1:
                    self.parent_window.fill(settings.Style.MINE_COLOR.value, (cell.location, (cell.size, cell.size)))
                    _ = pygame.draw.rect(self.parent_window, "black", (cell.location, (cell.size, cell.size)), 1)
                    self.parent_window.blit(bomb_img, (cell.location, (cell.size, cell.size)))

        pygame.display.flip()

    def find_zeroes(self, cell):
        """
        find all the zero value cells in the same grouping as cell

        :param cell: the zero value cell that was clicked
        :return: None
        """

        neighbors = cell.neighbors
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
            #  if we haven't checked this cell already, mark it as visited, refresh its neighbors list, then search
            #  the list for zeroes.
            if not current.visited and not current.was_clicked:

                current.visited = True
                for neighbor in current.neighbors:
                    if neighbor.value == 0:
                        neighbor.clicked()
                        for cell in neighbor.neighbors:
                            cell.clicked()
                        neighbors.extend(neighbor.neighbors)

            return self._find_zeroes_rec(neighbors)
        return None
