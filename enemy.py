import pygame
import random
from tile import AnimatedTile

"""This file defines all the enemy behavior."""

class Enemy(AnimatedTile):
    """The base enemy class."""
    def __init__(self, size, x, y, path, speed, health, damage, energy):
        """Initialize the parent AnimatedTile class.

        Arguments:
        size -- the tile size (can be a dummy value as it is only used to build the base Tile class)
        x -- the initial X position, measured in pixels from the left
        y -- the initial Y position, measured in pixels from the top
        path -- the folder with all the animation frames
        speed -- the enemy speed
        health -- the enemy health
        damage -- the damage the enemy deals
        energy -- the energy dropped by enemies
        """
        super().__init__(size, x, y, path)
        self.invincible = False
        self.hurt_time = 0
        self.speed = speed
        self.health = health
        self.damage = damage
        self.energy = energy
        self.toughness = random.choices([i for i in range(3)], [50, 25, 25])[0]
        self.health += self.toughness
        self.damage += int(self.toughness / 2)

    def move(self):
        """Move the enemy based on their speed."""
        if not self.invincible:
            self.rect.x += self.speed

    def flip(self):
        """Flip the enemy if it is going left."""
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        """Invert the enemy speed."""
        self.speed *= -1

    def tick_invincibility_timer(self):
        """Tick down the invincibility timer."""
        now = pygame.time.get_ticks()
        if self.invincible:
            if now - self.hurt_time >= 500:
                self.invincible = False

    def update(self, shift):
        """Update the enemy tile.

        Arguments:
        shift -- the camera shift
        """
        super().update(shift)
        self.move()
        self.flip()
        self.tick_invincibility_timer()

class Skeleton(Enemy):
    """This class defines the skeletons."""
    def __init__(self, size, x, y, path, offset):
        """Set the speed and the offset and initialize the parent Enemy class."""
        self.speed = random.randint(3, 6)
        self.health = 1
        self.damage = 1
        self.energy = random.randint(0, 3)
        super().__init__(size, x, y, path, self.speed, self.health, self.damage, self.energy)
        self.rect.y -= offset

    def update(self, shift):
        """Call Enemy().update()

        Arguments:
        shift -- the camera shift
        """
        super().update(shift)
