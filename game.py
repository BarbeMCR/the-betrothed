import pygame
import configparser
import shelve
import os
import random
import hashlib
import datetime
from world import World
from level import Level
from menu import MainMenu, Settings, Controls
from controller import Controller
from ui import UI
from misc import take_screenshot
from melee import *

"""This file contains the base game structure needed to switch between the world and the levels, as well as various global methods and attributes."""

class Game:
    """The main game class."""
    def __init__(self, display_surface, build):
        """Set the screen, the event puller, the world and the status.
        Also set all the global variables.

        Arguments:
        display_surface -- the screen
        build -- the build string
        """
        # Settings
        self.settings = configparser.ConfigParser()
        self.settings.read('./data/settings.ini')
        self.gamepad = self.settings['controller']['gamepad']
        # Savefile
        self.savefile_path = ''
        self.savefile = None
        self.loaded_from_savefile = False
        # Setup
        self.version = build
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
        self.character = 'renzo'
        self.health = {'renzo': 20}
        self.max_health = {'renzo': 20}
        self.energy = {'renzo': 0}
        self.max_energy = {'renzo': 100}
        self.energy_overflow = {'renzo': 0}
        self.max_energy_overflow = {'renzo': 25}

        # Inventory
        self.selection = {
            'melee': IronKnife()
        }

    def reset(self):
        """Reset the game."""
        self.first_level = 0
        self.start_level = 0
        self.end_level = 0
        self.current_subpart = 0
        self.current_part = 0
        self.health = {'renzo': 20}
        self.energy = {'renzo': 0}
        self.energy_overflow = {'renzo': 0}
        self.selection = {
            'melee': IronKnife()
        }

    def save(self, first=False):
        """Save the game to file."""
        if self.savefile_path != '':
            self.savefile = shelve.open(self.savefile_path, writeback=True)
            if first:
                self.savefile['creation_version'] = self.version
                self.savefile['creation_time'] = datetime.datetime.now().strftime('%B %d %Y, %H:%M:%S')
                self.savefile['access_time'] = self.savefile['creation_time']
            self.savefile['rng'] = random.getstate()
            self.savefile['version'] = self.version
            self.savefile['first_level'] = self.first_level
            self.savefile['start_level'] = self.start_level
            self.savefile['end_level'] = self.end_level
            self.savefile['current_subpart'] = self.current_subpart
            self.savefile['current_part'] = self.current_part
            self.savefile['health'] = self.health
            self.savefile['energy'] = self.energy
            self.savefile['energy_overflow'] = self.energy_overflow
            self.savefile['selection'] = self.selection
            self.savefile.close()
            hash = hashlib.sha256()
            with open(self.savefile_path + '.dat', 'rb') as savefile:
                hash.update(savefile.read())
                with open(self.savefile_path + '.checksum', 'w') as checksum:
                    checksum.write(hash.hexdigest())

    def load(self):
        """Load the game from file."""
        if os.path.isfile(self.savefile_path + '.dat'):
            hash = hashlib.sha256()
            with open(self.savefile_path + '.dat', 'rb') as savefile:
                hash.update(savefile.read())
            checksum = open(self.savefile_path + '.checksum', 'r')
            if checksum.read() == hash.hexdigest():
                self.savefile = shelve.open(self.savefile_path, writeback=True)
                random.setstate(self.savefile['rng'])
                self.savefile['version'] = self.version
                self.savefile['access_time'] = datetime.datetime.now().strftime('%B %d %Y, %H:%M:%S')
                self.first_level = self.savefile['first_level']
                self.start_level = self.savefile['start_level']
                self.end_level = self.savefile['end_level']
                self.current_subpart = self.savefile['current_subpart']
                self.current_part = self.savefile['current_part']
                self.health = self.savefile['health']
                self.energy = self.savefile['energy']
                self.energy_overflow = self.savefile['energy_overflow']
                self.selection = self.savefile['selection']
                self.savefile.close()
                with open(self.savefile_path + '.dat', 'rb') as savefile:
                    hash.update(savefile.read())
                    with open(self.savefile_path + '.checksum', 'w') as checksum:
                        checksum.write(hash.hexdigest())
                self.loaded_from_savefile = True
                self.create_world(self.first_level, self.start_level, self.end_level, self.current_subpart, self.current_part)
            else:
                message = "A checksum error occured in a savefile and the game was crashed on purpose to avoid potential damage."
                raise Exception(message)

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
        """Build the main menu and update the status.

        Arguments:
        save -- specify whether to save the game before building the main menu
        """
        self.reset()
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
        if self.health[self.character] <= 0:
            self.apply_death()
            pygame.mixer.stop()
            pygame.mixer.music.stop()
            pygame.mixer.music.load('./assets/audio/game_over.ogg')
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play()

    def apply_death(self):
        """Apply the death penalties."""
        self.first_level = 0
        self.start_level = 0
        self.end_level = 0
        self.current_part = 0
        self.world = World(self.first_level, self.start_level, self.end_level, self.current_subpart, self.current_part, self.display_surface, self)
        self.status = 'world'
        self.health[self.character] = self.max_health[self.character]
        self.energy[self.character] = int(self.energy[self.character] / 2)
        self.energy_overflow[self.character] = 0

    def update_health(self, amount, damage):
        """Change the player health.

        Arguments:
        amount -- the amount of health to add or subtract
        damage -- if this flag is set to True the amount will be subtracted from the health, otherwise it will be added to the health.
        """
        if damage:
            self.health[self.character] -= amount
            if self.health[self.character] < 0:
                self.health[self.character] = 0
        else:
            self.health[self.character] += amount
            if self.health[self.character] > self.max_health[self.character]:
                self.health[self.character] = self.max_health[self.character]

    def update_energy(self, amount, add):
        """Change the player energy.

        Arguments:
        amount -- the amount of energy to add or subtract
        add -- if this flag is set to True the amount will be added to the energy, otherwise it will be subracted from the energy.
        """
        if add:
            self.energy[self.character] += amount
            if self.energy[self.character] > self.max_energy[self.character]:
                self.energy_overflow[self.character] += self.energy[self.character] - self.max_energy[self.character]
                self.energy[self.character] = self.max_energy[self.character]
                if self.energy_overflow[self.character] >= self.max_energy_overflow[self.character]:
                    self.update_health(self.max_health[self.character], False)
                    self.energy_overflow[self.character] -= self.max_energy_overflow[self.character]
        else:
            self.energy[self.character] -= amount
            if self.energy[self.character] < self.max_energy[self.character] - int(self.max_energy[self.character] / 10):
                self.reset_energy_overflow()
            if self.energy[self.character] < 0:
                self.energy[self.character] = 0

    def reset_energy_overflow(self):
        """Reset the energy overflow bar."""
        self.energy_overflow[self.character] = 0

    def run(self, delta):
        """Pull the events and run the correct methods depending on the status.

        Arguments:
        delta -- the time delta
        """
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
            self.level.run(delta)
            if self.level.status == 'level':
                self.ui.display_health(self.health[self.character], self.max_health[self.character])
                self.ui.display_energy(self.energy[self.character], self.max_energy[self.character])
                self.ui.display_energy_overflow(self.energy_overflow[self.character], self.max_energy_overflow[self.character])
                self.ui.display_melee_overlay(self.selection['melee'].icon_path)
                self.check_death()
                if self.level.player.sprite.screenshot_taken:
                    take_screenshot(self.display_surface)
                    self.level.player.sprite.screenshot_taken = False
                if not self.level.level_completed:
                    self.level.fade_in(2)
                else:
                    self.level.fade_out(4)
