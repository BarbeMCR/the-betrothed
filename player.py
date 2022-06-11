import pygame
from math import sin
from settings import *  # lgtm [py/polluting-import]
from misc import import_folder

"""This file defines the player behavior."""

class Player(pygame.sprite.Sprite):
    """This class defines the player."""
    def __init__(self, pos, display_surface, create_jump_particles, controller, update_health):
        """Setup the player sprite, movement, particles, status and flags.

        Arguments:
        pos -- the position of the player spawn
        display_surface -- the screen
        create_jump_particles -- the method for creating the jump particles
        controller -- the controller class
        update_health -- the method for updating the health
        """
        super().__init__()
        self.display_surface = display_surface
        self.controllers = controller.controllers
        self.gamepad = 'xbox_one'
        self.import_player_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.player_assets['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.collision_rect = pygame.Rect((self.rect.top - 2, self.rect.left - 2), (self.rect.width - 2, self.rect.height - 2))
        self.now = 0  # This is a dummy value
        self.gen_time = pygame.time.get_ticks()

        # SFX
        self.jump_sfx = pygame.mixer.Sound('./assets/audio/sfx/jump.wav')
        self.jump_sfx.set_volume(0.25)
        self.player_hurt_sfx = pygame.mixer.Sound('./assets/audio/sfx/player_hurt.wav')
        self.enemy_hurt_sfx = pygame.mixer.Sound('./assets/audio/sfx/enemy_hurt.wav')

        # Player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 6
        self.gravity = 1
        self.jump_height = -22

        # Methods
        self.update_health = update_health

        # Dust particles
        self.import_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.create_jump_particles = create_jump_particles

        # Player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.jumping = False
        self.invincible = False
        self.invincibility_ticks = 1000
        self.hurt_time = 0  # This is a timestamp, like self.gen_time

        # Input initialization
        self.keydown_space = False
        self.buttondown_a = False

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
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            flipped_image = pygame.transform.flip(image, True, False)  # flip(image, X-axis, Y-axis)
            self.image = flipped_image
            self.rect.bottomright = self.collision_rect.bottomright

        # Sprite flickering
        alpha = self.create_sin_wave()
        if self.invincible:
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

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
        """Get the input from the devices and do the correct actions."""
        # To avoid using pygame.KEYDOWN events whilst keeping the same behavior:
        # if keys[key] and not keydown_key:
        #     ...
        #     keydown_key = True
        # if not keys[key]:
        #     keydown_key = False
        # where keydown_key is initialized as False
        gamepad = controllers[self.gamepad]  # controllers is a value defined in settings
        controller_left = False
        controller_right = False
        controller_a = False
        for controller in self.controllers.values():
            if self.gamepad == 'ps4' or self.gamepad == 'switch_pro':
                if controller.get_button(gamepad['buttons']['LEFT']):
                    controller_left = True
                elif controller.get_button(gamepad['buttons']['RIGHT']):
                    controller_right = True
            else:
                if controller.get_hat(0) == gamepad['hat']['LEFT']:
                    controller_left = True
                elif controller.get_hat(0) == gamepad['hat']['RIGHT']:
                    controller_right = True
            if controller.get_button(gamepad['buttons']['A']):
                controller_a = True
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or controller_left):
            self.direction.x = -1  # Left movement
            self.facing_right = False
        elif (keys[pygame.K_d] or controller_right):
            self.direction.x = 1  # Right movement
            self.facing_right = True
        else:
            self.direction.x = 0
        if (keys[pygame.K_SPACE] or controller_a) and not (self.keydown_space or self.buttondown_a) and self.on_ground and not self.jumping:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)
            self.keydown_space = True
            self.buttondown_a = True

        if not keys[pygame.K_SPACE]: self.keydown_space = False
        if not controller_a: self.buttondown_a = False

    def get_status(self):
        """Check the current player status and update it."""
        if self.direction.y < 0 and not self.on_ground:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def jump(self):
        """Make the player jump."""
        self.direction.y = self.jump_height
        self.jumping = True
        self.jump_sfx.play()

    def apply_gravity(self):
        """Apply gravity to the player."""
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def get_damage(self, damage, type):
        """Deal damage to the player and play the hurt SFX.

        Arguments:
        damage -- the amount of damage to deal
        type -- the damage type
        """
        if type == 'physical':
            if not self.invincible and damage > 0:
                self.update_health(damage, True)
                self.invincible = True
                self.hurt_time = pygame.time.get_ticks()
                self.player_hurt_sfx.play()
        elif type == 'pure':
            self.update_health(damage, True)

        if not type == 'physical':
            self.player_hurt_sfx.play()

    def heal(self, healing):
        """Heal the player.

        Arguments:
        healing -- the amount of health to heal
        """
        self.update_health(healing, False)

    def tick_invincibility_timer(self):
        """Tick down the invincibility timer."""
        if self.invincible:
            if self.now - self.hurt_time >= self.invincibility_ticks:
                self.invincible = False
                self.invincibility_ticks = 1000

    def create_sin_wave(self):
        """Create a sin wave for sprite flickering and return an alpha value of either full or no transparency."""
        wave = sin(self.now)
        if wave >= 0:
            return 255
        else:
            return 0

    def update(self):
        """Update the player."""
        self.now = pygame.time.get_ticks()
        if self.now - self.gen_time >= 100:
            self.get_input()
        self.get_status()
        self.animate()
        self.animate_run_particles()
        self.tick_invincibility_timer()
        self.create_sin_wave()
