from world import World
from level import Level

"""This file contains the base game structure needed to switch between the world and the levels."""

class Game:
    """The main game class."""
    def __init__(self, display_surface):
        """Set the screen, the world and the status.

        Arguments:
        display_surface -- the screen
        """
        self.display_surface = display_surface
        self.start_level = 0
        self.end_level = 0
        self.world = World(self.start_level, self.end_level, self.display_surface, self.create_level)
        self.status = 'world'

    def create_level(self, current_level):
        """Build the selected level and update the status.

        Arguments:
        current_level -- the currently selected level
        """
        self.level = Level(current_level, self.display_surface, self.create_world)
        self.status = 'level'

    def create_world(self, start_level, end_level):
        """Build the world map and update the status.

        Arguments:
        start_level -- the level to place the cursor on
        end_level -- the highest level the player can select
        """
        if end_level > self.end_level:
            self.end_level = end_level
        self.world = World(start_level, self.end_level, self.display_surface, self.create_level)
        self.status = 'world'

    def run(self):
        """Run the correct class method depending on the status."""
        if self.status == 'world':
            self.world.run()
        elif self.status == 'level':
            self.level.run()
