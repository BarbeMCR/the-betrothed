import pygame

"""This file contains the whole controller interface and is made for ease of access rather than convenience."""

class Controller:
    """The controller interface."""
    def __init__(self):
        """Initialize the joystick module and build the controller dict."""
        pygame.joystick.init()
        self.controllers = {controller: pygame.joystick.Joystick(controller) for controller in range(pygame.joystick.get_count())}
