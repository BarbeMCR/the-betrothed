import pygame
from misc import import_folder

"""This file defines the particle behavior."""

class Particle(pygame.sprite.Sprite):
    """The particle builder class."""
    def __init__(self, pos, type):
        """Create the particle sprite based on its type.

        Arguments:
        pos -- the position of the particle
        type -- the type of the particle
        """
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.1
        if type == 'jump':
            self.frames = import_folder('./assets/player/particles/jump')
        if type == 'fall':
            self.frames = import_folder('./assets/player/particles/fall')
        if type == 'enemy_death':
            self.frames = import_folder('./assets/enemy/death')
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
    def animate(self):
        """Animate the particle."""
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
    def update(self, shift):
        """Update the particle.

        Arguments:
        shift -- the camera shift
        """
        self.animate()
        self.rect.x += shift
