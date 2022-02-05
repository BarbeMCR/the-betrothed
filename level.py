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
from tile import Tile
from settings import tile_size, screen_width
from player import Player


class Level:
    def __init__(self, level_data, display_surface):
        self.display_surface = display_surface
        self.setup(level_data)
        self.shift = 0
        self.current_x = 0

    def setup(self, layout):
        """Builds the level based on a given layout, then places the player inside."""
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if col == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if col == 'P':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < screen_width / 4 and direction_x < 0:
            self.shift = 4
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.shift = -4
            player.speed = 0
        else:
            self.shift = 0
            player.speed = 4

    def x_mov_coll(self):
        """Checks for horizontal movement and collisions."""
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left_wall = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right_wall = True
                    self.current_x = player.rect.right

        # Checks if the player is touching a wall on the left
        if player.on_left_wall and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left_wall = False
        if player.on_right_wall and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right_wall = False

    def y_mov_coll(self):
        """Checks for vertical movement and collisions."""
        player = self.player.sprite
        player.apply_gravity()
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        # Checks if the player is jumping
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        # Checks if the player is falling
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def run(self):
        """Draws the level and the player to screen."""
        # Tile drawing
        self.tiles.update(self.shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()
        # Player drawing
        self.player.update()
        self.x_mov_coll()
        self.y_mov_coll()
        self.player.draw(self.display_surface)
