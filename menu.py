import pygame
import sys
import random
import configparser
import os
import shelve
from text import render
from settings import *  # lgtm [py/polluting-import]
from box import TextBox, SelectionBoxYN
from versions import get_version

"""This file defines the menus."""

class Menu:
    """The basic menu class."""
    def __init__(self, background, cursor, layout, display_surface, parent):
        """Setup the menu elements.

        Arguments:
        background -- the menu background
        cursor -- the cursor image
        layout -- the layout type
        display_surface -- the screen
        parent -- the parent class
        """
        # Setup
        self.display_surface = display_surface
        self.parent = parent
        self.controllers = self.parent.controller.controllers
        self.gamepad = self.parent.gamepad
        self.background = pygame.image.load(background).convert_alpha()
        self.cursor = pygame.image.load(cursor).convert_alpha()
        self.font_file = './font.ttf'
        self.font = pygame.font.Font(self.font_file, 40)
        self.layout = layout
        self.cursor_pos = 0
        self.now = 0  # This is a dummy value
        self.gen_time = pygame.time.get_ticks()

        # SFX
        self.menu_sfx = pygame.mixer.Sound('./assets/audio/sfx/menu_select.ogg')

        # Text attributes
        self.x = 0
        self.y = 0
        self.step = 0

        # Input initialization
        self.keydown_up = False
        self.keydown_down = False
        self.keydown_space = False
        self.buttondown_lb = False
        self.buttondown_rb = False
        self.buttondown_a = False

    def display_cursor(self):
        """Display the cursor."""
        if self.layout == 'v':
            x = self.x - self.cursor.get_width()
            y = self.y + self.cursor_pos*self.step
        elif self.layout == 'h':
            x = self.x + self.cursor_pos*self.step - self.cursor.get_width()
            y = self.y
        self.display_surface.blit(self.cursor, (x, y))

    def display_text(self, tags):
        """Display the button tag texts.

        Arguments:
        tags -- the tag texts
        """
        x = self.x
        y = self.y
        for text in tags:
            text_surface = self.font.render(text, False, 'white')
            self.display_surface.blit(text_surface, (x, y))
            if self.layout == 'v':
                y += self.step
            elif self.layout == 'h':
                x += self.step

    def dummy(self):
        """A dummy function."""
        pass

    def get_input(self, funcs):
        """Get the input from the devices and do the correct actions.

        Arguments:
        funcs -- the functions to run
        """
        gamepad = controllers[self.gamepad]
        controller_lb = False
        controller_rb = False
        controller_a = False
        for controller in self.controllers.values():
            if controller.get_button(gamepad['buttons']['LB']):
                controller_lb = True
            elif controller.get_button(gamepad['buttons']['RB']):
                controller_rb = True
            elif controller.get_button(gamepad['buttons']['A']):
                controller_a = True
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_LEFT] or controller_lb) and not (self.keydown_up or self.buttondown_lb) and self.cursor_pos > 0:
            self.cursor_pos -= 1
            self.menu_sfx.play()
            self.keydown_up = True
            self.buttondown_lb = True
        elif (keys[pygame.K_DOWN] or keys[pygame.K_RIGHT] or controller_rb) and not (self.keydown_down or self.buttondown_rb) and self.cursor_pos < len(funcs) - 1:
            self.cursor_pos += 1
            self.menu_sfx.play()
            self.keydown_down = True
            self.buttondown_rb = True
        elif (keys[pygame.K_SPACE] or controller_a) and not (self.keydown_space or self.buttondown_a):
            self.menu_sfx.play()
            self.keydown_space = True
            self.buttondown_a = True
            funcs[self.cursor_pos]()

        if not keys[pygame.K_UP] and not keys[pygame.K_LEFT]: self.keydown_up = False
        if not keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT]: self.keydown_down = False
        if not keys[pygame.K_SPACE]: self.keydown_space = False
        if not controller_lb: self.buttondown_lb = False
        if not controller_rb: self.buttondown_rb = False
        if not controller_a: self.buttondown_a = False

    def run(self, tags, *funcs):
        """Update and draw everything (must be called every frame).

        Arguments:
        tags -- the button tag texts
        funcs -- the functions to run
        """
        self.now = pygame.time.get_ticks()
        self.display_surface.blit(self.background, (0, 0))
        if self.now - self.gen_time >= 250:
            self.get_input(funcs)
        self.display_cursor()
        self.display_text(tags)

