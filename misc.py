import csv
import os
import pygame
import datetime
from settings import tile_size

"""This file contains several miscellaneous functions."""

def import_folder(path):
    """Import everything present in a folder with only images and return the list of all imported surfaces.

    Arguments:
    path -- the folder to import
    """
    surface_list = []
    for _, _, image_list in os.walk(path):
        for image in image_list:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)
    return surface_list


def import_csv_layout(path):
    """Read a CSV data layer and return a list with several lists containing the data for each row.

    Arguments:
    path -- the CSV file to import
    """
    terrain_map = []
    with open(path) as map:
        level = csv.reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map

def import_sliced_graphics(path):
    """Slice an image atlas and return a list of those slices.

    Arguments:
    path -- the image atlas to slice
    """
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_width() / tile_size)
    tile_num_y = int(surface.get_height() / tile_size)
    sliced_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            tile_surface = pygame.Surface((tile_size, tile_size), flags = pygame.SRCALPHA)
            tile_surface.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            sliced_tiles.append(tile_surface)
    return sliced_tiles

def take_screenshot(display_surface):
    """Take a screenshot of the screen and save it to file.

    Arguments:
    display_surface -- the screen
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
    pygame.image.save(display_surface, f'./data/screenshots/screenshot_{timestamp}.png')
