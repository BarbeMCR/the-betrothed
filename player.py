import pygame
from math import sin
from settings import controllers
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
        self.gamepad = self.game.gamepad
        self.base_path = './assets/player/'
        self.character = self.game.character
        self.import_player_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.player_assets['idle'][self.frame_index]
        self.rect = self.image.get_rect(bottomleft=pos)
        self.collision_rect = pygame.Rect(self.rect)
        self.melee_weapon_rect = pygame.Rect(self.rect.topright, (0, 0))
        self.now = 0  # This is a dummy value
        self.gen_time = pygame.time.get_ticks()

        # SFX
        self.jump_sfx = pygame.mixer.Sound('./assets/audio/sfx/jump.ogg')
        self.jump_sfx.set_volume(0.25)
        self.melee_attack_sfx = pygame.mixer.Sound('./assets/audio/sfx/attack_melee.ogg')
        self.melee_attack_sfx.set_volume(0.5)
        self.ranged_attack_sfx = pygame.mixer.Sound('./assets/audio/sfx/attack_ranged.ogg')
        self.ranged_attack_sfx.set_volume(0.5)
        self.magical_attack_sfx = pygame.mixer.Sound('./assets/audio/sfx/attack_magical.ogg')
        self.magical_attack_sfx.set_volume(0.5)
        self.player_hurt_sfx = pygame.mixer.Sound('./assets/audio/sfx/player_hurt.ogg')
        self.enemy_hurt_sfx = pygame.mixer.Sound('./assets/audio/sfx/enemy_hurt.ogg')
        self.game_paused_sfx = pygame.mixer.Sound('./assets/audio/sfx/game_paused.ogg')
        self.game_resumed_sfx = pygame.mixer.Sound('./assets/audio/sfx/game_resumed.ogg')
        self.screenshot_taken_sfx = pygame.mixer.Sound('./assets/audio/sfx/screenshot_taken.ogg')

        # Player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.base_speed = 360
        self.speed = 360
        self.target_speed = 360
        self.gravity = 60
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
        self.stamina_depleted_time = 0
        self.melee_attacking = False
        self.melee_attack_time = 0
        self.ranged_attack_time = 0
        self.magical_attack_time = 0
        self.screenshot_taken = False

        # Input initialization
        self.keydown_space = False
        self.keydown_j = False
        self.keydown_k = False
        self.keydown_l = False
        self.keydown_esc = False
        self.keydown_backslash = False
        self.keydown_f2 = False
        self.buttondown_a = False
        self.buttondown_b = False
        self.buttondown_x = False
        self.buttondown_y = False
        self.buttondown_menu = False
        self.buttondown_logo = False
        self.buttondown_share = False

    def import_player_assets(self):
        """Place all the player assets in an easily accessible dictionary."""
        self.player_assets = {'run': [], 'idle': [], 'jump': [], 'fall': []}
        scene_conversion_table = {'day': 'day', 'night': 'night', 'dawn': 'dawn_dusk', 'dusk': 'dawn_dusk'}
        for animation in self.player_assets.keys():
            full_path = self.base_path + self.character + '/' + animation + '/' + scene_conversion_table[self.parent.scene]
            self.player_assets[animation] = import_folder(full_path)

    def import_run_particles(self):
        """Import the run particles."""
        self.run_particles = import_folder('./assets/player/particles/run')

    def animate(self):
        """Animate the player and setup the player rect correctly."""
        if self.melee_attacking:
            scene_conversion_table = {'day': 'day', 'night': 'night', 'dawn': 'dawn_dusk', 'dusk': 'dawn_dusk'}
            animation = import_folder(self.base_path + self.character + '/attack' + self.game.selection['melee'].animation + '/' + scene_conversion_table[self.parent.scene])
            self.animation_speed = self.game.selection['melee'].animation_speed
        else:
            animation = self.player_assets[self.status]
            self.animation_speed = 0.15 * (self.speed / self.base_speed)
        # Frame index loop
        self.frame_index += self.animation_speed*60*self.parent.delta
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

        if self.melee_attacking:
            self.rect = pygame.Rect(self.rect.topleft, (self.image.get_width() - self.game.selection['melee'].range, self.image.get_height()))
        else:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def animate_run_particles(self):
        """Animate the run particles if the player is on the ground."""
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed*60*self.parent.delta
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
        # To avoid using pygame.KEYDOWN events while keeping the same behavior:
        # if keys[key] and not keydown_key:
        #     ...
        #     keydown_key = True
        # if not keys[key]:
        #     keydown_key = False
        # where keydown_key is initialized as False
        #
        # To decode key modifiers:
        # key_mods = pygame.key.get_mods()
        # if key_mods == pygame.KMOD_NONE:
        #     ...
        # if key_mods & pygame.KMOD_SHIFT:
        #     ...
        # if key_mods & (pygame.KMOD_CTRL | pygame.KMOD_ALT):
        #     ...
        gamepad = controllers[self.gamepad]  # controllers is a value defined in settings
        controller_left = False
        controller_right = False
        controller_a = False
        controller_b = False
        controller_x = False
        controller_y = False
        controller_menu = False
        controller_logo = False
        controller_share = False
        controller_rt = -1
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
            if controller.get_button(gamepad['buttons']['X']):
                controller_x = True
            if controller.get_button(gamepad['buttons']['Y']):
                controller_y = True
            if controller.get_button(gamepad['buttons']['MENU']):
                controller_menu = True
            if controller.get_button(gamepad['buttons']['LOGO']):
                controller_logo = True
            if controller.get_button(gamepad['buttons']['SHARE']):
                controller_share = True
            controller_rt = controller.get_axis(gamepad['axes']['RT'])
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or controller_left):
            self.direction.x = -1  # Left movement
            self.facing_right = False
            self.check_player_running(keys, controller_rt)
        elif (keys[pygame.K_d] or controller_right):
            self.direction.x = 1  # Right movement
            self.facing_right = True
            self.check_player_running(keys, controller_rt)
        else:
            self.direction.x = 0
        if (keys[pygame.K_SPACE] or controller_a) and not (self.keydown_space or self.buttondown_a) and self.on_ground and not self.jumping:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)
            self.keydown_space = True
            self.buttondown_a = True
        if (keys[pygame.K_j] or controller_b) and not (self.keydown_j or self.buttondown_b or self.keydown_k or self.buttondown_x or self.keydown_l or self.buttondown_y):
            if self.now - self.melee_attack_time >= self.game.selection['melee'].cooldown:
                self.melee_attacking = True
                self.melee_attack_time = pygame.time.get_ticks()
                self.melee_attack_sfx.play()
                self.update_melee_weapon_rect(False)
                self.frame_index = 0
                for controller in self.controllers.values():
                    controller.rumble(0, 0.5, int(self.game.selection['melee'].cooldown / 2))
            self.keydown_j = True
            self.buttondown_b = True
            self.keydown_k = True
            self.buttondown_x = True
            self.keydown_l = True
            self.buttondown_y = True
        if (keys[pygame.K_k] or controller_x) and not (self.keydown_k or self.buttondown_x or self.keydown_j or self.buttondown_b or self.keydown_l or self.buttondown_y) and self.game.selection['ranged'].projectile.count > 0:
            if self.now - self.ranged_attack_time >= self.game.selection['ranged'].cooldown:
                self.ranged_attack_time = pygame.time.get_ticks()
                self.ranged_attack_sfx.play()
                self.game.selection['ranged'].projectile.count -= 1
                self.parent.create_ranged_projectile()
                for controller in self.controllers.values():
                    controller.rumble(0.5, 0.5, int(self.game.selection['ranged'].cooldown / 1.5))
            self.keydown_k = True
            self.buttondown_x = True
            self.keydown_j = True
            self.buttondown_b = True
            self.keydown_l = True
            self.buttondown_y = True
        if (keys[pygame.K_l] or controller_y) and not(self.keydown_l or self.buttondown_y or self.keydown_j or self.buttondown_b or self.keydown_k or self.buttondown_x) and self.game.energy[self.character] >= self.game.selection['magical'].cost:
            if self.now - self.magical_attack_time >= self.game.selection['magical'].cooldown:
                self.magical_attack_time = pygame.time.get_ticks()
                self.magical_attack_sfx.play()
                self.parent.decrease_energy(self.game.selection['magical'].cost)
                self.parent.create_magical_projectile()
                for controller in self.controllers.values():
                    controller.rumble(1, 0.5, int(self.game.selection['magical'].cooldown / 1.5))
            self.keydown_l = True
            self.buttondown_y = True
            self.keydown_j = True
            self.buttondown_b = True
            self.keydown_k = True
            self.buttondown_x = True
        if (keys[pygame.K_ESCAPE] or controller_menu) and not (self.keydown_esc or self.buttondown_menu):
            for controller in self.controllers.values():
                controller.rumble(0, 1, 250)
            self.game_paused_sfx.play()
            self.parent.create_pause_menu()
            self.keydown_esc = True
            self.buttondown_menu = True
        if (keys[pygame.K_BACKSLASH] or controller_logo) and not (self.keydown_backslash or self.buttondown_logo):
            for controller in self.controllers.values():
                controller.rumble(0.5, 0.5, 250)
            self.parent.display_overlay = not self.parent.display_overlay
            self.keydown_backslash = True
            self.buttondown_logo = True
        if (keys[pygame.K_F2] or controller_share) and not (self.keydown_f2 or self.buttondown_share):
            for controller in self.controllers.values():
                controller.rumble(0.5, 0.5, 250)
            self.screenshot_taken_sfx.play()
            self.screenshot_taken = True
            self.keydown_f2 = True
            self.buttondown_share = True

        if not keys[pygame.K_SPACE]: self.keydown_space = False
        if not keys[pygame.K_j]: self.keydown_j = False
        if not keys[pygame.K_k]: self.keydown_k = False
        if not keys[pygame.K_l]: self.keydown_l = False
        if not keys[pygame.K_ESCAPE]: self.keydown_esc = False
        if not keys[pygame.K_BACKSLASH]: self.keydown_backslash = False
        if not keys[pygame.K_F2]: self.keydown_f2 = False
        if not controller_a: self.buttondown_a = False
        if not controller_b: self.buttondown_b = False
        if not controller_x: self.buttondown_x = False
        if not controller_y: self.buttondown_y = False
        if not controller_menu: self.buttondown_menu = False
        if not controller_logo: self.buttondown_logo = False
        if not controller_share: self.buttondown_share = False

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

    def _reset_speed(self):
        """Reset the player speed if no direction key is pressed."""
        if self.direction.x == 0:
            self.speed = self.base_speed

    def check_player_running(self, keys, controller_rt):
        """Check whether the player is running and apply the additional speed.

        Arguments:
        keys -- the currently pressed keys
        controller_rt -- the current value of the right trigger
        """
        if self.game.stamina[self.character] > 0:
            if keys[pygame.K_LCTRL]:
                if keys[pygame.K_LALT]:
                    self.speed = int(self.base_speed * 2)
                else:
                    self.speed = int(self.base_speed * 1.5)
            else:
                self.speed = self.base_speed
            if controller_rt > -1:
                controller_rt += 1  # Range: -1 to 1 -> 0 to 2
                controller_rt /= 2  # Range: 0 to 2 -> 0 to 1
                controller_rt += 1  # Range: 0 to 1 -> 1 to 2
                if controller_rt > 1.05:  # Takes drifting into account
                    self.speed = int(self.base_speed * controller_rt)
                    for controller in self.controllers.values():
                        controller.rumble(0, controller_rt-1, 50)
                else:
                    self.speed = self.base_speed
        else:
            self.speed = self.base_speed

    def decrease_stamina(self):
        """Decrease the stamina if needed."""
        if self.speed > self.base_speed:
            self.game.stamina[self.character] -= int((self.speed-self.base_speed)*self.parent.delta)

    def refill_stamina(self):
        """Gradually refill the stamina and limit it."""
        if self.now - self.stamina_depleted_time >= 1000:
            if self.speed <= self.base_speed:
                if self.direction.x == 0:
                    self.game.stamina[self.character] += int(180*self.parent.delta)
                else:
                    self.game.stamina[self.character] += int(60*self.parent.delta)
            if self.game.stamina[self.character] > self.game.max_stamina[self.character]:
                self.game.stamina[self.character] = self.game.max_stamina[self.character]
            if self.game.stamina[self.character] < 0:
                self.stamina_depleted_time = pygame.time.get_ticks()
                self.game.stamina[self.character] = 0

    def jump(self):
        """Make the player jump."""
        self.direction.y = self.jump_height
        self.jumping = True
        self.jump_sfx.play()

    def apply_gravity(self):
        """Apply gravity to the player."""
        self.direction.y += self.gravity * self.parent.delta
        self.collision_rect.y += self.direction.y*60*self.parent.delta

    def take_damage(self, damage, type):
        """Deal damage to the player and play the hurt SFX.

        Arguments:
        damage -- the amount of damage to deal
        type -- the damage type
        """
        if damage > 0:
            if type == 'physical':
                if not self.invincible:
                    self.update_health(damage, True)
                    self.invincible = True
                    self.hurt_time = pygame.time.get_ticks()
                    self.player_hurt_sfx.play()  # This is repeated for each type of damage to avoid looping on each frame
            elif type == 'pure':
                self.update_health(damage, True)
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
        if self.melee_attacking:
            self.direction.x = 0
        if self.now - self.melee_attack_time >= self.game.selection['melee'].cooldown:
            self.melee_attacking = False
            self.update_melee_weapon_rect(True)
        self.get_status()
        self.animate()
        self.animate_run_particles()
        self.tick_invincibility_timer()
        self.create_sin_wave()
        self._reset_speed()
        self.decrease_stamina()
        self.refill_stamina()
