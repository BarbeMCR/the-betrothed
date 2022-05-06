import pygame
import random
from misc import *
from settings import *
from tile import *
from enemy import *
from bgstuff import *
from player import Player
from particles import Particle
from data import levels

"""This file contains the level builder and a few useful functions for various behavior."""

class Level:
    """The level builder class."""
    def __init__(self, current_level, display_surface, create_world):
        """Setup the builder, the level layout, the player and the background.

        Arguments:
        current_level -- the selected level
        display_surface -- the screen
        create_world -- the method for building the world
        """
        # Basic setup
        self.display_surface = display_surface
        self.shift = 0
        self.current_x = None
        #self.now = pygame.time.get_ticks()

        # World setup
        #self.level_finished = False
        #self.trigger_level_end = False
        self.create_world = create_world
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.level_unlocked = level_data['unlock']

        # Level barriers
        barrier_layout = import_csv_layout(level_data['barriers'])
        self.barrier_sprites = self.create_tile_group(barrier_layout, 'barriers')

        # Player setup
        player_layout = import_csv_layout(level_data['setup'])
        self.player = pygame.sprite.GroupSingle()
        self.player_end = pygame.sprite.GroupSingle()
        self.setup_player(player_layout)
        # Player particles
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # Terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')
        # Building setup
        building_layout = import_csv_layout(level_data['buildings'])
        self.building_sprites = self.create_tile_group(building_layout, 'terrain')
        # Roof setup
        roof_layout = import_csv_layout(level_data['roofs'])
        self.roof_sprites = self.create_tile_group(roof_layout, 'roofs')
        # Window setup
        window_layout = import_csv_layout(level_data['windows'])
        self.window_sprites = self.create_tile_group(window_layout, 'terrain')
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
        self.skeleton_sprites = self.create_tile_group(enemy_layout, 'enemies')
        self.enemy_sprites = [self.skeleton_sprites]  # [self.skeleton_sprites, self.<enemy>_sprites]
        # Enemy borders
        border_layout = import_csv_layout(level_data['borders'])
        self.border_sprites = self.create_tile_group(border_layout, 'borders')

        # Background
        self.sky = Sky(7)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 52, level_width, level_data['enable_water'])
        self.clouds = Clouds(320, level_width, random.randint(0, 32))
        self.mountains = Mountains(192, level_width, level_data['enable_mountains'])

    def setup_player(self, layout):
        """Place the player and the end-level cross based upon their position

        Arguments:
        layout -- the level layout to use
        """
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if col == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles)
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
                    if type == 'roofs':
                        roof_list = import_sliced_graphics('./assets/level/ground/roofs.png')
                        tile_surface = roof_list[int(col)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    if type == 'grass':
                        grass_list = import_sliced_graphics('./assets/level/ground/grass.png')
                        tile_surface = grass_list[int(col)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    if type == 'energy':
                        sprite = AnimatedTile(tile_size, x, y, './assets/level/energy')
                    if type == 'trees':
                        sprite = Tree(tile_size, x, y, './assets/level/ground/tree.png', random.randrange(160, 192, 8))

                    if type == 'enemies':
                        if col == '0':
                            sprite = Skeleton(tile_size, x, y, './assets/skeleton', 64)
                    if type == 'borders':
                        sprite = Tile(tile_size, x, y)
                    sprite_group.add(sprite)
        return sprite_group

    def apply_enemy_border_collision(self):
        """Reverse the enemies if they run into a border tile."""
        for group in self.enemy_sprites:
            for enemy in group.sprites():
                if pygame.sprite.spritecollide(enemy, self.border_sprites, False):
                    enemy.reverse()

    def x_mov_coll(self):
        """Check the player horizontal movement collision and set the correct flags."""
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        # collidables = self.terrain_sprites.sprites() + self.whatever.sprites()
        # for sprite in collidables: collision code
        collidables = self.terrain_sprites.sprites() + self.barrier_sprites.sprites()
        for sprite in collidables:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left_wall = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right_wall = True
                    self.current_x = player.rect.right

        # Checks if the player is touching a wall on the left
        if player.on_left_wall and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left_wall = False
        # Checks if the player is touching a wall on the right
        if player.on_right_wall and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right_wall = False

    def y_mov_coll(self):
        """Check the player vertical movement collision and set the correct flags."""
        player = self.player.sprite
        player.apply_gravity()
        # See above for multiple collidable sprites
        collidables = self.terrain_sprites.sprites() + self.barrier_sprites.sprites()
        for sprite in collidables:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                    player.jumping = False
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        # Checks if the player is jumping
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        # Checks if the player is falling
        if player.on_ceiling and player.direction.y > 0 or (player.on_ceiling and player.on_ground and player.direction.x != 0):
            player.on_ceiling = False

    def scroll_x(self):
        """Scroll the camera horizontally."""
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        # BOTH self.shift and player.speed must be the same value as player.speed in player.py
        if player_x < screen_width / 4 and direction_x < 0:
            self.shift = 6
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.shift = -6
            player.speed = 0
        else:
            self.shift = 0
            player.speed = 6

    def check_death(self):
        """Check if the player is dead."""
        if self.player.sprite.rect.top > 2 * screen_height:
            self.create_world(self.current_level, self.current_level)  # self.create_world(current_level, level_unlocked)

    def check_success(self):
        """Check if the player completed the level and put them back to the level selection screen."""
        if pygame.sprite.spritecollide(self.player.sprite, self.player_end, False):
            pygame.display.flip()
            pygame.time.wait(500)
            self.create_world(self.current_level, self.level_unlocked)
        # The code below allows for a delay (the player can be controlled) to happen before being sent to the level selection screen
        #if self.level_finished:
            #global now
            #now = pygame.time.get_ticks()
            #self.level_finished = False
            #self.trigger_level_end = True
        #if pygame.sprite.spritecollide(self.player.sprite, self.player_end, False):
            #if not self.trigger_level_end:
                #self.level_finished = True
        #if self.trigger_level_end:
            #if self.now - now >= 1000:
                #del now
                #self.create_world(self.current_level, self.level_unlocked)

    def run(self):
        """Run the level, update and draw everything (must be called every frame)."""
        #self.now = pygame.time.get_ticks()
        # Level barriers
        self.barrier_sprites.update(self.shift)

        # Background
        self.sky.draw(self.display_surface)
        self.mountains.draw(self.display_surface, self.shift / 3)
        self.water.draw(self.display_surface, self.shift / 3)
        self.clouds.draw(self.display_surface, self.shift / 3)

        # Particles
        self.dust_sprite.update(self.shift)
        self.dust_sprite.draw(self.display_surface)

        # Terrain
        self.terrain_sprites.update(self.shift)
        self.terrain_sprites.draw(self.display_surface)
        # Buildings
        self.building_sprites.update(self.shift)
        self.building_sprites.draw(self.display_surface)
        # Roofs
        self.roof_sprites.update(self.shift)
        self.roof_sprites.draw(self.display_surface)
        # Windows
        self.window_sprites.update(self.shift)
        self.window_sprites.draw(self.display_surface)
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
        self.energy_sprites.draw(self.display_surface)
        # Enemies
        for group in self.enemy_sprites:
            group.update(self.shift)
        self.border_sprites.update(self.shift)
        self.apply_enemy_border_collision()
        for group in self.enemy_sprites:
            group.draw(self.display_surface)

        # End tile
        self.player_end.update(self.shift)
        self.player_end.draw(self.display_surface)
        # Player
        self.player.update()
        self.x_mov_coll()
        self.get_player_on_ground()
        self.y_mov_coll()
        self.create_fall_particle()
        self.scroll_x()
        self.player.draw(self.display_surface)

        # Level end
        self.check_death()
        self.check_success()
