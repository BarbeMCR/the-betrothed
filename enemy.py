import pygame
import random
from tile import AnimatedTile

"""This file defines all the enemy behavior."""

class Enemy(AnimatedTile):
    """The base enemy class."""
    def __init__(self, size, x, y, path, speed, health, damage, energy, melee_resistance, ranged_resistance, magical_resistance):
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
        melee_resistance -- the level of melee resistance
        ranged_resistance -- the level of ranged resistance
        magical_resistance -- the level of magical resistance
        """
        super().__init__(size, x, y, path)
        self.now = pygame.time.get_ticks()
        self.invincible = False
        self.hurt_time = 0
        self.just_flipped = False  # This is used to fix a bug where the enemies get "caught" on the border tiles
        self.flip_time = 0  # Dummy value
        self.stun_duration = random.randint(400, 500)
        self.speed = speed
        self.health = health
        self.damage = damage
        self.energy = energy
        self.melee_resistance = melee_resistance
        self.ranged_resistance = ranged_resistance
        self.magical_resistance = magical_resistance
        self.toughness = random.choices([i for i in range(3)], [50, 25, 25])[0]
        self.health += self.toughness
        self.damage += int(self.toughness / 2)

    def move(self, delta):
        """Move the enemy based on their speed.

        Arguments:
        delta -- the time delta
        """
        if not self.invincible:
            if self.now - self.hurt_time >= self.stun_duration:
                self.rect.x += int(self.speed*60*delta)

    def flip(self):
        """Flip the enemy if it is going left."""
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        """Invert the enemy speed."""
        if not self.just_flipped:
            self.speed *= -1
            self.just_flipped = True
            self.flip_time = pygame.time.get_ticks()

    def tick_timers(self):
        """Tick down the internal timers."""
        self.now = pygame.time.get_ticks()
        if self.just_flipped:
            if self.now - self.flip_time >= 50:
                self.just_flipped = False
        if self.invincible:
            if self.now - self.hurt_time >= 500:
                self.invincible = False

    def update(self, shift, delta):
        """Update the enemy tile.

        Arguments:
        shift -- the camera shift
        delta -- the time delta
        """
        super().update(shift, delta)
        self.move(delta)
        self.flip()
        self.tick_timers()

class Skeleton(Enemy):
    """This class defines the skeletons."""
    def __init__(self, size, x, y, path, offset):
        """Set the speed and the offset and initialize the parent Enemy class."""
        self.speed = random.randint(3, 6)
        self.health = 1
        self.damage = 1
        self.energy = random.randint(0, 3)
        self.melee_resistance = 0
        self.ranged_resistance = 0
        self.magical_resistance = 0
        super().__init__(size, x, y, path, self.speed, self.health, self.damage, self.energy, self.melee_resistance, self.ranged_resistance, self.magical_resistance)
        self.rect.y -= offset

    def update(self, shift, delta):
        """Call 'Enemy.update'.

        Arguments:
        shift -- the camera shift
        delta -- the time delta
        """
        super().update(shift, delta)

class Zombie(Enemy):
    """This class defines the zombies."""
    def __init__(self, size, x, y, path, offset):
        """Set the speed and the offset and initialize the parent Enemy class."""
        self.speed = random.randint(4, 8)
        self.health = 2
        self.damage = 2
        self.energy = random.randint(0, 4)
        self.melee_resistance = 0
        self.ranged_resistance = 1
        self.magical_resistance = 1
        super().__init__(size, x, y, path, self.speed, self.health, self.damage, self.energy, self.melee_resistance, self.ranged_resistance, self.magical_resistance)
        self.rect.y -= offset

    def update(self, shift, delta):
        """Call 'Enemy.update'.

        Arguments:
        shift -- the camera shift
        delta -- the time delta
        """
        super().update(shift, delta)
