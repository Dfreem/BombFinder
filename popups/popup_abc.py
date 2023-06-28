from typing import List
import pygame
from pygame import font
from abc import ABCMeta, abstractmethod

import settings
from settings import Placement, Style, Sizes
from popups.radio_button import RadioButton


SCREEN_SIZE = Sizes.POPUP_SCREEN_SIZE.value
BG_COLOR = Style.POPUP_BG_COLOR.value
UNIT_X = Placement.POPUP_GRID_UNIT_X.value
UNIT_Y = Placement.POPUP_GRID_UNIT_Y.value


class Popup(metaclass=ABCMeta):
    """
    ABCMeta for popup windows.

    :type buttons: List[RadioButton]
    :ivar buttons: a list of all the radio buttons in the popup.
    :type window: pygame.Surface
    :ivar window: the window this popup resides in

    """

    def __init__(self, display_text: str | None, font_size=16):
        self.buttons = []
        self.text = display_text
        self.font_size = font_size
        self.window = pygame.display.set_mode(SCREEN_SIZE)

    @abstractmethod
    def create_buttons(self):
        """
        This method should create any :class:`RadioButton`'s for the popup window.
        The created buttons should be stored in this popup's window variable :ivar:`window`

        :return: None

        """
        pass

    def draw(self):
        """Call :method:`draw` on each button contained in the buttons list"""

        self.window.fill(BG_COLOR)
        for button in self.buttons:
            _ = button.draw()
        if self.text is not None:
            font_path = font.match_font(Style.FONT_NAME.value)
            nova_font = font.Font(font_path, 18)
            title = nova_font.render(self.text, True, Style.POPUP_FONT_COLOR.value)
            text_x = UNIT_X * 6 - title.get_width() // 2
            text_y = UNIT_Y * 2
            _ = self.window.blit(title, (text_x, text_y))
        pygame.display.flip()

    def run(self):
        """Initiate the event loop for this pop window. returns the chosen option on exit.

        :returns: an Enum indicating the button option that was chosen.
        """

        clock = pygame.time.Clock()
        chosen = False
        choice = None
        while not chosen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    chosen = True
                    return choice
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]:
                        choice = self.handle_click(pygame.mouse.get_pos())
                        if choice is not None:
                            chosen = True
                self.draw()
            _ = clock.tick(60) / 1000
        pygame.display.quit()
        return choice

    @abstractmethod
    def handle_click(self, pos):
        """
        call clicked() on each button, deal with the consequences

        :param pos: the mouse position at the time of the click
        :return:
        """
        pass
