import settings
import pygame.draw


class RadioButton:
    def __init__(self, screen, value, location):
        self.location = location
        self.is_selected = False
        self.value = value
        self.parent_window = screen
        font_path = pygame.font.match_font(settings.Style.FONT_NAME.value)
        self.font = pygame.font.Font(font_path, 18)

    def draw(self):
        """
        Draw the radio button on the parent window. Should be called inside the game-loop before updating the display

        :return: a :class:`pygame.rect.Rect` representing the location and area of the button.
        """

        button = pygame.draw.circle(self.parent_window,
                                    "black",
                                    self.location,
                                    settings.Sizes.RADIO_BUTTON_RADIUS.value,
                                    3)
        text = self.font.render(f"{self.value}", True, settings.Style.POPUP_FONT_COLOR.value)
        offset_x = text.get_rect().width // 2
        self.parent_window.blit(text,
                                (self.location[0] - offset_x,
                                 self.location[1] - (text.get_rect().height * 2)))
        return button