class MainMenu(Menu):
    """The main menu class."""
    def __init__(self, display_surface, parent):
        """Initialize the base class and setup the elements.

        Arguments:
        display_surface -- the screen
        parent -- the parent class
        """
        self.display_surface = display_surface
        self.parent = parent
        self.background = './assets/menu/title_bg.png'
        self.cursor = './assets/menu/cursor_gray.png'
        self.layout = 'v'
        super().__init__(self.background, self.cursor, self.layout, self.display_surface, self.parent)
        self.x = 128
        self.y = 288
        self.step = 80
        self.tags = ['New Game', 'Continue', 'Settings', 'Controls', 'Quit']
        self.create_settings = self.parent.create_settings
        self.create_controls = self.parent.create_controls
        self.title = pygame.image.load('./assets/menu/title.png').convert_alpha()
        self.copyright_info = "Copyright (C) 2022  BarbeMCR"
        self.status = None
        self.splash_font = pygame.font.Font(self.font_file, 24)
        self.splashes = './splashes.txt'
        with open(self.splashes) as file:
            splashes = file.readlines()
            splashes = [line.rstrip() for line in splashes]
            self.splash = random.choice(splashes)

    def display_text(self, tags):
        """Display the button tag texts.

        Arguments:
        tags -- the tag texts
        """
        x = self.x
        y = self.y
        for text in tags:
            text_surface = self.font.render(text, False, 'gray50')
            self.display_surface.blit(text_surface, (x, y))
            if self.layout == 'v':
                y += self.step
            elif self.layout == 'h':
                x += self.step

    def display_splash(self):
        """Display a splash text."""
        render(self.splash, self.splash_font, self.display_surface, (640, 288, 640, 416), 'black')

    def display_copyright_info(self):
        """Display the copyright information."""
        copyright_surface = self.splash_font.render(self.copyright_info, False, 'white')
        copyright_rect = copyright_surface.get_rect(bottomright=self.display_surface.get_rect().bottomright)
        self.display_surface.blit(copyright_surface, copyright_rect)

    def create_save_textbox(self):
        """Create a save textbox."""
        self.save_textbox = TextBox('./assets/ui/save_input_box.png', self.display_surface, self.parent)
        self.status = 'save_textbox'

    def create_load_textbox(self):
        """Create a load textbox."""
        self.load_textbox = TextBox('./assets/ui/load_input_box.png', self.display_surface, self.parent)
        self.status = 'load_textbox'

    def create_infobox(self):
        """Create an infobox for the savefile information."""
        if os.path.isfile(self.parent.savefile_path + '.dat'):
            with shelve.open(self.parent.savefile_path, 'r') as savefile:
                raw_creation_version = savefile['creation_version']
                creation_time = savefile['creation_time']
                raw_version = savefile['version']
                access_time = savefile['access_time']
            creation_version = get_version(raw_creation_version)
            version = get_version(raw_version)
            text = f"Are you sure to load savefile '{self.parent.savefile_path[7:]}'?\nCreated on {creation_time} in version {creation_version}\nLast accessed on {access_time} in version {version}\nKeep in mind that loading from a savefile could trigger\nsome dangerous Arbitrary Code Execution (ACE).\nOnly load a savefile if it comes from a trusted source (such as you).\nThe savefile will be upgraded to the latest version if necessary.".split('\n')
            self.infobox = SelectionBoxYN(text, self.display_surface, self.parent)
            self.infobox.font = pygame.font.Font('./font.ttf', 12)
            self.status = 'infobox'
        else:
            self.status = None

    def create_game(self):
        """Create a new game."""
        self.parent.save(True)
        self.parent.create_world(self.parent.start_level, self.parent.end_level, self.parent.current_subpart, self.parent.current_part)

    def quit(self):
        """A function for quitting the game."""
        pygame.quit()
        sys.exit()

    def run(self):
        """Update and draw everything."""
        if self.status == 'save_textbox':
            self.display_surface.blit(self.background, (0, 0))
            self.save_textbox.run(self.create_game)
        elif self.status == 'load_textbox':
            self.display_surface.blit(self.background, (0, 0))
            self.load_textbox.run(self.create_infobox)
        elif self.status == 'infobox':
            self.infobox.run(self.parent.load, lambda: setattr(self, 'status', None), small=True)
        else:
            super().run(self.tags, self.create_save_textbox, self.create_load_textbox, self.create_settings, self.create_controls, self.quit)
            self.display_splash()
        self.display_surface.blit(self.title, (0, 0))
        self.display_copyright_info()

