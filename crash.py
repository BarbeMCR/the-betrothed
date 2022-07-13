import pygame
import sys
from menu import Menu

"""This file defines the crash screen."""

class Crash(Menu):
    """The crash screen class."""
    def __init__(self, display_surface, parent):
        """Initialize the base class and setup the elements.

        Arguments:
        display_surface -- the screen
        parent -- the parent class
        """
        self.display_surface = display_surface
        self.parent = parent
        self.background = './assets/menu/crash_bg.png'
        self.cursor = './assets/menu/cursor.png'
        self.layout = 'h'
        super().__init__(self.background, self.cursor, self.layout, self.display_surface, self.parent)
        self.x = 128
        self.y = 608
        self.step = 720
        self.tags = ['Save & Quit', 'Quit']
        self.tb_font = pygame.font.Font('./font.ttf', 12)

    def save_game(self):
        """Save and quit the game."""
        self.parent.save()
        self.quit()

    def quit(self):
        """A function for quitting the game."""
        pygame.quit()
        sys.exit()

    def print_traceback(self, tb):
        """Print the traceback.

        Arguments:
        tb -- the traceback as described in run()
        """
        y = 160
        for string in tb:
            text_surface = self.tb_font.render(string, False, 'white')
            self.display_surface.blit(text_surface, (32, y))
            y += 24

    def run(self, tb):
        """Update and draw everything.

        Arguments:
        tb -- a list of strings containing the traceback
        """
        pygame.mixer.music.stop()
        self.parent.events = pygame.event.get()
        super().run(self.tags, self.save_game, self.quit)
        self.print_traceback(tb)
