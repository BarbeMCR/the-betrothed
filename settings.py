"""This file contains various settings that need to be easily accessible."""

y_tiles = 11
tile_size = 64

screen_height = y_tiles * tile_size
screen_width = 1280

# Controller mappings

xbox_one = {  # Xbox One / Xbox Series X|S Controller (also works with Xbox 360 Controller)
    'buttons': {
        'A': 0,
        'B': 1,
        'X': 2,
        'Y': 3,
        'LB': 4,
        'RB': 5,
        'VIEW': 6,
        'MENU': 7,
        'LSTICK': 8,
        'RSTICK': 9,
        'LOGO': 10,
        'SHARE': 11
    },
    'hat': {
        'CENTER': (0, 0),
        'LEFT': (-1, 0),
        'RIGHT': (1, 0),
        'DOWN': (0, -1),
        'UP': (0, 1),
        'LEFT_DOWN': (-1, -1),
        'RIGHT_DOWN': (1, -1),
        'LEFT_UP': (-1, 1),
        'RIGHT_UP': (1, 1)
    },
    'axes': {
        'LSTICK_X': 0,
        'LSTICK_Y': 1,
        'RSTICK_X': 2,
        'RSTICK_Y': 3,
        'LT': 4,
        'RT': 5
    }
}
ps4 = {  # DualShock 4
    'buttons': {
        'A': 0,  # CROSS
        'B': 1,  # CIRCLE
        'X': 2,  # SQUARE
        'Y': 3,  # TRIANGLE
        'VIEW': 4,  # SHARE
        'LOGO': 5,
        'MENU': 6,  # OPTIONS
        'LSTICK': 7,  # L3
        'RSTICK': 8,  # R3
        'LB': 9,  # L1
        'RB': 10,  # R1
        'UP': 11,
        'DOWN': 12,
        'LEFT': 13,
        'RIGHT': 14,
        'SHARE': 15  # TOUCHPAD_CLICK
    },
    'axes': {
        'LSTICK_X': 0,
        'LSTICK_Y': 1,
        'RSTICK_X': 2,
        'RSTICK_Y': 3,
        'LT': 4,  # L2
        'RT': 5  # R2
    }
}

controllers = {
    'xbox_one': xbox_one,
    'ps4': ps4
}
