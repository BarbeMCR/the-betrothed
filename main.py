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
    import platform
from settings import *  # lgtm [py/polluting-import]
from game import Game

def main():
    # Build identification
    version = "0.11a"
    build = 705  # lgtm [py/unused-local-variable]
    build_id = 0  # lgtm [py/unused-local-variable]
    stable = True

    # Pygame initialization
    # The comments below the if-elif-else statements are used to suppress LGTM warnings about build identification
    pygame.init()
    if stable:  # lgtm [py/unreachable-statement]
        pygame.display.set_caption(f"The Betrothed {version}")  # lgtm [py/unreachable-statement]
    elif build_id == 0:  # lgtm [py/unreachable-statement]
        pygame.display.set_caption(f"The Betrothed {version} - Build {build}")  # lgtm [py/unreachable-statement]
    else:  # lgtm [py/unreachable-statement]
        pygame.display.set_caption(f"The Betrothed {version} - Build {build}.{build_id}")  # lgtm [py/unreachable-statement]
    if sys.platform.startswith('win32'):
        if platform.version().startswith(('10.0', '6.3')):
            ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
        elif platform.version().startswith(('6.2', '6.1', '6.0')):
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
                game.controller.controllers[controller.get_instance_id()] = controller
            if event.type == pygame.JOYDEVICEREMOVED:
                del game.controller.controllers[event.instance_id]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()

        screen.fill('black')
        game.run()

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()
