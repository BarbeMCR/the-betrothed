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

import os
import pygame

def import_folder(path):
    """Imports all images in a folder and puts them in Pygame surfaces.
    This function will throw an error if anything other than images is present in the target folder.
    """
    surface_list = []
    for _, __, images in os.walk(path):
        for image in images:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)
    return surface_list
