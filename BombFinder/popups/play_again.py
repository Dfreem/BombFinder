import pygame.display

from popups.radio_button import RadioButton
import settings
from settings import Placement, Style, Sizes
from popups.popup_abc import Popup
from pygame import font

UNIT_X = Placement.POPUP_GRID_UNIT_X.value
UNIT_Y = Placement.POPUP_GRID_UNIT_Y.value
RADIUS = Sizes.RADIO_BUTTON_RADIUS.value
CELL_SIZE = Sizes.CELL_SIZE.value
FONT_NAME = settings.Style.FONT_NAME.value
FONT_COLOR = settings.Style.POPUP_FONT_COLOR.value

font.init()


class PlayAgainPopup(Popup):
    def __init__(self, text):
        super().__init__(text)

    def create_buttons(self):

        yes = RadioButton(self.window, "yes", (UNIT_X * 4, UNIT_Y * 6))
        no = RadioButton(self.window, "no", (UNIT_X * 8, UNIT_Y * 6))

        self.buttons.append(yes)
        self.buttons.append(no)

    def handle_click(self, pos):
        y_offset = (CELL_SIZE // 2)
        x_offset = (CELL_SIZE // 2)
        button_y = self.buttons[0].location[1]
        low_y = button_y - y_offset
        high_y = button_y + y_offset
        in_range_y = low_y < pos[1] < high_y
        if in_range_y:
            for button in self.buttons:
                low_x = button.location[0] - x_offset
                high_x = button.location[0] + x_offset
                in_range_x = low_x < pos[0] < high_x
                if in_range_x:
                    return button

    # def draw(self):
    #     font_path = font.match_font(FONT_NAME)
    #     nova_font = font.Font(font_path, 18)
    #     title = nova_font.render(self.text, True, FONT_COLOR)
    #     text_x = UNIT_X * 6 - title.get_width() // 2
    #     text_y = UNIT_Y * 2
    #     square = self.window.blit(title, (text_x, text_y))
    #     super().draw()
    #     pygame.display.update(square)

    # def run(self):
    #     clock = pygame.time.Clock()
    #     chosen = False
    #     choice = None
    #     while not chosen:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 difficulty = 0
    #                 return difficulty
    #             elif event.type == pygame.MOUSEBUTTONDOWN:
    #                 if pygame.mouse.get_pressed(3)[0]:
    #                     choice = self.handle_click(pygame.mouse.get_pos())
    #                     if choice is not None:
    #                         chosen = True
    #         self.draw()
    #         _ = clock.tick(60) / 1000
    #     pygame.display.quit()
    #     return choice
