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


class DifficultyPopup(Popup):

    def __init__(self, text: str):
        super().__init__(text)

    def create_buttons(self):

        easy = RadioButton(self.window, "EASY", (UNIT_X * 3, UNIT_Y * 6))
        medium = RadioButton(self.window, "MEDIUM", (UNIT_X * 6, UNIT_Y * 6))
        hard = RadioButton(self.window, "HARD", (UNIT_X * 9, UNIT_Y * 6))

        self.buttons.append(easy)
        self.buttons.append(medium)
        self.buttons.append(hard)

    def handle_click(self, pos):
        for button in self.buttons:
            button_x = button.location[0]
            button_y = button.location[1]
            if button_y - RADIUS < pos[1] < button_y + RADIUS:
                if button_x - RADIUS < pos[0] < button_x + RADIUS:
                    print(f"handle_click in difficulty: {button.value}")
                    return button.value

    def run(self):
        return super().run()
