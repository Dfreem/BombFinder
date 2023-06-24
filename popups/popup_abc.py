from typing import List
import pygame
from abc import ABCMeta, abstractmethod
from settings import Placement, Style, Sizes
from popups.radio_button import RadioButton


SCREEN_SIZE = Sizes.POPUP_SCREEN_SIZE.value
BG_COLOR = Style.POPUP_BG_COLOR.value


class Popup(metaclass=ABCMeta):
    """
    ABCMeta for popup windows.

    :type buttons: List[RadioButton]
    :ivar buttons: a list of all the radio buttons in the popup.
    :type window: pygame.Surface
    :ivar window: the window this popup resides in

    """

    def __init__(self):
        self.buttons = []
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
        pygame.display.flip()

    def run(self):
        """Initiate the event loop for this pop window. returns the chosen option on exit.

        :returns: an int indicating the button option that was chosen chose.
        """
        difficulty = -1
        clock = pygame.time.Clock()
        while difficulty < 0:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    difficulty = 0
                    return difficulty
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]:
                        difficulty = self.handle_click(pygame.mouse.get_pos())
            _ = clock.tick(60) / 1000
        pygame.display.quit()
        return difficulty

    @abstractmethod
    def handle_click(self, pos):
        """
        call clicked() on each button, deal with the consequences

        :param pos: the mouse position at the time of the click
        :return:
        """
        pass
