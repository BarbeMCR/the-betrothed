# The Betrothed, a Python platformer built with Pygame
# Copyright (C) 2022  BarbeMCR
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((16, 32))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)

        # Player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 4
        self.gravity = 0.4
        self.jump_height = -8

    def get_input(self):
        """Gets the player input and moves it accordingly."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.direction.x = -1  # Left movement
        elif keys[pygame.K_d]:
            self.direction.x = 1  # Right movement
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.jump()

    def jump(self):
        """Makes the player jump."""
        self.direction.y = self.jump_height

    def apply_gravity(self):
        """Applies gravity to the player."""
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self):
        """Updates the player position."""
        self.get_input()
