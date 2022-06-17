import pygame
from math import sin
from settings import *  # lgtm [py/polluting-import]
from misc import import_folder

"""This file defines the player behavior."""

class Player(pygame.sprite.Sprite):
    """This class defines the player."""
    def __init__(self, pos, display_surface, create_jump_particles, controller, parent):
        """Setup the player sprite, movement, particles, status and flags.

        Arguments:
        pos -- the position of the player spawn
        display_surface -- the screen
        create_jump_particles -- the method for creating the jump particles
        controller -- the controller class
        parent -- the parent class
        """
        super().__init__()
        self.display_surface = display_surface
        self.parent = parent
        self.game = self.parent.parent
        self.controllers = controller.controllers
        self.gamepad = 'xbox_one'
        self.base_path = './assets/player/'
        self.character = 'renzo'
        self.import_player_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.player_assets['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.collision_rect = pygame.Rect((self.rect.top - 2, self.rect.left - 2), (self.rect.width - 2, self.rect.height - 2))
        self.melee_weapon_rect = pygame.Rect(self.rect.topright, (0, 0))
        self.now = 0  # This is a dummy value
        self.gen_time = pygame.time.get_ticks()

        # SFX
        self.jump_sfx = pygame.mixer.Sound('./assets/audio/sfx/jump.ogg')
        self.jump_sfx.set_volume(0.25)
        self.melee_attack_sfx = pygame.mixer.Sound('./assets/audio/sfx/attack_melee.ogg')
        self.melee_attack_sfx.set_volume(0.5)
        self.player_hurt_sfx = pygame.mixer.Sound('./assets/audio/sfx/player_hurt.ogg')
        self.enemy_hurt_sfx = pygame.mixer.Sound('./assets/audio/sfx/enemy_hurt.ogg')

        # Player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 6
        self.gravity = 1
        self.jump_height = -22

        # Methods
        self.update_health = self.game.update_health

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
        self.melee_attacking = False
        self.melee_attack_time = 0

        # Input initialization
        self.keydown_space = False
        self.keydown_j = False
        self.buttondown_a = False
        self.buttondown_b = False

    def import_player_assets(self):
        """Place all the player assets in an easily accessible dictionary."""
        self.player_assets = {'run':  [], 'idle': [], 'jump': [], 'fall': []}
        for animation in self.player_assets.keys():
            full_path = self.base_path + self.character + '/' + animation
            self.player_assets[animation] = import_folder(full_path)

    def import_run_particles(self):
        """Import the run particles."""
        self.run_particles = import_folder('./assets/player/particles/run')

    def animate(self):
        """Animate the player and setup the player rect correctly."""
        if self.melee_attacking:
            animation = import_folder(self.base_path + self.character + '/attack/melee' + self.game.selection['melee'].animation)
            self.animation_speed = self.game.selection['melee'].animation_speed
            self.frame_index = 0
        else:
            animation = self.player_assets[self.status]
            self.animation_speed = 0.15
        # Frame index loop
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
            self.rect.bottomleft = self.collision_rect.bottomleft
            self.melee_weapon_rect.topleft = (self.rect.right, self.rect.top + self.game.selection['melee'].offset)
        else:
            flipped_image = pygame.transform.flip(image, True, False)  # flip(image, X-axis, Y-axis)
            self.image = flipped_image
            self.rect.bottomright = self.collision_rect.bottomright
            self.melee_weapon_rect.topright = (self.rect.left, self.rect.top + self.game.selection['melee'].offset)

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
        controller_b = False
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
            if controller.get_button(gamepad['buttons']['B']):
                controller_b = True
        keys = pygame.key.get_pressed()
        #mod_keys = pygame.key.get_mods()
        if (keys[pygame.K_a] or controller_left):
            self.direction.x = -1  # Left movement
            self.facing_right = False
            #if mod_keys & pygame.KMOD_ALT
        elif (keys[pygame.K_d] or controller_right):
            self.direction.x = 1  # Right movement
            self.facing_right = True
            #if mod_keys & pygame.KMOD_ALT
        else:
            self.direction.x = 0
        if (keys[pygame.K_SPACE] or controller_a) and not (self.keydown_space or self.buttondown_a) and self.on_ground and not self.jumping:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)
            self.keydown_space = True
            self.buttondown_a = True
        if (keys[pygame.K_j] or controller_b) and not (self.keydown_j or self.buttondown_b):
            if self.now - self.melee_attack_time >= self.game.selection['melee'].cooldown:
                self.melee_attacking = True
                self.melee_attack_time = pygame.time.get_ticks()
                self.melee_attack_sfx.play()
                self.update_melee_weapon_rect(False)
            self.keydown_j = True
            self.buttondown_b = True

        if not keys[pygame.K_SPACE]: self.keydown_space = False
        if not keys[pygame.K_j]: self.keydown_j = False
        if not controller_a: self.buttondown_a = False
        if not controller_b: self.buttondown_b = False

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

    def take_damage(self, damage, type):
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

    def update_melee_weapon_rect(self, reset):
        """Change the melee weapon rectangle.

        Arguments:
        reset -- if this flag is set to True, the rectangle will be reset
        """
        if not reset:
            self.melee_weapon_rect.size = (self.game.selection['melee'].range, self.game.selection['melee'].height)
        else:
            self.melee_weapon_rect.size = (0, 0)

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
        if self.melee_attacking:
            self.direction.x = 0
        if self.now - self.melee_attack_time >= self.game.selection['melee'].cooldown:
            self.melee_attacking = False
            self.update_melee_weapon_rect(True)
