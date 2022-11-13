import pygame
from misc import import_folder

"""This file contains the tile classes."""

class Tile(pygame.sprite.Sprite):
    """The base tile class."""
    def __init__(self, size, x, y):
        """Initialize the tile sprite.

        Arguments:
        size -- the tile size
        x -- the X position, measured in pixels from the left
        y -- the Y position, measured in pixels from the top
        """
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = (x, y))

    def update(self, shift):
        """Update the tile.

        Arguments:
        shift -- the camera shift
        """
        self.rect.x += shift

class StaticTile(Tile):
    """The base static tile class."""
    def __init__(self, size, x, y, surface):
        """Initialize the parent Tile class and create the static tile sprite.

        Arguments:
        size -- the tile size (can be a dummy value as it is only used to build the base Tile class)
        x -- the initial X position, measured in pixels from the left
        y -- the initial Y position, measured in pixels from the top
        surface -- the static tile image surface
        """
        super().__init__(size, x, y)
        self.image = surface
        self.rect = self.image.get_rect(topleft = (x, y))

class Tree(StaticTile):
    """A specialized StaticTile for the trees."""
    def __init__(self, size, x, y, path, offset):
        """Initialize the parent StaticTile class and offset the tree image correctly.

        Arguments:
        size -- the tile size (can be a dummy value as it is only used to build the base Tile class)
        x -- the initial X position, measured in pixels from the left
        y -- the initial Y position, measured in pixels from the top
        path -- the tree image
        offset -- the tree image offset
        """
        super().__init__(size, x, y, pygame.image.load(path).convert_alpha())
        offset_y = y - offset
        self.rect.topleft = (x, offset_y)

class AnimatedTile(Tile):
    """The base animated tile class."""
    def __init__(self, size, x, y, path):
        """Initialize the parent Tile class and setup the initial animated tile sprite.

        Arguments:
        size -- the tile size (can be a dummy value as it is only used to build the base Tile class)
        x -- the initial X position, measured in pixels from the left
        y -- the initial Y position, measured in pixels from the top
        path -- the folder with all the animation frames
        """
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft = (x, y))

    def animate(self, delta):
        """Animate the tile.

        Arguments:
        delta -- the time delta
        """
        self.frame_index += 0.1*60*delta
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift, delta):
        """Update the tile.

        Arguments:
        shift -- the camera shift
        delta -- the time delta
        """
        self.animate(delta)
        super().update(shift)

class Energy(AnimatedTile):
    """A specialized AnimatedTile for the energy items."""
    def __init__(self, size, x, y, path, value):
        """Initialize the parent AnimatedTile class.

        Arguments:
        size -- the tile size (can be a dummy value as it is only used to build the base Tile class)
        x -- the initial X position
        y -- the initial Y position
        path -- the folder with all the animation frames
        value -- the amount of energy to add after collection
        """
        super().__init__(size, x, y, path)
        self.value = value

    def update(self, shift, delta):
        """Update the energy tile.

        Arguments:
        shift -- the camera shift
        delta -- the time delta
        """
        super().update(shift, delta)
