# region imports
import pygame
import settings
from popups.play_again import PlayAgainPopup
from popups.difficulty_window import DifficultyPopup
from settings import Difficulty, Placement, Style, Sizes
from cell import Cell
from game_board import BombField
# endregion

pygame.init()
pygame.font.init()

# region Magic numbers from settings.py
EASY = Difficulty.EASY.value
MEDIUM = Difficulty.MEDIUM.value
HARD = Difficulty.HARD.value
EASY_BOARD_SIZE = EASY_WIDTH, EASY_HEIGHT = Sizes.EASY_BOARD_SIZE.value
MEDIUM_BOARD_SIZE = MEDIUM_WIDTH, MEDIUM_HEIGHT = Sizes.MEDIUM_BOARD_SIZE.value
HARD_BOARD_SIZE = HARD_WIDTH, HARD_HEIGHT = Sizes.HARD_BOARD_SIZE.value

CELL_SIZE = Sizes.CELL_SIZE.value
MARGIN = Placement.MARGIN_OFFSET.value
BOARD_COLOR = Style.BOARD_COLOR.value
# endregion


def main():

    # Ask the player what difficulty they would like to play on.
    popup = DifficultyPopup()
    popup.create_buttons()
    difficulty = popup.run()

    # to change difficulty values, see settings.py
    # region Get Difficulty
    if difficulty == EASY:
        window_size = (EASY_WIDTH * CELL_SIZE[0] + MARGIN,
                       EASY_HEIGHT * CELL_SIZE[1] + MARGIN)
        board_size = EASY_BOARD_SIZE
        num_mines = Difficulty.EASY_MINES.value

    elif difficulty == MEDIUM:
        window_size = (MEDIUM_WIDTH * CELL_SIZE[0] + MARGIN,
                       MEDIUM_HEIGHT * CELL_SIZE[1] + MARGIN)
        board_size = MEDIUM_BOARD_SIZE
        num_mines = Difficulty.MED_MINES.value

    else:
        window_size = (HARD_WIDTH * CELL_SIZE[0] + MARGIN,
                       HARD_HEIGHT * CELL_SIZE[1] + MARGIN)
        board_size = HARD_BOARD_SIZE
        num_mines = Difficulty.HARD_MINES.value
    # endregion

    # Main game loop prep
    screen = pygame.display.set_mode(window_size)
    board = BombField(board_size, screen, num_mines=num_mines)
    clock = pygame.time.Clock()
    running = True

    # Main game loop. Popups handle their own loop via their overloaded run() method.
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()

            # all mouse clicks are sent to game-board to be handled.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_cell: Cell | None = board.handle_click(pygame.mouse.get_pressed(3), pygame.mouse.get_pos())
                if clicked_cell is not None and clicked_cell.value == -1:
                    running = False
                    pygame.time.wait(3000)

        # clear and redraw the board once per frame. GameBoard.draw() calls each cells draw() method.
        screen.fill(settings.Style.BOARD_COLOR.value)
        board.draw()
        _ = clock.tick(60) / 1000

    # close current pygame display before opening a popup window
    pygame.display.quit()

    # send control to the PlayAgain popup.
    play_again = PlayAgainPopup()
    play_again.create_buttons()
    again = play_again.run()

    # return main so we don't get lost in a recursive stack.
    if again.value == "yes":
        return main()

    pygame.quit()


if __name__ == '__main__':
    main()