class Controls(Menu):
    """The controls info class."""
    def __init__(self, display_surface, parent):
        """Initialize the base class and setup the elements.

        Arguments:
        display_surface -- the screen
        parent -- the parent class
        """
        self.display_surface = display_surface
        self.parent = parent
        self.background = './assets/menu/menu_bg.png'
        self.cursor = './assets/menu/cursor.png'
        self.layout = 'v'
        super().__init__(self.background, self.cursor, self.layout, self.display_surface, self.parent)
        self.tags = ['Back']
        self.x = int((screen_width - self.font.size(self.tags[0])[0]) / 2)
        self.y = screen_height - self.font.size(self.tags[0])[1] - 64
        self.step = 64
        self.create_main_menu = self.parent.create_main_menu
        self.controls_font = pygame.font.Font(self.font_file, 18)
        self.controls = [
            "Movement: 'WASD' / D-Pad / D-Pad / D-Pad",
            "Jump: 'Space' / A / Cross / A",
            "Attack: 'JKL' / B-X-Y / Circle-Square-Triangle / B-X-Y",
            "Pause: 'Esc' / Menu / Options / +",
            "Take screenshot: 'F2' / Share / Touchpad Click / Capture"
        ]

    def display_controls(self):
        """Display the control information."""
        y = 64
        for control in self.controls:
            control_surface = self.controls_font.render(control, False, 'white')
            self.display_surface.blit(control_surface, (64, y))
            y += 32

    def run(self):
        """Update and draw everything."""
        super().run(self.tags, self.create_main_menu)
        self.display_controls()

class PauseMenu(Menu):
    """The pause menu class."""
    def __init__(self, display_surface, parent):
        """Initialize the base class and setup the elements.

        Arguments:
        display_surface -- the screen
        parent -- the parent class
        """
        self.display_surface = display_surface
        self.parent = parent
        self.background = './assets/menu/menu_bg.png'
        self.cursor = './assets/menu/cursor.png'
        self.layout = 'v'
        super().__init__(self.background, self.cursor, self.layout, self.display_surface, self.parent)
        self.x = 384
        self.y = 288
        self.step = 80
        self.tags = ['Resume Game', 'Save Game', 'Save and Quit to Title']
        self.resume_game = self.parent.resume_level
        self.save_game = self.parent.parent.save
        self.pause_caption_font = pygame.font.Font(self.font_file, 64)
        self.pause_caption = "Game Paused"

    def exit_game(self):
        """Save and quit the game."""
        self.parent.parent.save()
        self.parent.parent.create_main_menu()

    def display_pause_caption(self):
        """Display the pause caption."""
        pause_caption_surface = self.pause_caption_font.render(self.pause_caption, False, 'white')
        x = int((screen_width - self.pause_caption_font.size(self.pause_caption)[0]) / 2)
        self.display_surface.blit(pause_caption_surface, (x, 64))

    def run(self):
        """Update and draw everything."""
        super().run(self.tags, self.resume_game, self.save_game, self.exit_game)
        self.display_pause_caption()

