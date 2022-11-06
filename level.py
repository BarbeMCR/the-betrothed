import pygame
import random
from misc import *  # lgtm [py/polluting-import]
from settings import *  # lgtm [py/polluting-import]
from tile import *  # lgtm [py/polluting-import]
from enemy import *  # lgtm [py/polluting-import]
from bgstuff import *  # lgtm [py/polluting-import]
from player import Player
from particles import Particle
from weapons import Projectile
from menu import PauseMenu
from data import levels

"""This file contains the level builder and numerous functions to control the game behavior."""

class Level:
    """The level builder class."""
    def __init__(self, display_surface, current_level, current_subpart, current_part, parent):
        """Setup the builder, the level layout, the player and the background.

        Arguments:
        current_level -- the currently selected level
        current_subpart -- the currently selected subpart
        current_part -- the currently selected part
        display_surface -- the screen
        parent -- the parent class
        """
        # Basic setup
        self.display_surface = display_surface
        self.parent = parent
        self.status = 'level'
        self.controller = self.parent.controller
        self.controllers = self.controller.controllers
        self.gamepad = self.parent.gamepad
        self.shift = 0
        self.start_x = 0
        self.pause_start = 0
        self.time_paused = 0

        # Loading screen
        self.display_surface.fill('black')
        loading_screen = pygame.image.load('./assets/ui/loading.png').convert_alpha()
        self.display_surface.blit(loading_screen, (64, 64))
        pygame.display.flip()

        # SFX
        self.energy_pickup_sfx = pygame.mixer.Sound('./assets/audio/sfx/energy_pickup.ogg')
        self.energy_pickup_sfx.set_volume(0.5)
        self.enemy_death_sfx = pygame.mixer.Sound('./assets/audio/sfx/enemy_death.ogg')
        self.player_death_sfx = pygame.mixer.Sound('./assets/audio/sfx/player_death.ogg')

        # World setup
        self.create_world = self.parent.create_world
        self.end_level = self.parent.end_level
        self.current_level = current_level
        self.current_subpart = current_subpart
        self.current_part = current_part
        level_data = levels[self.current_part][self.current_subpart][self.current_level]
        self.level_unlocked = level_data['unlock']
        self.level_completed = False
        self.level_completed_music_started = False

        # Level barriers
        barrier_layout = import_csv_layout(level_data['barriers'])
        self.barrier_sprites = self.create_tile_group(barrier_layout, 'barriers')

        # Player setup
        player_layout = import_csv_layout(level_data['setup'])
        self.player = pygame.sprite.GroupSingle()
        self.player_end = pygame.sprite.GroupSingle()
        self.setup_player(player_layout, self)
        self.ranged_sprites = pygame.sprite.Group()
        # Player particles
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False
        # Enemy particles
        self.enemy_death_sprites = pygame.sprite.Group()

        # UI
        self.update_energy = self.parent.update_energy
        self.reset_energy_overflow = self.parent.reset_energy_overflow
        self.display_overlay = True

        # Terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')
        # Background terrain setup
        bg_terrain_layout = import_csv_layout(level_data['background'])
        self.background_sprites = self.create_tile_group(bg_terrain_layout, 'background')
        # Building setup
        building_layout = import_csv_layout(level_data['buildings'])
        self.building_sprites = self.create_tile_group(building_layout, 'terrain')
        # Roof setup
        roof_layout = import_csv_layout(level_data['roofs'])
        self.roof_sprites = self.create_tile_group(roof_layout, 'roofs')
        # Decoration setup
        decoration_layout = import_csv_layout(level_data['decoration'])
        self.decoration_sprites = self.create_tile_group(decoration_layout, 'terrain')
        # Root setup
        root_layout = import_csv_layout(level_data['roots'])
        self.root_sprites = self.create_tile_group(root_layout, 'terrain')
        # Grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')
        # Energy setup
        energy_layout = import_csv_layout(level_data['energy'])
        self.energy_sprites = self.create_tile_group(energy_layout, 'energy')
        # Tree setup
        tree_layout = import_csv_layout(level_data['trees'])
        self.tree_sprites = self.create_tile_group(tree_layout, 'trees')

        # Enemies
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')
        # Enemy borders
        border_layout = import_csv_layout(level_data['borders'])
        self.border_sprites = self.create_tile_group(border_layout, 'borders')

        # Background
        self.sky = Sky(level_data['horizon'])
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 52, level_width, level_data['enable_water'])
        self.clouds = Clouds(320, level_width, random.randint(0, 32))
        self.mountains = Mountains(192, level_width, level_data['enable_mountains'])

        # Terrain optimization
        self.internal_terrain_sprites = pygame.sprite.Group()
        self.optimize_internal_terrain()
        for sprite in self.internal_terrain_sprites.sprites():
            self.terrain_sprites.remove(sprite)

        # Music
        pygame.mixer.music.load(level_data['music'])
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, fade_ms=2000)

        # Fade
        self.fade_surface = pygame.Surface((screen_width, screen_height))
        self.fade_surface.fill('black')
        self.fade_surface.set_alpha(255)

    def resume_level(self):
        """Resume the game."""
        pygame.mixer.music.unpause()
        now = pygame.time.get_ticks()
        self.time_paused = now - self.pause_start
        self._update_timestamps()
        self.player.sprite.game_resumed_sfx.play()
        self.player.sprite.keydown_space = True
        self.player.sprite.keydown_j = True
        self.player.sprite.buttondown_a = True
        self.player.sprite.buttondown_b = True
        self.status = 'level'
        for controller in self.controllers.values():
            controller.rumble(0, 1, 250)

    def _update_timestamps(self):
        """Update the timestamps so that they work as expected after resuming."""
        self.player.sprite.melee_attack_time += self.time_paused
        self.player.sprite.ranged_attack_time += self.time_paused
        self.player.sprite.hurt_time += self.time_paused
        self.player.sprite.gen_time += self.time_paused
        for enemy in self.enemy_sprites:
            enemy.hurt_time += self.time_paused
        if hasattr(self.player_end.sprite, 'ticks'):
            self.player_end.sprite.ticks += self.time_paused

    def create_pause_menu(self):
        """Build the pause menu and pause the game."""
        pygame.mixer.music.pause()
        self.pause_start = pygame.time.get_ticks()
        self.pause_menu = PauseMenu(self.display_surface, self)
        self.status = 'pause'

    def fade_in(self, amount):
        """Fade in the screen.

        Arguments:
        amount -- the higher the value, the faster the fade in
        """
        alpha = self.fade_surface.get_alpha()
        if alpha > 0:
            self.display_surface.blit(self.fade_surface, (0, 0))
            self.fade_surface.set_alpha(alpha - int(amount))
            if self.fade_surface.get_alpha() < 0:
                self.fade_surface.set_alpha(0)

    def fade_out(self, amount):
        """Fade out the screen.

        Arguments:
        amount -- the higher the value, the faster the fade out
        """
        alpha = self.fade_surface.get_alpha()
        if alpha < 255:
            self.display_surface.blit(self.fade_surface, (0, 0))
            self.fade_surface.set_alpha(alpha + int(amount))
            if self.fade_surface.get_alpha() > 255:
                self.fade_surface.set_alpha(255)

    def setup_player(self, layout, parent):
        """Place the player and the end-level cross based upon their position.

        Arguments:
        layout -- the level layout to use
        parent -- the parent class
        """
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if col == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles, self.controller, parent)
                    self.player.add(sprite)
                if col == '1':
                    cross_surface = pygame.image.load('./assets/level/ground/cross.png')
                    sprite = StaticTile(tile_size, x, y, cross_surface)
                    self.player_end.add(sprite)

    def create_jump_particles(self, pos):
        """Spawn the jump particles.

        Arguments:
        pos -- the position of the particles
        """
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(0, 32)
        else:
            pos += pygame.math.Vector2(0, -32)
        jump_particle_sprite = Particle(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def create_fall_particle(self):
        """Spawn the fall particles."""
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(0, 32)
            else:
                offset = pygame.math.Vector2(0, 32)
            fall_particle = Particle(self.player.sprite.rect.midbottom - offset, 'fall')
            self.dust_sprite.add(fall_particle)

    def get_player_on_ground(self):
        """Get whether the player is on the ground."""
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_tile_group(self, layout, type):
        """Make a group to hold in the sprites and return it.

        Arguments:
        layout -- the level layout to use
        type -- the type of the group
        """
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                if col != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'barriers':
                        sprite = Tile(tile_size, x, y - (tile_size * 3))

                    if type == 'terrain':
                        terrain_list = import_sliced_graphics('./assets/level/ground/ground_day.png')
                        tile_surface = terrain_list[int(col)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    if type == 'background':
                        bg_terrain_list = import_sliced_graphics('./assets/level/ground/bg_day.png')
                        tile_surface = bg_terrain_list[int(col)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    if type == 'roofs':
                        roof_list = import_sliced_graphics('./assets/level/ground/roofs.png')
                        tile_surface = roof_list[int(col)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    if type == 'grass':
                        grass_list = import_sliced_graphics('./assets/level/ground/grass.png')
                        tile_surface = grass_list[int(col)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    if type == 'trees':
                        sprite = Tree(tile_size, x, y, './assets/level/ground/tree.png', random.randrange(160, 192, 8))

                    if type == 'energy':
                        if col == '0':
                            sprite = Energy(tile_size, x, y, './assets/level/energy/blue', 2)
                        elif col == '1':
                            sprite = Energy(tile_size, x, y, './assets/level/energy/red', 5)
                        elif col == '2':
                            sprite = Energy(tile_size, x, y, './assets/level/energy/yellow', 10)
                        elif col == '3':
                            sprite = Energy(tile_size, x, y, './assets/level/energy/green', 20)

                    if type == 'enemies':
                        if col == '1':
                            sprite = Skeleton(tile_size, x, y, './assets/enemy/skeleton', 64)
                        elif col == '2':
                            sprite = Zombie(tile_size, x, y, './assets/enemy/zombie', 64)
                    if type == 'borders':
                        sprite = Tile(tile_size, x, y)
                    sprite_group.add(sprite)
            pygame.event.pump()
        return sprite_group

    def optimize_internal_terrain(self):
        """Optimize the internal terrain by detecting it and putting it in a separate group where collision isn't checked."""
        for target_tile in self.terrain_sprites.sprites():
            topleft_tile = False
            top_tile = False
            topright_tile = False
            left_tile = False
            right_tile = False
            bottomleft_tile = False
            bottom_tile = False
            bottomright_tile = False
            for sprite in self.terrain_sprites.sprites():
                if sprite.rect.collidepoint(target_tile.rect.topleft - pygame.math.Vector2(32, 32)):
                    topleft_tile = True
                elif sprite.rect.collidepoint(target_tile.rect.midtop - pygame.math.Vector2(0, 32)):
                    top_tile = True
                elif sprite.rect.collidepoint(target_tile.rect.topright - pygame.math.Vector2(-32, 32)):
                    topright_tile = True
                elif sprite.rect.collidepoint(target_tile.rect.midleft - pygame.math.Vector2(32, 0)):
                    left_tile = True
                elif sprite.rect.collidepoint(target_tile.rect.midright + pygame.math.Vector2(32, 0)):
                    right_tile = True
                elif sprite.rect.collidepoint(target_tile.rect.bottomleft + pygame.math.Vector2(-32, 32)):
                    bottomleft_tile = True
                elif sprite.rect.collidepoint(target_tile.rect.midbottom + pygame.math.Vector2(0, 32)):
                    bottom_tile = True
                elif sprite.rect.collidepoint(target_tile.rect.bottomright + pygame.math.Vector2(32, 32)):
                    bottomright_tile = True
            if topleft_tile and top_tile and topright_tile and left_tile and right_tile and bottomleft_tile and bottom_tile and bottomright_tile:
                self.internal_terrain_sprites.add(target_tile)
            elif target_tile.rect.bottom == screen_height and topleft_tile and top_tile and topright_tile and left_tile and right_tile:
                self.internal_terrain_sprites.add(target_tile)

    def apply_enemy_border_collision(self):
        """Reverse the enemies if they run into a border tile."""
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.border_sprites, False):
                enemy.reverse()

    def x_mov_coll(self):
        """Check the player horizontal movement collision and set the correct flags."""
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed
        # collidables = self.terrain_sprites.sprites() + self.whatever.sprites()
        # for sprite in collidables: collision code
        collidables = self.terrain_sprites.sprites() + self.barrier_sprites.sprites()
        for sprite in collidables:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left

    def y_mov_coll(self):
        """Check the player vertical movement collision and set the correct flags."""
        player = self.player.sprite
        player.apply_gravity()
        # See above for multiple collidable sprites
        collidables = self.terrain_sprites.sprites() + self.barrier_sprites.sprites()
        for sprite in collidables:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                    player.jumping = False
                elif player.direction.y < 0:
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0

        # Checks if the player is jumping
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False

    def scroll_x(self, speed):
        """Scroll the camera horizontally.

        Arguments:
        speed -- the speed the camera is scrolling and the player is moving
        """
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < screen_width / 2.5 and direction_x < 0:
            self.shift = speed
            player.speed = 0
        elif player_x > screen_width - (screen_width / 2.5) and direction_x > 0:
            self.shift = -speed
            player.speed = 0
        else:
            self.shift = 0
            player.speed = speed

    def increase_energy(self, amount):
        """Add energy to the player.

        Arguments:
        amount -- the amount of energy to add
        """
        self.update_energy(amount, True)

    def decrease_energy(self, amount):
        """Subtract energy from the player.

        Arguments:
        amount -- the amount of energy to subtract
        """
        self.update_energy(amount, False)

    def check_energy_collisions(self):
        """Check if the player collides with the energy and collect it."""
        energy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.energy_sprites, True)
        if energy_collisions:
            self.energy_pickup_sfx.play()
            for energy in energy_collisions:
                self.increase_energy(energy.value)

    def check_enemy_collisions(self):
        """Check if the player collides with the enemies and do actions accordingly."""
        for enemy in self.enemy_sprites:
            if self.player.sprite.collision_rect.colliderect(enemy.rect):
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.collision_rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y > 1:
                    self.player.sprite.direction.y = int(self.player.sprite.jump_height / 2)
                    enemy.health -= 1
                    self.player.sprite.enemy_hurt_sfx.play()
                    self.player.sprite.invincibility_ticks = 250
                    self.player.sprite.invincible = True
                    self.player.sprite.hurt_time = pygame.time.get_ticks()
                    if random.randint(1, 4) == 1:
                        self.player.sprite.take_damage(enemy.damage / 10, 'pure')
                else:
                    self.player.sprite.take_damage(enemy.damage, 'physical')

    def check_enemy_melee_collisions(self):
        """Check if the melee weapon collides with the enemies and damage them if so."""
        for enemy in self.enemy_sprites:
            if self.player.sprite.melee_weapon_rect.colliderect(enemy.rect):
                if enemy.melee_resistance < 5:
                    if not enemy.invincible:
                        damage = self.parent.selection['melee'].damage[self.parent.selection['melee'].level]
                        damage -= 20*enemy.melee_resistance/100 * damage
                        enemy.health -= damage
                        self.player.sprite.enemy_hurt_sfx.play()
                        enemy.invincible = True
                        enemy.hurt_time = pygame.time.get_ticks()
                        melee_weapon_cooldown = self.parent.selection['melee'].cooldown
                        if melee_weapon_cooldown >= 500:
                            if melee_weapon_cooldown <= 750:
                                enemy.stun_duration = random.randint(melee_weapon_cooldown, melee_weapon_cooldown+100)
                            else:
                                enemy.stun_duration = random.randint(melee_weapon_cooldown-100, melee_weapon_cooldown)

    def check_enemy_ranged_collisions(self):
        """Check if the ranged weapon projectiles are valid, then check if they collide with the enemies."""
        for projectile in self.ranged_sprites:
            if abs((self.start_x-projectile.rect.x)*-1 - projectile.start_x) > self.parent.selection['ranged'].range:
                projectile.kill()
            collidables = self.terrain_sprites.sprites() + self.barrier_sprites.sprites()
            if pygame.sprite.spritecollideany(projectile, collidables) is not None:
                projectile.kill()
        enemy_collisions = pygame.sprite.groupcollide(self.ranged_sprites, self.enemy_sprites, False, False)
        if enemy_collisions:
            for projectile, enemies in enemy_collisions.items():
                for enemy in enemies:
                    if enemy.ranged_resistance < 5:
                        if not enemy.invincible:
                            damage = self.parent.selection['ranged'].damage[self.parent.selection['ranged'].level]
                            damage -= 20*enemy.ranged_resistance/100 * damage
                            enemy.health -= damage
                            self.player.sprite.enemy_hurt_sfx.play()
                            enemy.invincible = True
                            enemy.hurt_time = pygame.time.get_ticks()
                            enemy.stun_duration = self.parent.selection['ranged'].cooldown
                projectile.kill()

    def create_ranged_projectile(self):
        """Create a ranged projectile sprite and add it to the correct group."""
        image = self.parent.selection['ranged'].projectile.image
        if self.player.sprite.facing_right:
            pos = self.player.sprite.rect.midright
            facing_right = True
        else:
            pos = self.player.sprite.rect.midleft
            facing_right = False
        pos -= pygame.math.Vector2(0, 16)  # This allows for the projectile to be shot from higher up
        speed = self.parent.selection['ranged'].speed
        start_x = (self.start_x - pos[0]) * -1
        ranged_projectile = Projectile(image, pos, speed, facing_right, start_x)
        self.ranged_sprites.add(ranged_projectile)

    def check_enemy_death(self):
        """Check if the enemies should be dead and kill their sprites if that is the case."""
        for enemy in self.enemy_sprites.sprites():
            if enemy.health <= 0:
                death_particle = Particle(enemy.rect.center, 'enemy_death')
                self.enemy_death_sprites.add(death_particle)
                enemy.kill()
                if self.current_level >= self.end_level and not self.parent.loaded_from_savefile:
                    self.increase_energy(enemy.energy + enemy.toughness)
                else:
                    self.increase_energy(int((enemy.energy + enemy.toughness) / 3))
                self.player.sprite.enemy_hurt_sfx.stop()
                self.enemy_death_sfx.play()

    def check_fall_death(self):
        """Check if the player has fallen and should be dead."""
        if self.player.sprite.collision_rect.top > 4 * screen_height:
            self.player.sprite.take_damage(5, 'pure')
            self.decrease_energy(random.randint(1, 25))
            self.reset_energy_overflow()
            self.player_death_sfx.play()
            self.player.sprite.collision_rect.top = -2 * tile_size
            self.player.sprite.gravity = 1
            self.player.sprite.direction.y = 0

    def check_success(self):
        """Check if the player completed the level and put them back to the level selection screen."""
        if pygame.sprite.spritecollide(self.player.sprite, self.player_end, False) and not self.level_completed:
            self.player_end.sprite.ticks = pygame.time.get_ticks()
            self.level_completed = True
        elif self.level_completed:
            self.run_end_level_sequence()

    def run_end_level_sequence(self):
        """Run the end level sequence."""
        now = pygame.time.get_ticks()
        if not self.level_completed_music_started:
            pygame.mixer.music.stop()
            pygame.mixer.music.load('./assets/audio/level_completed.ogg')
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play()
            self.level_completed_music_started = True
        if now - self.player_end.sprite.ticks >= 1000:
            if self.current_level >= self.end_level:
                self.player.sprite.heal(5)
                self.parent.loaded_from_savefile = False
            self.parent.save()
            self.create_world(self.level_unlocked, self.level_unlocked, self.current_subpart, self.current_part)

    def run(self, delta):
        """Run the level and the menus, update and draw everything (must be called every frame).

        Arguments:
        delta -- the time delta
        """
        if self.status == 'level':
            # Level barriers
            self.barrier_sprites.update(self.shift)

            # Background
            self.sky.draw(self.display_surface)
            self.mountains.draw(self.display_surface, int(self.shift / 3))
            self.water.draw(self.display_surface, int(self.shift / 3))
            self.clouds.draw(self.display_surface, int(self.shift / 3))

            # Particles
            self.dust_sprite.update(self.shift)
            self.dust_sprite.draw(self.display_surface)

            # Terrain
            self.terrain_sprites.update(self.shift)
            self.terrain_sprites.draw(self.display_surface)
            self.internal_terrain_sprites.update(self.shift)
            self.internal_terrain_sprites.draw(self.display_surface)
            # Background terrain
            self.background_sprites.update(self.shift)
            self.background_sprites.draw(self.display_surface)
            # Buildings
            self.building_sprites.update(self.shift)
            self.building_sprites.draw(self.display_surface)
            # Roofs
            self.roof_sprites.update(self.shift)
            self.roof_sprites.draw(self.display_surface)
            # Decoration
            self.decoration_sprites.update(self.shift)
            self.decoration_sprites.draw(self.display_surface)
            # Roots
            self.root_sprites.update(self.shift)
            self.root_sprites.draw(self.display_surface)
            # Grass
            self.grass_sprites.update(self.shift)
            self.grass_sprites.draw(self.display_surface)
            # Trees
            self.tree_sprites.update(self.shift)
            self.tree_sprites.draw(self.display_surface)
            # Energy
            self.energy_sprites.update(self.shift)
            if self.current_level >= self.end_level and not self.parent.loaded_from_savefile:
                self.energy_sprites.draw(self.display_surface)
                self.check_energy_collisions()
            # Enemies
            self.enemy_sprites.update(self.shift)
            self.border_sprites.update(self.shift)
            self.apply_enemy_border_collision()
            self.enemy_sprites.draw(self.display_surface)
            self.enemy_death_sprites.update(self.shift)
            self.enemy_death_sprites.draw(self.display_surface)

            # End tile
            self.player_end.update(self.shift)
            self.player_end.draw(self.display_surface)
            # Player
            self.player.update()
            self.x_mov_coll()
            self.get_player_on_ground()
            self.y_mov_coll()
            self.create_fall_particle()
            self.scroll_x(int(360*delta))
            self.start_x += self.shift
            # The code below allows for adjusting the player blitting position when melee attacking and facing left so that the player doesn't "slide" right
            if self.player.sprite.melee_attacking and not self.player.sprite.facing_right:
                self.display_surface.blit(self.player.sprite.image, self.player.sprite.rect.topleft - pygame.math.Vector2(self.parent.selection['melee'].range, 0))
            else:
                self.player.draw(self.display_surface)  # Normal draw routine
            self.ranged_sprites.update(self.shift)
            self.ranged_sprites.draw(self.display_surface)

            # Enemy routines
            self.check_enemy_collisions()
            self.check_enemy_melee_collisions()
            self.check_enemy_ranged_collisions()
            self.check_enemy_death()

            # Level end
            self.check_fall_death()
            self.check_success()

        elif self.status == 'pause':
            self.pause_menu.run()
