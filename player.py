import pygame
from misc import import_folder

"""This file defines the player behavior."""

class Player(pygame.sprite.Sprite):
    """This class defines the player."""
    def __init__(self, pos, display_surface, create_jump_particle):
        """Setup the player sprite, movement, particles, status and flags.

        Arguments:
        pos -- the position of the player spawn
        display_surface -- the screen
        create_jump_particle -- the method for creating the jump particles
        """
        super().__init__()
        self.display_surface = display_surface
        self.import_player_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.player_assets['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        # Player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 6
        self.gravity = 1
        self.jump_height = -22

        # Dust particles
        self.import_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.create_jump_particle = create_jump_particle

        # Player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left_wall = False
        self.on_right_wall = False
        self.jumping = False

    def import_player_assets(self):
        """Place all the player assets in an easily accessible dictionary."""
        player_path = './assets/player/'
        self.player_assets = {'run':  [], 'idle': [], 'jump': [], 'fall': []}
        for animation in self.player_assets.keys():
            full_path = player_path + animation
            self.player_assets[animation] = import_folder(full_path)

    def import_run_particles(self):
        """Import the run particles."""
        self.run_particles = import_folder('./assets/player/particles/run')

    def animate(self):
        """Animate the player and setup the player rect correctly."""
        animation = self.player_assets[self.status]
        # Frame index loop
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)  # flip(image, X-axis, Y-axis)
            self.image = flipped_image

        # Rect setup
        if self.on_ground and self.on_right_wall:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left_wall:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right_wall:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left_wall:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        else:  # Fallback for rect setup
            self.rect = self.image.get_rect(center = self.rect.center)

    def animate_run_particles(self):
        """Animate the run particles if the player is on the ground."""
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.run_particles):
                self.dust_frame_index = 0

            particle = self.run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(28, 32)
                self.display_surface.blit(particle, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6, 32)
                flipped_particle = pygame.transform.flip(particle, True, False)
                self.display_surface.blit(flipped_particle, pos)

    def get_input(self):
        """Get the input from the keyboard and do the correct actions."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.direction.x = -1  # Left movement
            self.facing_right = False
        elif keys[pygame.K_d]:
            self.direction.x = 1  # Right movement
            self.facing_right = True
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground and not self.on_ceiling:
            if not self.jumping:
                self.jump()
                self.create_jump_particle(self.rect.midbottom)

    def get_status(self):
        """Check the current player status and update it."""
        if self.direction.y < 0 and not self.on_ground:
            self.status = 'jump'
        elif self.direction.y > 1 and not self.on_ceiling:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def jump(self):
        """Make the player jump."""
        self.direction.y = self.jump_height
        self.on_ceiling = False
        self.jumping = True

    def apply_gravity(self):
        """Apply gravity to the player."""
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self):
        """Update the player."""
        self.get_input()
        self.get_status()
        self.animate()
        self.animate_run_particles()