class Settings(Menu):
    """The settings menu class."""
    def __init__(self, display_surface, parent):
        """Initialize the base class and setup the elements.

        Arguments:
        display_surface -- the screen
        parent -- the parent class
        """
        self.display_surface = display_surface
        self.parent = parent
        self.background = './assets/menu/menu_bg.png'
        self.cursor = './assets/menu/cursor.png'
        self.layout = 'v'
        super().__init__(self.background, self.cursor, self.layout, self.display_surface, self.parent)
        self.tags = ['Controller', 'Autodownload', 'Delete Game', 'Reset settings', 'Back to title']
        self.x = 128
        self.y = 64
        self.step = 96
        self.create_main_menu = self.parent.create_main_menu
        self.settings = configparser.ConfigParser()
        self.settings.read('./data/settings.ini')
        self.status = None

    def select_option(self, child):
        """A function used to substitute 'get_input' and simplify the input management.

        Arguments:
        child -- the child class
        """
        gamepad = controllers[self.gamepad]
        controller_lb = False
        controller_rb = False
        controller_a = False
        for controller in self.controllers.values():
            if controller.get_button(gamepad['buttons']['LB']):
                controller_lb = True
            elif controller.get_button(gamepad['buttons']['RB']):
                controller_rb = True
            elif controller.get_button(gamepad['buttons']['A']):
                controller_a = True
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_LEFT] or controller_lb) and not (self.keydown_up or self.buttondown_lb) and child.selection > 0:
            child.selection -= 1
            self.cursor_pos -= 1
            self.menu_sfx.play()
            self.keydown_up = True
            self.buttondown_lb = True
        elif (keys[pygame.K_DOWN] or keys[pygame.K_RIGHT] or controller_rb) and not (self.keydown_down or self.buttondown_rb) and child.selection < len(child.strings) - 1:
            child.selection += 1
            self.cursor_pos += 1
            self.menu_sfx.play()
            self.keydown_down = True
            self.buttondown_rb = True
        elif (keys[pygame.K_SPACE] or controller_a) and not (self.keydown_space or self.buttondown_a):
            self.menu_sfx.play()
            self.keydown_space = True
            self.buttondown_a = True
            self.settings[child.section] = {}
            self.settings[child.section][child.key] = child.strings[child.selection]
            with open('./data/settings.ini', 'w') as file:
                self.settings.write(file)
            child.selection = 0
            self.cursor_pos = 0
            self.status = None

        if not keys[pygame.K_UP] and not keys[pygame.K_LEFT]: self.keydown_up = False
        if not keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT]: self.keydown_down = False
        if not keys[pygame.K_SPACE]: self.keydown_space = False
        if not controller_lb: self.buttondown_lb = False
        if not controller_rb: self.buttondown_rb = False
        if not controller_a: self.buttondown_a = False

    def place_cursor(self, child):
        """Place the cursor to signal the current option.

        Arguments:
        child -- the child class
        """
        self.settings.read('./data/settings.ini')
        for index, string in enumerate(child.strings):
            if string == self.settings[child.section][child.key]:
                child.selection = index
                self.cursor_pos = index

    def reset_settings(self):
        """Reset the settings to their default values."""
        self.settings.read('./data/settings.ini')
        for section in self.settings.sections():
            for key in self.settings.options(section):
                self.settings[section][key] = self.settings.defaults()[key]
        with open('./data/settings.ini', 'w') as file:
            self.settings.write(file)

    def delete_game(self):
        """Delete a savefile."""
        if os.path.isfile(self.parent.savefile_path + '.dat'):
            os.remove(self.parent.savefile_path + '.dat')
            # self.parent.savefile[7:] is done to avoid displaying the './data/' prefix
            confirmation = self.font.render(f"Savefile '{self.parent.savefile_path[7:]}' was deleted.", False, 'white')
            confirmation_rect = confirmation.get_rect(center=self.display_surface.get_rect().center)
            self.display_surface.blit(confirmation, confirmation_rect)
            pygame.display.flip()
            pygame.time.wait(2000)
        if os.path.isfile(self.parent.savefile_path + '.dir'):
            os.remove(self.parent.savefile_path + '.dir')
        if os.path.isfile(self.parent.savefile_path + '.bak'):
            os.remove(self.parent.savefile_path + '.bak')
        if os.path.isfile(self.parent.savefile_path + '.checksum'):
            os.remove(self.parent.savefile_path + '.checksum')
        self.parent.savefile_path = ''
        self.status = None

    def create_delete_textbox(self):
        """Create a delete textbox."""
        self.delete_textbox = TextBox('./assets/ui/delete_input_box.png', self.display_surface, self.parent)
        self.status = 'delete_textbox'

    def create_controller_settings(self):
        """Create the controller settings submenu."""
        self.controller = ControllerSettings(self)
        self.status = 'controller'
        self.place_cursor(self.controller)

    def create_autodownload_settings(self):
        """Create the autodownload settings submenu."""
        self.autodownload = AutodownloadSettings(self)
        self.status = 'autodownload'
        self.place_cursor(self.autodownload)

    def run(self):
        """Update and draw everything."""
        if self.status == 'delete_textbox':
            self.display_surface.blit(self.background, (0, 0))
            self.delete_textbox.run(self.delete_game)
        elif self.status == 'controller':
            self.controller.run()
            super().run(self.controller.options, self.dummy)
        elif self.status == 'autodownload':
            self.autodownload.run()
            super().run(self.autodownload.options, self.dummy)
        else:
            super().run(self.tags, self.create_controller_settings, self.create_autodownload_settings, self.create_delete_textbox, self.reset_settings, self.create_main_menu)

class ControllerSettings(Settings):  #lgtm [py/missing-call-to-init]
    """The controller settings submenu."""
    def __init__(self, parent):
        """Initialize the base settings class.

        Arguments:
        parent -- the parent class
        """
        self.parent = parent
        self.options = ['Xbox One / X|S / 360', 'DualShock 4', 'Switch Pro']
        self.strings = ['xbox_one', 'ps4', 'switch_pro']
        self.section = 'controller'
        self.key = 'gamepad'
        self.selection = 0

    def run(self):
        """Update and draw everything."""
        self.parent.select_option(self)

class AutodownloadSettings(Settings):  #lgtm [py/missing-call-to-init]
    """The autodownload settings submenu."""
    def __init__(self, parent):
        """Initialize the base settings class.

        Arguments:
        parent -- the parent class
        """
        self.parent = parent
        self.options = ['Disabled', 'Enabled']
        self.strings = ['false', 'true']
        self.section = 'autodownload'
        self.key = 'autodownload'
        self.selection = 0

    def run(self):
        """Update and draw everything."""
        self.parent.select_option(self)
