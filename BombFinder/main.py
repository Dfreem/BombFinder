# region imports
from typing import List
import pygame
import settings
from popups.play_again import PlayAgainPopup
from popups.difficulty_window import DifficultyPopup
from settings import Difficulty, Placement, Style
from cell import Cell
from game_board import BombField
# endregion

pygame.init()
pygame.font.init()

UNIT_X: int = Placement.POPUP_GRID_UNIT_X.value

UNIT_Y: int = Placement.POPUP_GRID_UNIT_Y.value

BOARD_COLOR: str = Style.BOARD_COLOR.value


def not_a_winner(field: BombField, correct: int):
    result_popup(field, f"Not all bombs \nhave been flagged\ncorrect: {correct}")
    field.num_mines = field.start_mines - correct
    for row in field.cells:
        for cell in row:
            if cell.is_flagged and cell.value != -1:
                cell.is_flagged = False
    pygame.display.flip()
    pygame.time.wait(3000)


def result_popup(field: BombField, result: str):
    screen = field.parent_window
    rect_placement = ((screen.get_width() // 2) - 100,
                      (screen.get_height() // 2) - 75)
    rect_size = (screen.get_width() * .4,
                 screen.get_height() * .5)
    pygame.draw.rect(screen, settings.Style.POPUP_BG_COLOR.value,
                     (rect_placement, rect_size))
    text_writer = pygame.font.Font(
        pygame.font.match_font(settings.Style.FONT_NAME.value),
        18)
    rendered_text = text_writer.render(result, True, settings.Style.POPUP_FONT_COLOR.value)
    screen.blit(rendered_text, ((UNIT_X * 6) - (rendered_text.get_width() // 2),
                                (UNIT_Y * 5) - (rendered_text.get_height() // 2)))


def check_if_winner(board: BombField):
    correct = 0
    for row in board.cells:
        for cell in row:
            if cell.is_flagged:
                if cell.value == settings.MINE:
                    correct += 1
    return correct


def get_board_size(difficulty: str | None):
    if difficulty is None:
        return -1
    size: settings.Sizes = eval(f"settings.Sizes.{difficulty}_BOARD_SIZE")
    return size.value


def get_number_of_mines(difficulty: str | None):
    if settings.DEBUG:
        return 1
    if difficulty is None:
        return -1
    new_difficulty: Difficulty = eval(f"settings.Difficulty.{difficulty}")
    percentage = 0.15 + (0.01 * new_difficulty.value)
    return int(eval(f"settings.Sizes.{difficulty}_BOARD_SIZE.value ** 2 * {percentage}"))


def get_screen_size(difficulty: str | None):
    if difficulty is None:
        return -1
    width: settings.Sizes = eval(f"settings.Sizes.{difficulty}_BOARD_SIZE")
    cell_size = settings.Sizes.CELL_SIZE.value
    margin = settings.Placement.MARGIN_WIDTH.value
    side_length = width.value * cell_size + margin
    return side_length, side_length



def main():

    # Ask the player what difficulty they would like to play on.
    popup = DifficultyPopup("Choose your difficulty")
    popup.create_buttons()
    difficulty = popup.run()
    # print(f"difficulty from main: {difficulty}")

    # difficulty dependent settings
    board_size = get_board_size(difficulty)
    window_size = get_screen_size(difficulty)
    num_mines = get_number_of_mines(difficulty)
    # Main game loop prep
    screen = pygame.display.set_mode(window_size)
    board = BombField(board_size, screen, num_mines=num_mines)
    clock = pygame.time.Clock()

    def main_loop():
        running = True
        while board.num_mines > 0 and running:

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
        return board

    board = main_loop()
    if board.num_mines == 0:
        is_winner = check_if_winner(board)
        if is_winner == 0:
            board.reveal_mines()
            result_popup(board, "YOU WIN!!!")
        else:
            not_a_winner(board, is_winner)
            main_loop()

    # close current pygame display before opening a popup window
    pygame.display.quit()

    # send control to the PlayAgain popup.
    play_again = PlayAgainPopup("Would you like to play again?")
    play_again.create_buttons()
    again = play_again.run()

    # return main so we don't get lost in a recursive stack.
    if again.value == "yes":
        return main()

    pygame.quit()


if __name__ == '__main__':
    main()
