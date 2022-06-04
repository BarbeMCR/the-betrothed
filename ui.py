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
        self.energy_bar = pygame.image.load('./assets/ui/energy_bar.png').convert_alpha()
        self.energy_rect = self.energy_bar.get_rect(topleft=(16, 80))
        self.energy_overflow_bar = pygame.image.load('./assets/ui/energy_overflow_bar.png').convert_alpha()
        self.energy_overflow_rect = self.energy_overflow_bar.get_rect(topleft=(64, 144))

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

    def display_energy(self, energy, max_energy):
        """Display the energy bar and statistics.

        Arguments:
        energy -- the current energy value
        max_energy -- the maximum energy value
        """
        # Preparation
        energy_bar_topleft = (self.energy_rect.topleft[0]+52, self.energy_rect.topleft[1]+28)
        energy_bar_width = 200
        energy_bar_height = 12
        # Drawing
        self.display_surface.blit(self.energy_bar, self.energy_rect)
        energy_statistics_surface = self.font.render(f'{energy} / {max_energy}', False, 'white')
        energy_statistics_rect = energy_statistics_surface.get_rect(midleft=(self.energy_rect.right+8, self.energy_rect.centery))
        self.display_surface.blit(energy_statistics_surface, energy_statistics_rect)
        energy_percentage = energy / max_energy
        energy_width = int(energy_bar_width * energy_percentage)
        energy_bar_rect = pygame.Rect((energy_bar_topleft), (energy_width, energy_bar_height))
        pygame.draw.rect(self.display_surface, '#0098db', energy_bar_rect)

    def display_energy_overflow(self, energy_overflow, max_energy_overflow):
        """Display the energy overflow bar.

        Arguments:
        energy_overflow -- the current energy overflow value
        max_energy_overflow -- the maximum energy overflow value
        """
        # Preparation
        energy_overflow_bar_topleft = (self.energy_overflow_rect.topleft[0]+4, self.energy_overflow_rect.topleft[1]+4)
        energy_overflow_bar_width = 52
        energy_overflow_bar_height = 12
        # Drawing
        self.display_surface.blit(self.energy_overflow_bar, self.energy_overflow_rect)
        energy_overflow_percentage = energy_overflow / max_energy_overflow
        energy_overflow_width = int(energy_overflow_bar_width * energy_overflow_percentage)
        energy_overflow_bar_rect = pygame.Rect((energy_overflow_bar_topleft), (energy_overflow_width, energy_overflow_bar_height))
        pygame.draw.rect(self.display_surface, '#0098db', energy_overflow_bar_rect)
