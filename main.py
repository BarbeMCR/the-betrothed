#!/usr/bin/env python3

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
import sys
if sys.platform.startswith('win32'):
    import ctypes
from settings import *
from game import Game
from data import *

# Build identification
version = "0.07a"
build = 603
stable = True

# Pygame initialization
pygame.init()
if stable:
    pygame.display.set_caption(f"The Betrothed {version}")
else:
    pygame.display.set_caption(f"The Betrothed {version} - Build {build}")
if sys.platform.startswith('win32'):
    ctypes.windll.user32.SetProcessDPIAware()  # This makes the window the correct resolution
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SCALED, vsync=1)
icon = pygame.image.load('./icon.png').convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
game = Game(screen)

# Event loop
while True:
    for event in game.events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.JOYDEVICEADDED:
            controller = pygame.joystick.Joystick(event.device_index)
            game.controller.controllers[controller.get_instance_id()]
        if event.type == pygame.JOYDEVICEREMOVED:
            del game.controller.controllers[event.instance_id]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()

    screen.fill('black')
    game.run()

    pygame.display.update()
    clock.tick(60)
