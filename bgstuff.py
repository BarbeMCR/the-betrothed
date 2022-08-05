import pygame
import random
from settings import *  # lgtm [py/polluting-import]
from tile import *  # lgtm [py/polluting-import]

"""This file defines all the background elements."""

class Sky:
    """This class defines the actual sky."""
    def __init__(self, horizon):
        """Create the sky tiles according to their height.

        Arguments:
        horizon -- the height of the horizon line, measured in tiles from the top
        """
        self.sky_top = pygame.image.load('./assets/level/sky/skytop.png').convert()
        self.sky_middle = pygame.image.load('./assets/level/sky/skymiddle.png').convert()
        self.sky_bottom = pygame.image.load('./assets/level/sky/skybottom.png').convert()
        self.horizon = horizon

        # Stretch tile
        self.sky_top = pygame.transform.scale(self.sky_top, (screen_width, tile_size))
        self.sky_middle = pygame.transform.scale(self.sky_middle, (screen_width, tile_size))
        self.sky_bottom = pygame.transform.scale(self.sky_bottom, (screen_width, tile_size))

    def draw(self, display_surface):
        """Draw the sky tiles to screen based on their height.

        Arguments:
        display_surface -- the screen
        """
        for row in range(y_tiles):
            y = row * tile_size
            if row < self.horizon:
                display_surface.blit(self.sky_top, (0, y))
            elif row == self.horizon:
                display_surface.blit(self.sky_middle, (0, y))
            else:
                display_surface.blit(self.sky_bottom, (0, y))

class Water:
    """This class defines the water you see at the bottom of pits."""
    def __init__(self, top, level_width, generate):
        """Create the water tiles if the generator allows it.

        Arguments:
        top -- the water level, measured in pixels from the top
        level_width -- the width of the level, measured in tiles
        generate -- water will be generated only if this flag is set to True
        """
        self.water_sprites = pygame.sprite.Group()
        if generate:
            water_start = -screen_width
            water_width = pygame.image.load('./assets/level/water/water1.png').get_width()
            water_x_tiles = int((level_width + 2 * screen_width) / water_width)
            for tile in range(water_x_tiles):
                x = tile * water_width + water_start
                y = top
                sprite = AnimatedTile(water_width, x, y, './assets/level/water')
                self.water_sprites.add(sprite)

    def draw(self, display_surface, shift):
        """Draw the water tiles to screen.

        Arguments:
        display_surface -- the screen
        shift -- the camera shift
        """
        self.water_sprites.update(shift)
        self.water_sprites.draw(display_surface)

class Clouds:
    """This class defines the clouds."""
    def __init__(self, horizon, level_width, cloud_number):
        """Create and place the clouds.

        Arguments:
        horizon -- the lowest point where clouds can generate, measured in pixels from the top
        level_width -- the width of the level, measured in tiles
        cloud_number -- the number of clouds to generate
        """
        self.level_width = level_width
        clouds = [
            './assets/level/sky/cloudsmall_day.png',
            './assets/level/sky/cloudmedium_day.png',
            './assets/level/sky/cloudlarge_day.png'
        ]
        cloud_start = -screen_width
        cloud_stop = self.level_width + screen_width
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()
        for tile in range(cloud_number):
            x = random.randrange(cloud_start, cloud_stop, 8)
            y = random.randrange(min_y, max_y, 16)
            cloud_surf = pygame.image.load(random.choice(clouds)).convert_alpha()
            sprite = StaticTile(0, x, y, cloud_surf)
            sprite.cooldown = random.randrange(300, 1500, 300)
            sprite.speed = random.randrange(1, 8)
            sprite.ticks = pygame.time.get_ticks()
            self.cloud_sprites.add(sprite)

    def move(self):
        """Move the clouds from right to left based on their speed and countdown values."""
        for sprite in self.cloud_sprites.sprites():
            now = pygame.time.get_ticks()
            if now - sprite.ticks >= sprite.cooldown:
                sprite.ticks = now
                sprite.rect.x -= sprite.speed
                if sprite.rect.x < -screen_width:
                    sprite.rect.x = self.level_width + screen_width

    def draw(self, display_surface, shift):
        """Draw the clouds to screen.

        Arguments:
        display_surface -- the screen
        shift -- the camera shift
        """
        self.move()
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(display_surface)

class Mountains:
    """This class defines the mountains in the background."""
    def __init__(self, top, level_width, generate):
        """Create the mountains if the generator allows it.

        Arguments:
        top -- the highest point where mountains can generate, measured in pixels from the top
        level_width -- the width of the level, measured in tiles
        generate -- mountains will be generated only if this flag is set to True
        """
        self.mountain_sprites = pygame.sprite.Group()
        if generate:
            mountain_surf = pygame.image.load('./assets/level/ground/mountain.png').convert_alpha()
            mountain_start = -screen_width
            mountain_width = mountain_surf.get_width()
            mountain_x_tiles = int((level_width + 2 * screen_width) / mountain_width)
            for tile in range(mountain_x_tiles):
                x = tile * mountain_width + mountain_start
                y = random.randrange(top, top+256, 32)
                sprite = StaticTile(0, x, y, mountain_surf)
                self.mountain_sprites.add(sprite)

    def draw(self, display_surface, shift):
        """Draw the mountains to screen.

        Arguments:
        display_surface -- the screen
        shift -- the camera shift
        """
        self.mountain_sprites.update(shift)
        self.mountain_sprites.draw(display_surface)
