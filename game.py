import pygame
from world import World
from level import Level
from controller import Controller
from ui import UI

"""This file contains the base game structure needed to switch between the world and the levels, as well as the controller interface and the event queue."""

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
        self.current_part = 0
        self.world = World(self.first_level, self.start_level, self.end_level, self.current_part, self.display_surface, self.create_level, self.controller)
        self.status = 'world'

        # Global variables
        self.health = 20
        self.max_health = 20

    def create_level(self, current_level, current_part):
        """Build the selected level and update the status.

        Arguments:
        current_level -- the currently selected level
        current_part -- the part the level is in
        """
        self.level = Level(current_level, self.current_part, self.display_surface, self.create_world, self.first_level, self.controller, self.update_health)
        self.status = 'level'

    def create_world(self, first_level, start_level, end_level, current_part):
        """Build the world map and update the status.

        Arguments:
        first_level -- the lowest level the player can select
        start_level -- the level to place the cursor on
        end_level -- the highest level the player can select
        current_part -- the part to load
        """
        if end_level > self.end_level:
            self.end_level = end_level
        self.first_level = first_level
        self.current_part = current_part
        self.world = World(self.first_level, start_level, self.end_level, self.current_part, self.display_surface, self.create_level, self.controller)
        self.status = 'world'

    def check_death(self):
        """Check if the player is dead."""
        if self.health <= 0:
            self.first_level = 0
            self.start_level = 0
            self.end_level = 0
            self.current_part = 0
            self.world = World(self.first_level, self.start_level, self.end_level, self.current_part, self.display_surface, self.create_level, self.controller)
            self.status = 'world'
            self.health = 20

    def update_health(self, amount, damage):
        """Change the player health.

        Arguments:
        amount -- the amount of health to add or subtract
        damage -- if this flag is set to True, the amount will be subtracted from the health, otherwise it will be added to the health.
        """
        if damage:
            self.health -= amount
        else:
            self.health += amount
            if self.health > self.max_health:
                self.health = self.max_health

    def run(self):
        """Pull the events and run the correct methods depending on the status."""
        self.events = pygame.event.get()
        if self.status == 'world':
            self.world.run()
        elif self.status == 'level':
            self.level.run()
            self.ui.display_health(self.health, self.max_health)
            self.check_death()
