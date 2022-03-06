import pygame
import random
from tile import AnimatedTile

class Enemy(AnimatedTile):
    def __init__(self, size, x, y, path, speed):
        super().__init__(size, x, y, path)
        self.speed = speed

    def move(self):
        self.rect.x += self.speed

    def flip(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, shift):
        super().update(shift)
        self.move()
        self.flip()

class Skeleton(Enemy):
    def __init__(self, size, x, y, path, offset):
        self.speed = random.randint(3, 6)
        # self.speed_start = 1
        # self.speed_stop = 8
        super().__init__(size, x, y, path, self.speed)
        self.rect.y -= offset

    # def reverse(self):
        # speed_start = self.speed_start * -1
        # speed_stop = self.speed_stop * -1
        # self.speed_start = speed_stop
        # self.speed_stop = speed_start

    def update(self, shift):
        # self.speed = random.randint(self.speed_start, self.speed_stop)
        super().update(shift)
