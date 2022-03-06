import pygame
import random
from misc import import_csv_layout, import_sliced_graphics
from settings import *
from tile import *
from enemy import *
from bgstuff import *
from player import Player
from particles import Particle

class Level:
    def __init__(self, level_data, display_surface):
        # Basic setup
        self.display_surface = display_surface
        self.shift = 0
        self.current_x = None

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
        self.sky = Sky(7)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 52, level_width)
        self.clouds = Clouds(320, level_width, random.randint(0, 32))
        self.mountains = Mountains(192, level_width, True)

    def setup_player(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if col == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player.add(sprite)
                if col == '1':
                    chapel_surface = pygame.image.load('./assets/level/ground/cross.png')
                    sprite = StaticTile(tile_size, x, y, chapel_surface)
                    self.player_end.add(sprite)

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(0, 32)
        else:
            pos += pygame.math.Vector2(0, -32)
        jump_particle_sprite = Particle(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def create_fall_particle(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(0, 32)
            else:
                offset = pygame.math.Vector2(0, 32)
            fall_particle = Particle(self.player.sprite.rect.midbottom - offset, 'fall')
            self.dust_sprite.add(fall_particle)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                if col != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'barriers':
                        sprite = Tile(tile_size, x, y - (tile_size * 3))

                    if type == 'terrain':
                        terrain_list = import_sliced_graphics('./assets/level/ground/ground.png')
                        tile_surface = terrain_list[int(col)]
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
                        sprite = Skeleton(tile_size, x, y, './assets/skeleton', 63)
                    if type == 'borders':
                        sprite = Tile(tile_size, x, y)
                    sprite_group.add(sprite)
        return sprite_group

    def apply_border_collision(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.border_sprites, False):
                enemy.reverse()

    def x_mov_coll(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        # collidables = self.terrain_sprites.sprites() + self.whatever.sprites()
        # for sprite in collidables: collision code
        for sprite in self.terrain_sprites.sprites() + self.barrier_sprites.sprites():
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
        player = self.player.sprite
        player.apply_gravity()
        # See above for multiple collidable sprites
        for sprite in self.terrain_sprites.sprites() + self.barrier_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        # Checks if the player is jumping
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        # Checks if the player is falling
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def scroll_x(self):
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

    def update(self):
        # Level barriers
        self.barrier_sprites.update(self.shift)

        # Background
        self.sky.draw(self.display_surface)
        self.mountains.draw(self.display_surface, self.shift / 3)
        self.water.draw(self.display_surface, self.shift / 3)
        self.clouds.draw(self.display_surface, self.shift / 3)

        # Terrain
        self.terrain_sprites.update(self.shift)
        self.terrain_sprites.draw(self.display_surface)
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
        self.enemy_sprites.update(self.shift)
        self.border_sprites.update(self.shift)
        self.apply_border_collision()
        self.enemy_sprites.draw(self.display_surface)

        # End tile
        self.player_end.update(self.shift)
        self.player_end.draw(self.display_surface)
        # Player with particles
        self.dust_sprite.update(self.shift)
        self.dust_sprite.draw(self.display_surface)
        self.player.update()
        self.x_mov_coll()
        self.get_player_on_ground()
        self.y_mov_coll()
        self.create_fall_particle()
        self.scroll_x()
        self.player.draw(self.display_surface)
