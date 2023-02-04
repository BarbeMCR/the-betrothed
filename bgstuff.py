import pygame
import random
from settings import *
from tile import *

"""This file defines all the background elements."""

class Sky:
    """This class defines the actual sky."""
    def __init__(self, horizon, scene):
        """Create the sky tiles according to their height.

        Arguments:
        horizon -- the height of the horizon line, measured in tiles from the top
        scene -- the time of the day
        """
        self.horizon = horizon
        if scene == 'day':
            self.sky_top = pygame.image.load('./assets/level/sky/skytop_day.png').convert()
            self.sky_middle = pygame.image.load('./assets/level/sky/skymiddle_day.png').convert()
            self.sky_bottom = pygame.image.load('./assets/level/sky/skybottom_day.png').convert()
        elif scene == 'night':
            self.sky = pygame.image.load('./assets/level/sky/sky_night.png').convert()
            self.stars = pygame.sprite.Group()
            star_surf = pygame.image.load('./assets/level/sky/star.png').convert()
            star_number = [random.randint(0, 10*(self.horizon-row)) for row in range(self.horizon)]
            for index, num in enumerate(star_number):
                for _ in range(num):
                    x = random.randrange(16, screen_width-16, 4)
                    y = random.randrange(tile_size*index+4, tile_size*index+60, 4)
                    sprite = StaticTile(0, x, y, star_surf)
                    self.stars.add(sprite)
        elif scene == 'dawn':
            self.sky_top = pygame.image.load('./assets/level/sky/skytop_dawn.png').convert()
            self.sky_middle = pygame.image.load('./assets/level/sky/skymiddle_dawn.png').convert()
            self.sky_bottom = pygame.image.load('./assets/level/sky/skybottom_dawn.png').convert()
        elif scene == 'dusk':
            self.sky_top = pygame.image.load('./assets/level/sky/skytop_dusk.png').convert()
            self.sky_middle = pygame.image.load('./assets/level/sky/skymiddle_dusk.png').convert()
            self.sky_bottom = pygame.image.load('./assets/level/sky/skybottom_dusk.png').convert()

    def draw(self, display_surface, scene):
        """Draw the sky tiles to screen based on their height.

        Arguments:
        display_surface -- the screen
        scene -- the time of the day
        """
        for row in range(y_tiles):
            y = row * tile_size
            if scene == 'night':
                display_surface.blit(self.sky, (0, y))
                self.stars.draw(display_surface)
            else:
                if row < self.horizon:
                    display_surface.blit(self.sky_top, (0, y))
                elif row == self.horizon:
                    display_surface.blit(self.sky_middle, (0, y))
                else:
                    display_surface.blit(self.sky_bottom, (0, y))

class Water:
    """This class defines the water you see at the bottom of pits."""
    def __init__(self, top, scene, level_width, generate):
        """Create the water tiles if the generator allows it.

        Arguments:
        top -- the water level, measured in pixels from the top
        scene -- the time of the day
        level_width -- the width of the level, measured in tiles
        generate -- water will be generated only if this flag is set to True
        """
        self.water_sprites = pygame.sprite.Group()
        if scene == 'day':
            path = './assets/level/water/day'
        elif scene == 'night':
            path = './assets/level/water/night'
        elif scene == 'dawn' or scene == 'dusk':
            path = './assets/level/water/dawn_dusk'
        if generate:
            water_start = -screen_width
            water_width = pygame.image.load('./assets/level/water/day/water1.png').get_width()
            water_x_tiles = int((level_width + 2 * screen_width) / water_width)
            for tile in range(water_x_tiles):
                x = tile * water_width + water_start
                y = top
                sprite = AnimatedTile(water_width, x, y, path)
                self.water_sprites.add(sprite)

    def draw(self, display_surface, shift, delta):
        """Draw the water tiles to screen.

        Arguments:
        display_surface -- the screen
        shift -- the camera shift
        delta -- the time delta
        """
        self.water_sprites.update(shift, delta)
        self.water_sprites.draw(display_surface)

class Clouds:
    """This class defines the clouds."""
    def __init__(self, horizon, scene, level_width, cloud_number):
        """Create and place the clouds.

        Arguments:
        horizon -- the lowest point where clouds can generate, measured in pixels from the top
        scene -- the time of the day
        level_width -- the width of the level, measured in tiles
        cloud_number -- the number of clouds to generate
        """
        self.level_width = level_width
        if scene == 'day':
            clouds = [
                './assets/level/sky/cloudsmall_day.png',
                './assets/level/sky/cloudmedium_day.png',
                './assets/level/sky/cloudlarge_day.png'
            ]
        elif scene == 'night':
            clouds = [
                './assets/level/sky/cloudsmall_night.png',
                './assets/level/sky/cloudmedium_night.png',
                './assets/level/sky/cloudlarge_night.png'
            ]
        elif scene == 'dawn' or scene == 'dusk':
            clouds = [
                './assets/level/sky/cloudsmall_dawn_dusk.png',
                './assets/level/sky/cloudmedium_dawn_dusk.png',
                './assets/level/sky/cloudlarge_dawn_dusk.png'
            ]
        cloud_start = -screen_width
        cloud_stop = self.level_width + screen_width
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()
        for _ in range(cloud_number):
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
    def __init__(self, top, scene, level_width, generate):
        """Create the mountains if the generator allows it.

        Arguments:
        top -- the highest point where mountains can generate, measured in pixels from the top
        scene -- the time of the day
        level_width -- the width of the level, measured in tiles
        generate -- mountains will be generated only if this flag is set to True
        """
        self.mountain_sprites = pygame.sprite.Group()
        if scene == 'day':
            path = './assets/level/ground/mountain_day.png'
        elif scene == 'night':
            path = './assets/level/ground/mountain_night.png'
        elif scene == 'dawn' or scene == 'dusk':
            path = './assets/level/ground/mountain_dawn_dusk.png'
        if generate:
            mountain_surf = pygame.image.load(path).convert_alpha()
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
