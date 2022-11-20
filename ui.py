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
        self.health_remainder_bar = pygame.image.load('./assets/ui/health_remainder_bar.png').convert_alpha()
        self.health_remainder_rect = self.health_remainder_bar.get_rect(topleft=(16, 144))
        self.energy_bar = pygame.image.load('./assets/ui/energy_bar.png').convert_alpha()
        self.energy_rect = self.energy_bar.get_rect(topleft=(16, 80))
        self.energy_overflow_bar = pygame.image.load('./assets/ui/energy_overflow_bar.png').convert_alpha()
        self.energy_overflow_rect = self.energy_overflow_bar.get_rect(topright=(self.energy_rect.right, 144))
        self.stamina_bar = pygame.image.load('./assets/ui/stamina_bar.png').convert_alpha()
        self.stamina_rect = self.stamina_bar.get_rect(topleft=(16, 176))
        self.melee_overlay = pygame.image.load('./assets/ui/overlay_melee.png').convert_alpha()
        self.melee_overlay_rect = self.melee_overlay.get_rect(bottomleft=(16, 688))
        self.ranged_overlay = pygame.image.load('./assets/ui/overlay_ranged.png').convert_alpha()
        self.ranged_overlay_rect = self.ranged_overlay.get_rect(bottomleft=self.melee_overlay_rect.bottomright)
        self.magical_overlay = pygame.image.load('./assets/ui/overlay_magical.png').convert_alpha()
        self.magical_overlay_rect = self.magical_overlay.get_rect(bottomleft=self.ranged_overlay_rect.bottomright)

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
        health_bar_rect = pygame.Rect(health_bar_topleft, (health_width, health_bar_height))
        pygame.draw.rect(self.display_surface, '#dc4949', health_bar_rect)

    def display_health_remainder(self, health_remainder, max_health_remainder):
        """Display the health remainder bar and statistics.

        Arguments:
        health_remainder -- the current health remainder value
        max_health_remainder -- the maximum health remainder value
        """
        # Preparation
        health_remainder_bar_topleft = (self.health_remainder_rect.topleft[0]+4, self.health_remainder_rect.topleft[1]+4)
        health_remainder_bar_width = 112
        health_remainder_bar_height = 12
        # Drawing
        self.display_surface.blit(self.health_remainder_bar, self.health_remainder_rect)
        health_remainder_statistics_surface = self.font.render(f'{health_remainder}', False, 'white')
        health_remainder_statistics_rect = health_remainder_statistics_surface.get_rect(midleft=(self.health_remainder_rect.right+8, self.health_remainder_rect.centery))
        self.display_surface.blit(health_remainder_statistics_surface, health_remainder_statistics_rect)
        if health_remainder == 0:
            health_remainder_percentage = 1  # If the health remainder is 0, show the bar as full instead of empty
        else:
            health_remainder_percentage = health_remainder / max_health_remainder
        health_remainder_width = int(health_remainder_bar_width * health_remainder_percentage)
        health_remainder_bar_rect = pygame.Rect(health_remainder_bar_topleft, (health_remainder_width, health_remainder_bar_height))
        pygame.draw.rect(self.display_surface, '#dc4949', health_remainder_bar_rect)

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
        energy_bar_rect = pygame.Rect(energy_bar_topleft, (energy_width, energy_bar_height))
        pygame.draw.rect(self.display_surface, '#0098db', energy_bar_rect)

    def display_energy_overflow(self, energy_overflow, max_energy_overflow):
        """Display the energy overflow bar and statistics.

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
        energy_overflow_statistics_surface = self.font.render(f'{energy_overflow}', False, 'white')
        energy_overflow_statistics_rect = energy_overflow_statistics_surface.get_rect(midleft=(self.energy_overflow_rect.right+8, self.energy_overflow_rect.centery))
        self.display_surface.blit(energy_overflow_statistics_surface, energy_overflow_statistics_rect)
        energy_overflow_percentage = energy_overflow / max_energy_overflow
        energy_overflow_width = int(energy_overflow_bar_width * energy_overflow_percentage)
        energy_overflow_bar_rect = pygame.Rect(energy_overflow_bar_topleft, (energy_overflow_width, energy_overflow_bar_height))
        pygame.draw.rect(self.display_surface, '#0098db', energy_overflow_bar_rect)

    def display_stamina(self, stamina, max_stamina):
        """Display the stamina bar.

        Arguments:
        stamina -- the current stamina value
        max_stamina -- the maximum stamina value
        """
        # Preparation
        stamina_bar_topleft = (self.stamina_rect.topleft[0]+52, self.stamina_rect.topleft[1]+28)
        stamina_bar_width = 200
        stamina_bar_height = 12
        # Drawing
        self.display_surface.blit(self.stamina_bar, self.stamina_rect)
        stamina_percentage = stamina / max_stamina
        stamina_width = int(stamina_bar_width * stamina_percentage)
        stamina_bar_rect = pygame.Rect(stamina_bar_topleft, (stamina_width, stamina_bar_height))
        pygame.draw.rect(self.display_surface, '#aeda48', stamina_bar_rect)

    def display_melee_overlay(self, melee_weapon, melee_durability, max_melee_durability):
        """Display the melee weapon overlay.

        Arguments:
        melee_weapon -- the path to the melee weapon icon
        melee_durability -- the current melee weapon durability
        max_melee_durability -- the maximum melee weapon durability
        """
        melee_weapon_icon = pygame.image.load(melee_weapon).convert_alpha()
        melee_weapon_icon_rect = melee_weapon_icon.get_rect(center=self.melee_overlay_rect.center)
        self.display_surface.blit(self.melee_overlay, self.melee_overlay_rect)
        self.display_surface.blit(melee_weapon_icon, melee_weapon_icon_rect)
        melee_durability_percentage = melee_durability / max_melee_durability
        melee_durability_width = int(48 * melee_durability_percentage)
        melee_durability_rect = pygame.Rect((self.melee_overlay_rect.topleft[0]+5, self.melee_overlay_rect.topleft[1]+72), (melee_durability_width, 4))
        pygame.draw.rect(self.display_surface, '#14a02e', melee_durability_rect)

    def display_ranged_overlay(self, ranged_weapon, ranged_projectile_count):
        """Display the ranged weapon overlay.

        Arguments:
        ranged_weapon -- the path to the ranged weapon icon
        ranged_projectile_count -- the ranged projectile count
        """
        ranged_weapon_icon = pygame.image.load(ranged_weapon).convert_alpha()
        ranged_weapon_icon_rect = ranged_weapon_icon.get_rect(center=self.ranged_overlay_rect.center)
        self.display_surface.blit(self.ranged_overlay, self.ranged_overlay_rect)
        self.display_surface.blit(ranged_weapon_icon, ranged_weapon_icon_rect)
        ranged_projectile_count_font = pygame.font.Font('./font.ttf', 6)
        ranged_projectile_count_surface = ranged_projectile_count_font.render(str(ranged_projectile_count), False, 'white')
        ranged_projectile_count_rect = ranged_projectile_count_surface.get_rect(bottomleft=(self.ranged_overlay_rect.left+4, self.ranged_overlay_rect.bottom-4))
        self.display_surface.blit(ranged_projectile_count_surface, ranged_projectile_count_rect)

    def display_magical_overlay(self, magical_weapon, magical_power, max_magical_power):
        """Display the magical weapon overlay.

        Arguments:
        magical_weapon -- the path to the magical weapon icon
        magical_power -- the current magical weapon power
        max_magical_power -- the maximum magical weapon power
        """
        magical_weapon_icon = pygame.image.load(magical_weapon).convert_alpha()
        magical_weapon_icon_rect = magical_weapon_icon.get_rect(center=self.magical_overlay_rect.center)
        self.display_surface.blit(self.magical_overlay, self.magical_overlay_rect)
        self.display_surface.blit(magical_weapon_icon, magical_weapon_icon_rect)
        magical_power_percentage = magical_power / max_magical_power
        magical_power_width = int(48 * magical_power_percentage)
        magical_power_rect = pygame.Rect((self.magical_overlay_rect.topleft[0]+5, self.magical_overlay_rect.topleft[1]+72), (magical_power_width, 4))
        pygame.draw.rect(self.display_surface, '#ffe320', magical_power_rect)
