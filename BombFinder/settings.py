from enum import Enum
MINE = -1
DEBUG = False


class Debug(Enum):
    BOARD_SIZE = (15, 15)


class Style(Enum):
    NORMAL_CELL_COLOR = "#A68A64"
    CLICKED_CELL_COLOR = "#B6AD90"
    FLAGGED_CELL_COLOR = "#656D4A"
    CELL_FONT_COLOR = "#344E41"
    BOARD_COLOR = "#582F0E"
    POPUP_BG_COLOR = "#D3792A"
    MINE_COLOR = "#ae2012"
    POPUP_FONT_COLOR = "#0F4C5C"
    FONT_NAME = "ArialRounded"


class Sizes(Enum):
    RADIO_BUTTON_RADIUS = 10
    CELL_SIZE = 40
    EASY_BOARD_SIZE = 8
    MEDIUM_BOARD_SIZE = 12
    HARD_BOARD_SIZE = 15
    POPUP_SCREEN_SIZE = (400, 300)
    GAME_SCREEN_SIZE = (600, 500)


class Placement(Enum):
    MARGIN_WIDTH = 80
    POPUP_GRID_UNIT_X = 400 // 12  # popup screen width // 12
    POPUP_GRID_UNIT_Y = 300 // 12  # popup screen height // 12


class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    CUSTOM = -1
    STOP = 0




