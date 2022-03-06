import csv
import os
import pygame
from settings import tile_size

def import_folder(path):
    surface_list = []
    for _, __, image_list in os.walk(path):
        for image in image_list:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)
    return surface_list


def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = csv.reader(map, delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map

def import_sliced_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0]) / tile_size
    tile_num_y = int(surface.get_size()[1]) / tile_size
    sliced_tiles = []
    for row in range(int(tile_num_y)):
        for col in range(int(tile_num_x)):
            x = col * tile_size
            y = row * tile_size
            tile_surface = pygame.Surface((tile_size, tile_size), flags = pygame.SRCALPHA)
            tile_surface.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            sliced_tiles.append(tile_surface)
    return sliced_tiles
