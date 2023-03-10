import pygame
from text import render
from settings import controllers

"""This file defines all user interaction boxes."""

class TextBox:
    """The text input box."""
    def __init__(self, outline, display_surface, parent):
        """Setup the box elements.

        Arguments:
        outline -- the box image
        display_surface -- the screen
        parent -- the parent class
        """
        # Setup
        self.display_surface = display_surface
        self.parent = parent
        self.controllers = self.parent.controller.controllers
        self.gamepad = self.parent.gamepad
        self.outline = pygame.image.load(outline).convert_alpha()
        self.outline_rect = self.outline.get_rect(center=self.display_surface.get_rect().center)
        self.input_box_topleft = self.outline_rect.topleft + pygame.Vector2(27, 67)
        self.font = pygame.font.Font('./font.ttf', 48)
        self.now = 0  # This is a dummy value
        self.gen_time = pygame.time.get_ticks()
        self.text = ''

        # SFX
        self.menu_sfx = pygame.mixer.Sound('./assets/audio/sfx/menu_select.ogg')

    def get_input(self, func):
        """Get the input from the devices.

        Arguments:
        func -- the function to run after finishing input
        """
        pygame.key.set_repeat(500, 50)
        for event in self.parent.events:
            # Readability hack below
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or\
            (event.type == pygame.JOYBUTTONDOWN and event.button == controllers[self.parent.gamepad]['buttons']['A']):
                self.parent.main_menu.status = None
                if self.text != '':
                    self.parent.savefile_path = './data/' + self.text
                self.menu_sfx.play()
                pygame.key.set_repeat()
                func()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if self.font.size(self.text)[0] <= 700:
                        self.text += event.unicode
                        if not self.text.isalnum():
                            self.text = self.text[:-1]

    def display_text(self):
        """Display the input text."""
        text_surface = self.font.render(self.text, False, 'white')
        self.display_surface.blit(text_surface, self.input_box_topleft)

    def run(self, func):
        """Update and draw everything.

        Arguments:
        func -- the function to run after finishing input
        """
        self.now = pygame.time.get_ticks()
        if self.now - self.gen_time >= 250:
            self.get_input(func)
        self.display_surface.blit(self.outline, self.outline_rect)
        self.display_text()

class SelectionBox:
    """The base selection box."""
    def __init__(self, outline, display_surface, parent):
        """Setup the box elements.

        Arguments:
        outline -- the box image
        display_surface -- the screen
        parent -- the parent class
        """
        # Setup
        self.display_surface = display_surface
        self.parent = parent
        self.controllers = self.parent.controller.controllers
        self.gamepad = self.parent.gamepad
        self.outline = pygame.image.load(outline).convert_alpha()
        self.outline_rect = self.outline.get_rect(midbottom=(self.display_surface.get_rect().centerx, self.display_surface.get_rect().bottom-54))
        self.textbox_topleft = self.outline_rect.midleft + pygame.Vector2(16, 16)
        self.textbox_rect = pygame.Rect(self.textbox_topleft, self.outline_rect.size - pygame.Vector2(32, 32))
        self.font = pygame.font.Font('./font.ttf', 24)
        self.selection_font = pygame.font.Font('./font.ttf', 40)
        self.cursor = pygame.image.load('./assets/menu/cursor.png').convert_alpha()
        self.cursor_pos = 0
        self.now = 0  # This is a dummy value
        self.gen_time = pygame.time.get_ticks()
        self.x = 496
        self.y = 32

        # SFX
        self.menu_sfx = pygame.mixer.Sound('./assets/audio/sfx/menu_select.ogg')

        # Input initialization
        self.keydown_up = False
        self.keydown_down = False
        self.keydown_space = False
        self.buttondown_lb = False
        self.buttondown_rb = False
        self.buttondown_a = False

    def display_cursor(self):
        """Display the cursor."""
        x = self.outline_rect.left + self.x - self.cursor.get_width()
        y = self.outline_rect.top + self.y + self.cursor_pos*64
        self.display_surface.blit(self.cursor, (x, y))

    def display_options(self, options):
        """Display the options.

        Arguments:
        options -- the options
        """
        x = self.outline_rect.left + self.x
        y = self.outline_rect.top + self.y
        for option in options:
            option_surface = self.selection_font.render(option, False, 'white')
            self.display_surface.blit(option_surface, (x, y))
            y += 64

    def display_text(self, text, small=False):
        """Display the text to display below the selection box.

        Arguments:
        text -- the text to display
        small -- if this flag is True, the lines of text will be closer together
        """
        if isinstance(text, str):
            if small: step = -2
            else: step = 2
            render(text, self.font, self.display_surface, self.textbox_rect, 'white', step)
        else:
            y = self.textbox_rect.top
            if small: step = 24
            else: step = 32
            for string in text:
                string_surface = self.font.render(string, False, 'white')
                self.display_surface.blit(string_surface, (self.textbox_rect.left, y))
                y += step

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
        if (keys[pygame.K_UP] or controller_lb) and not (self.keydown_up or self.buttondown_lb) and self.cursor_pos > 0:
            self.cursor_pos -= 1
            self.menu_sfx.play()
            self.keydown_up = True
            self.buttondown_lb = True
        elif (keys[pygame.K_DOWN] or controller_rb) and not (self.keydown_down or self.buttondown_rb) and self.cursor_pos < len(funcs) - 1:
            self.cursor_pos += 1
            self.menu_sfx.play()
            self.keydown_down = True
            self.buttondown_rb = True
        elif (keys[pygame.K_SPACE] or controller_a) and not (self.keydown_space or self.buttondown_a):
            self.menu_sfx.play()
            self.keydown_space = True
            self.buttondown_a = True
            funcs[self.cursor_pos]()
        if not keys[pygame.K_UP]: self.keydown_up = False
        if not keys[pygame.K_DOWN]: self.keydown_down = False
        if not keys[pygame.K_SPACE]: self.keydown_space = False
        if not controller_lb: self.buttondown_lb = False
        if not controller_rb: self.buttondown_rb = False
        if not controller_a: self.buttondown_a = False

    def run(self, options, text, *funcs, **kwargs):
        """Update and draw everything.

        Arguments:
        options -- the options
        text -- the text to display
        funcs -- the functions to run
        kwargs -- the keyword arguments, used to get the 'small' flag for self.display_text()
        """
        self.now = pygame.time.get_ticks()
        self.display_surface.fill('black')
        self.display_surface.blit(self.outline, self.outline_rect)
        if self.now - self.gen_time >= 250:
            self.get_input(funcs)
        self.display_cursor()
        self.display_options(options)
        self.display_text(text, kwargs.get('small', False))

class SelectionBoxYN(SelectionBox):
    """The Yes/No selection box."""
    def __init__(self, text, display_surface, parent):
        """Setup the box elements.

        Arguments:
        display_surface -- the screen
        parent -- the parent class
        """
        self.display_surface = display_surface
        self.parent = parent
        outline = './assets/ui/selection_box.png'
        self.options = ["Yes", "No"]
        self.text = text
        super().__init__(outline, self.display_surface, self.parent)

    def run(self, *funcs, **kwargs):
        """Update and draw everything.

        Arguments:
        funcs -- the functions to run
        kwargs -- see SelectionBox.run()
        """
        super().run(self.options, self.text, *funcs, **kwargs)
