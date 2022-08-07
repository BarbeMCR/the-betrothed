import pygame
import sys
import datetime
import random
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
        self.font = pygame.font.Font(self.font_file, 32)
        self.x = 128
        self.y = 624
        self.step = 440
        self.tags = ['Get Report', 'Save & Quit', 'Quit']
        self.tb_font = pygame.font.Font(self.font_file, 12)
        self.report_font = pygame.font.Font(self.font_file, 18)
        self.comments = [
            "It worked in 2021...",
            "What did you do wrong this time?",
            "It's all BarbeMCR's fault. Don't blame me!",
            "Did you blow me up?",
            "Whoops!",
            "The problem lies somewhere in the pythonic catalyst",
            "Everything is falling apart. No problem, I'll blame you.",
            "I'll be with you in a couple millenia."
        ]

    def save_game(self):
        """Save and quit the game."""
        self.parent.save()
        self.quit()

    def quit(self):
        """A function for quitting the game."""
        pygame.quit()
        sys.exit()

    def get_report(self, tb):
        """Save a crash report to file.

        Arguments:
        tb -- the traceback as described in run()
        """
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
        with open(f'./data/reports/report_{timestamp}.txt', 'w') as report:
            report.write("-- BarbeMCR's The Betrothed Crash Report --\n")
            report.write(f"Timestamp: {timestamp}\n")
            report.write("# " + random.choice(self.comments) + "\n\n")
            for string in tb:
                report.write(string + '\n')
        confirmation = self.report_font.render(f"Crash report './data/reports/report_{timestamp}.txt' was saved.", False, 'white')
        confirmation_rect = confirmation.get_rect(center=self.display_surface.get_rect().center)
        self.display_surface.blit(confirmation, confirmation_rect)
        pygame.display.flip()
        pygame.time.wait(2000)
        self.cursor_pos = 1

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
        self.now = pygame.time.get_ticks()
        self.display_surface.blit(self.background, (0, 0))
        if self.now - self.gen_time >= 1000:
            self.get_input((lambda:self.get_report(tb), self.save_game, self.quit))
        self.display_cursor()
        self.display_text(self.tags)
        self.print_traceback(tb)
