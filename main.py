import pygame

import settings
from popups.play_again import PlayAgainPopup
from popups.difficulty_window import DifficultyPopup
from settings import Difficulty, Placement, Style, Sizes
from cell import Cell
from game_board import GameBoard
pygame.init()
pygame.font.init()

EASY = Difficulty.EASY.value
MEDIUM = Difficulty.MEDIUM.value
HARD = Difficulty.HARD.value
EASY_BOARD_SIZE = EASY_WIDTH, EASY_HEIGHT = Sizes.EASY_BOARD_SIZE.value
MEDIUM_BOARD_SIZE = MEDIUM_WIDTH, MEDIUM_HEIGHT = Sizes.MEDIUM_BOARD_SIZE.value
HARD_BOARD_SIZE = HARD_WIDTH, HARD_HEIGHT = Sizes.HARD_BOARD_SIZE.value

CELL_SIZE = Sizes.CELL_SIZE.value
MARGIN = Placement.MARGIN_OFFSET.value
BOARD_COLOR = Style.BOARD_COLOR.value


def main():
    popup = DifficultyPopup()
    popup.create_buttons()
    difficulty = popup.run()
    running = True
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

    screen = pygame.display.set_mode(window_size)
    board = GameBoard(board_size, screen, num_mines=num_mines)
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_cell: Cell | None = board.handle_click(pygame.mouse.get_pressed(3), pygame.mouse.get_pos())
                if clicked_cell is not None and clicked_cell.value == -1:
                    running = False
                    pygame.time.wait(3000)
        screen.fill(settings.Style.BOARD_COLOR.value)
        board.draw()
        _ = clock.tick(60) / 1000
    pygame.display.quit()
    play_again = PlayAgainPopup()
    play_again.create_buttons()
    if play_again.run() == "yes":
        return main()

    pygame.quit()


if __name__ == '__main__':
    main()
