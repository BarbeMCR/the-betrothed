import pygame
from misc import import_folder

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.1
        if type == 'jump':
            self.frames = import_folder('./assets/player/particles/jump')
        if type == 'fall':
            self.frames = import_folder('./assets/player/particles/fall')
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
    def update(self, shift):
        self.animate()
        self.rect.x += shift
