import pygame
import random
from tile import AnimatedTile

"""This file defines all the enemy behavior."""

class Enemy(AnimatedTile):
    """The base enemy class."""
    def __init__(self, size, x, y, path, speed):
        """Initialize the parent AnimatedTile class.

        Arguments:
        size -- the tile size (can be a dummy value as it is only used to build the base Tile class)
        x -- the initial X position, measured in pixels from the left
        y -- the initial Y position, measured in pixels from the top
        path -- the folder with all the animation frames
        speed -- the enemy speed
        """
        super().__init__(size, x, y, path)
        self.speed = speed

    def move(self):
        """Move the enemy based on their speed."""
        self.rect.x += self.speed

    def flip(self):
        """Flip the enemy if it is going left."""
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        """Invert the enemy speed."""
        self.speed *= -1

    def update(self, shift):
        """Update the enemy tile.

        Arguments:
        shift -- the camera shift
        """
        super().update(shift)
        self.move()
        self.flip()

class Skeleton(Enemy):
    """This class defines the skeletons."""
    def __init__(self, size, x, y, path, offset):
        """Set the speed and the offset and initialize the parent Enemy class.

        Arguments:
        size -- the tile size (can be a dummy value as it is only used to build the base Tile class)
        x -- the initial X position, measured in pixels from the left
        y -- the initial Y position, measured in pixels from the top
        path -- the folder with all the animation frames
        offset -- the vertical offset (the bigger the value the higher the enemy)
        """
        self.speed = random.randint(3, 6)
        # self.speed_start = 1
        # self.speed_stop = 8
        super().__init__(size, x, y, path, self.speed)
        self.rect.y -= offset

    # def reverse(self):
        # speed_start = self.speed_start * -1
        # speed_stop = self.speed_stop * -1
        # self.speed_start = speed_stop
        # self.speed_stop = speed_start

    def update(self, shift):
        """Call Enemy().update()

        Arguments:
        shift -- the camera shift
        """
        # self.speed = random.randint(self.speed_start, self.speed_stop)
        super().update(shift)
