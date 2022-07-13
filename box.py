import pygame

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
        self.input_box_topleft = self.outline_rect.topleft + pygame.math.Vector2(27, 67)
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
        for event in self.parent.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.text != '':
                    self.parent.main_menu.status = None
                    self.parent.savefile_path = './data/' + self.text
                    self.menu_sfx.play()
                    func()
                elif event.key == pygame.K_BACKSPACE:
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
