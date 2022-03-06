import pygame
import random
from settings import *
from tile import *

class Sky:
    def __init__(self, horizon):
        self.sky_top = pygame.image.load('./assets/level/sky/skytop.png').convert()
        self.sky_middle = pygame.image.load('./assets/level/sky/skymiddle.png').convert()
        self.sky_bottom = pygame.image.load('./assets/level/sky/skybottom.png').convert()
        self.horizon = horizon

        # Stretch tile
        self.sky_top = pygame.transform.scale(self.sky_top, (screen_width, tile_size))
        self.sky_middle = pygame.transform.scale(self.sky_middle, (screen_width, tile_size))
        self.sky_bottom = pygame.transform.scale(self.sky_bottom, (screen_width, tile_size))

    def draw(self, display_surface):
        for row in range(y_tiles):
            y = row * tile_size
            if row < self.horizon:
                display_surface.blit(self.sky_top, (0, y))
            elif row == self.horizon:
                display_surface.blit(self.sky_middle, (0, y))
            else:
                display_surface.blit(self.sky_bottom, (0, y))

class Water:
    def __init__(self, top, level_width):
        water_start = -screen_width
        water_width = 128  # This is a hardcoded value for the water image width
        water_x_tiles = int((level_width + 2 * screen_width) / water_width)
        self.water_sprites = pygame.sprite.Group()
        for tile in range(water_x_tiles):
            x = tile * water_width + water_start
            y = top
            sprite = AnimatedTile(water_width, x, y, './assets/level/water')
            self.water_sprites.add(sprite)

    def draw(self, display_surface, shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(display_surface)

class Clouds:
    def __init__(self, horizon, level_width, cloud_number):
        cloud_surf = pygame.image.load('./assets/level/sky/cloud.png').convert_alpha()
        cloud_start = -screen_width
        cloud_stop = level_width + screen_width
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()
        for tile in range(cloud_number):
            x = random.randrange(cloud_start, cloud_stop, 8)
            y = random.randrange(min_y, max_y, 16)
            sprite = StaticTile(0, x, y, cloud_surf)
            self.cloud_sprites.add(sprite)

    def draw(self, display_surface, shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(display_surface)

class Mountains:
    def __init__(self, top, level_width, generate):
        mountain_surf = pygame.image.load('./assets/level/ground/mountain.png').convert_alpha()
        mountain_start = -screen_width
        mountain_width = 1024
        mountain_x_tiles = int((level_width + 2 * screen_width) / mountain_width)
        self.mountain_sprites = pygame.sprite.Group()
        if generate:
            for tile in range(mountain_x_tiles):
                x = tile * mountain_width + mountain_start
                y = random.randrange(top, top+256, 32)
                sprite = StaticTile(0, x, y, mountain_surf)
                self.mountain_sprites.add(sprite)

    def draw(self, display_surface, shift):
        self.mountain_sprites.update(shift)
        self.mountain_sprites.draw(display_surface)
