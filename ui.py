import pygame

"""This file defines the UI elements."""

class UI:
    """The main UI class."""
    def __init__(self, display_surface):
        """Prepare things for displaying the actual UI.

        Arguments:
        display_surface -- the screen
        """
        self.display_surface = display_surface
        self.font = pygame.font.Font('./font.ttf', 20)
        self.health_bar = pygame.image.load('./assets/ui/health_bar.png').convert_alpha()
        self.health_rect = self.health_bar.get_rect(topleft=(16, 16))

    def display_health(self, health, max_health):
        """Display the health bar and statistics.

        Arguments:
        health -- the current health value
        max_health -- the maximum health value
        """
        # Preparation
        health_bar_topleft = (self.health_rect.topleft[0]+52, self.health_rect.topleft[1]+28)  # Those numbers must be hardcoded because they depend on the actual health bar image
        health_bar_width = 200
        health_bar_height = 12
        # Drawing
        self.display_surface.blit(self.health_bar, self.health_rect)
        health_statistics_surface = self.font.render(f'{health} / {max_health}', False, 'white')  # self.font.render(text, antialiasing, color)
        health_statistics_rect = health_statistics_surface.get_rect(midleft=(self.health_rect.right+8, self.health_rect.centery))
        self.display_surface.blit(health_statistics_surface, health_statistics_rect)
        health_percentage = health / max_health
        health_width = int(health_bar_width * health_percentage)
        health_bar_rect = pygame.Rect((health_bar_topleft), (health_width, health_bar_height))
        pygame.draw.rect(self.display_surface, '#dc4949', health_bar_rect)
