import pygame.display

import settings
from settings import Style, Sizes, Placement, Difficulty
from popups.radio_button import RadioButton
from popups.popup_abc import Popup
from pygame import font
font.init()

UNIT_X = Placement.POPUP_GRID_UNIT_X.value
UNIT_Y = Placement.POPUP_GRID_UNIT_Y.value
RADIUS = Sizes.RADIO_BUTTON_RADIUS.value
EASY = Difficulty.EASY.value
MEDIUM = Difficulty.MEDIUM.value
HARD = Difficulty.HARD.value


class DifficultyPopup(Popup):

    def __init__(self):
        super().__init__()

    def create_buttons(self):

        easy = RadioButton(self.window, "easy", (UNIT_X * 3, UNIT_Y * 3))
        medium = RadioButton(self.window, "medium", (UNIT_X * 6, UNIT_Y * 3))
        hard = RadioButton(self.window, "hard", (UNIT_X * 9, UNIT_Y * 3))

        self.buttons.append(easy)
        self.buttons.append(medium)
        self.buttons.append(hard)

    def handle_click(self, pos):
        for button in self.buttons:
            button_x = button.location[0]
            button_y = button.location[1]
            if button_y - RADIUS < pos[1] < button_y + RADIUS:
                if button_x - RADIUS < pos[0] < button_x + RADIUS:
                    if button.value == "easy":
                        return EASY
                    elif button.value == "medium":
                        return MEDIUM
                    elif button.value == "hard":
                        return HARD
        return -1

    def draw(self):
        super().draw()
        font_path = font.match_font(settings.Style.FONT_NAME.value)
        nova_font = font.Font(font_path)
        text = nova_font.render("Choose Your Difficulty", True, settings.Style.POPUP_FONT_COLOR.value)
        _ = self.window.blit(text, ((UNIT_X * 6) - (text.get_width() // 2), (UNIT_Y * 2)))
