import pygame
from world import World
from level import Level
from menu import MainMenu, Settings, Controls
from controller import Controller
from ui import UI
from melee import *

"""This file contains the base game structure needed to switch between the world and the levels, as well as various global methods and attributes."""

class Game:
    """The main game class."""
    def __init__(self, display_surface):
        """Set the screen, the event puller, the world and the status.
        Also set all the global variables.

        Arguments:
        display_surface -- the screen
        """
        self.display_surface = display_surface
        self.events = pygame.event.get()
        self.controller = Controller()
        self.ui = UI(self.display_surface)
        self.first_level = 0
        self.start_level = 0
        self.end_level = 0
        self.current_subpart = 0
        self.current_part = 0
        self.main_menu = MainMenu(self.display_surface, self)
        self.status = 'main_menu'

        # Global variables
        self.health = 20
        self.max_health = 20
        self.energy = 0
        self.max_energy = 100
        self.energy_overflow = 0
        self.max_energy_overflow = 25

        # Inventory
        self.selection = {
            'melee': IronKnife()
        }

    def create_level(self, current_level, current_subpart, current_part):
        """Build the selected level and update the status.

        Arguments:
        current_level -- the currently selected level
        current_subpart -- the subpart the level is in
        current_part -- the part the level is in
        """
        self.level = Level(self.display_surface, current_level, current_subpart, current_part, self)
        self.status = 'level'

    def create_world(self, first_level, start_level, end_level, current_subpart, current_part):
        """Build the world map and update the status.

        Arguments:
        first_level -- the lowest level the player can select
        start_level -- the level to place the cursor on
        end_level -- the highest level the player can select
        current_subpart -- the subpart to load
        current_part -- the part to load
        """
        if end_level > self.end_level:
            self.end_level = end_level
        self.first_level = first_level
        self.current_subpart = current_subpart
        self.current_part = current_part
        self.world = World(self.first_level, start_level, self.end_level, self.current_subpart, self.current_part, self.display_surface, self)
        self.status = 'world'

    def create_main_menu(self):
        """Build the main menu and update the status."""
        self.main_menu = MainMenu(self.display_surface, self)
        self.status = 'main_menu'

    def create_settings(self):
        """Build the settings menu and update the status."""
        self.settings = Settings(self.display_surface, self)
        self.status = 'settings'

    def create_controls(self):
        """Build the controls screen and update the status."""
        self.controls = Controls(self.display_surface, self)
        self.status = 'controls'

    def check_death(self):
        """Check if the player is dead."""
        if self.health <= 0:
            self.first_level = 0
            self.start_level = 0
            self.end_level = 0
            self.current_part = 0
            self.world = World(self.first_level, self.start_level, self.end_level, self.current_subpart, self.current_part, self.display_surface, self)
            self.status = 'world'
            self.health = 20
            self.energy = int(self.energy / 2)
            self.energy_overflow = 0
            pygame.mixer.stop()
            pygame.mixer.music.stop()
            pygame.mixer.music.load('./assets/audio/game_over.ogg')
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play()

    def update_health(self, amount, damage):
        """Change the player health.

        Arguments:
        amount -- the amount of health to add or subtract
        damage -- if this flag is set to True the amount will be subtracted from the health, otherwise it will be added to the health.
        """
        if damage:
            self.health -= amount
            if self.health < 0:
                self.health = 0
        else:
            self.health += amount
            if self.health > self.max_health:
                self.health = self.max_health

    def update_energy(self, amount, add):
        """Change the player energy.

        Arguments:
        amount -- the amount of energy to add or subtract
        add -- if this flag is set to True the amount will be added to the energy, otherwise it will be subracted from the energy.
        """
        if add:
            self.energy += amount
            if self.energy > self.max_energy:
                self.energy_overflow += self.energy - self.max_energy
                self.energy = self.max_energy
                if self.energy_overflow >= self.max_energy_overflow:
                    self.update_health(self.max_health, False)
                    self.energy_overflow -= self.max_energy_overflow
        else:
            self.energy -= amount
            if self.energy < self.max_energy - int(self.max_energy / 10):
                self.reset_energy_overflow()
            if self.energy < 0:
                self.energy = 0

    def reset_energy_overflow(self):
        """Reset the energy overflow bar."""
        self.energy_overflow = 0

    def run(self):
        """Pull the events and run the correct methods depending on the status."""
        self.events = pygame.event.get()
        if self.status == 'main_menu':
            self.main_menu.run()
        elif self.status == 'settings':
            self.settings.run()
        elif self.status == 'controls':
            self.controls.run()
        elif self.status == 'world':
            self.world.run()
        elif self.status == 'level':
            self.level.run()
            if self.level.status == 'level':
                self.ui.display_health(self.health, self.max_health)
                self.ui.display_energy(self.energy, self.max_energy)
                self.ui.display_energy_overflow(self.energy_overflow, self.max_energy_overflow)
                self.ui.display_melee_overlay(self.selection['melee'].icon_path)
                self.check_death()
                if not self.level.level_completed:
                    self.level.fade_in(2)
                else:
                    self.level.fade_out(4)
