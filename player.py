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
from misc import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_player_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.player_assets['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # Player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 4
        self.gravity = 0.4
        self.jump_height = -8

        # Player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left_wall = False
        self.on_right_wall = False

    def import_player_assets(self):
        """Imports and manages the assets for the player character."""
        player_path = './assets/player/'
        self.player_assets = {
            'run':  [],
            'idle': [],
            'jump': [],
            'fall': []
            }
        for animation in self.player_assets.keys():
            full_path = player_path + animation
            self.player_assets[animation] = import_folder(full_path)

    def animate(self):
        """Animates the player."""
        animation = self.player_assets[self.status]
        # Frame index loop
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)  # flip(image, X-axis, Y-axis)
            self.image = flipped_image

        # rect setup
        if self.on_ground and self.on_right_wall:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left_wall:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right_wall:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left_wall:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        else:  # Fallback for rect setup
            self.rect = self.image.get_rect(center = self.rect.center)

    def get_input(self):
        """Gets the player input and moves it accordingly."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.direction.x = -1  # Left movement
            self.facing_right = False
        elif keys[pygame.K_d]:
            self.direction.x = 1  # Right movement
            self.facing_right = True
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def get_status(self):
        """Retrieves the current status of the player."""
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def jump(self):
        """Makes the player jump."""
        self.direction.y = self.jump_height

    def apply_gravity(self):
        """Applies gravity to the player."""
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self):
        """Updates the player."""
        self.get_input()
        self.get_status()
        self.animate()
