from enum import Enum
MINE = -1


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
    CELL_SIZE = (40, 40)
    EASY_BOARD_SIZE = (8, 8)
    MEDIUM_BOARD_SIZE = (12, 12)
    HARD_BOARD_SIZE = (15, 15)
    POPUP_SCREEN_SIZE = (400, 300)
    GAME_SCREEN_SIZE = (600, 500)


class Placement(Enum):
    MARGIN_OFFSET = 80
    POPUP_GRID_UNIT_X = Sizes.POPUP_SCREEN_SIZE.value[0] // 12
    POPUP_GRID_UNIT_Y = Sizes.POPUP_SCREEN_SIZE.value[1] // 12


class Difficulty(Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2
    CUSTOM = 3
    EASY_MINES = int(Sizes.EASY_BOARD_SIZE.value[0] ** 2 * 0.16)
    MED_MINES = int(Sizes.MEDIUM_BOARD_SIZE.value[0] ** 2 * 0.17)
    HARD_MINES = int(Sizes.HARD_BOARD_SIZE.value[0] ** 2 * 0.18)



