import pygame
import random
from tile import AnimatedTile

"""This file defines all the enemy behavior."""

class Enemy(AnimatedTile):
    """The base enemy class."""
    def __init__(self, size, x, y, path, speed, health, damage, energy, melee_resistance, ranged_resistance, magical_resistance, parent):
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
        parent -- the 'Level' class
        """
        super().__init__(size, x, y, path)
        self.parent = parent
        self.now = pygame.time.get_ticks()
        self.invincible = False
        self.hurt_time = 0
        self.stun_duration = random.randint(400, 500)
        self.speed = speed
        self.real_speed = speed
        self.health = health
        self.damage = damage
        self.energy = energy
        self.melee_resistance = melee_resistance
        self.ranged_resistance = ranged_resistance
        self.magical_resistance = magical_resistance
        self.toughness = random.choices([i for i in range(3)], [50, 25, 25])[0]
        self.health += self.toughness
        self.damage += int(self.toughness / 2)

    def move(self):
        """Move the enemy based on their speed."""
        if not self.invincible:
            if self.now - self.hurt_time >= self.stun_duration:
                self.rect.x += self.real_speed
                #if not self.about_to_flip:
                #    self.rect.x += int(self.speed*60*delta)
                #else:
                #    self.rect.x += self.speed

    def apply_delta_deadzone(self, delta):
        """Calculate the real enemy speed based on the distance from the borders.

        Arguments:
        delta -- the time delta
        """
        deadzone_active = False
        for border in self.parent.border_sprites.sprites():
            if not deadzone_active:
                if abs(self.rect.left-border.rect.right) <= 32 or abs(self.rect.right-border.rect.left) <= 32:
                    deadzone_active = True
        if deadzone_active:
            self.real_speed = self.speed
        else:
            self.real_speed = int(self.speed*60*delta)

    def flip(self):
        """Flip the enemy if it is going left."""
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        """Invert the enemy speed."""
        self.speed *= -1

    def tick_timers(self):
        """Tick down the internal timers."""
        self.now = pygame.time.get_ticks()
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
        self.apply_delta_deadzone(delta)
        self.move()
        self.flip()
        self.tick_timers()

class Skeleton(Enemy):
    """This class defines the skeletons."""
    def __init__(self, size, x, y, path, offset, parent):
        """Set the speed and the offset and initialize the parent Enemy class."""
        self.parent = parent
        self.speed = random.randint(3, 6)
        self.health = 1
        self.damage = 1
        self.energy = random.randint(0, 3)
        self.melee_resistance = 0
        self.ranged_resistance = 0
        self.magical_resistance = 0
        super().__init__(size, x, y, path, self.speed, self.health, self.damage, self.energy, self.melee_resistance, self.ranged_resistance, self.magical_resistance, self.parent)
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
    def __init__(self, size, x, y, path, offset, parent):
        """Set the speed and the offset and initialize the parent Enemy class."""
        self.parent = parent
        self.speed = random.randint(4, 8)
        self.health = 2
        self.damage = 2
        self.energy = random.randint(0, 4)
        self.melee_resistance = 0
        self.ranged_resistance = 1
        self.magical_resistance = 1
        super().__init__(size, x, y, path, self.speed, self.health, self.damage, self.energy, self.melee_resistance, self.ranged_resistance, self.magical_resistance, self.parent)
        self.rect.y -= offset

    def update(self, shift, delta):
        """Call 'Enemy.update'.

        Arguments:
        shift -- the camera shift
        delta -- the time delta
        """
        super().update(shift, delta)
