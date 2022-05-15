import pygame
from settings import *
from data import levels

"""This file defines the level selection screen."""

class Node(pygame.sprite.Sprite):
    """The level node class."""
    def __init__(self, pos, unlocked, movement_speed, image):
        """Create the node surface and the target rect inside the node.

        Arguments:
        pos -- the position of the node
        unlocked -- the node will appear as unlocked only if this flag is set to True
        movement_speed -- the speed at which the level selector travels
        image -- the path to the node graphics
        """
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        if unlocked:
            self.status = 'unlocked'
        else:
            self.status = 'locked'
        pos = (pos[0], pos[1] - 34)  # Lowering by 18 pixels makes for a cool effect when the cross moves
        self.rect = self.image.get_rect(center = pos)
        self.target_rect = pygame.Rect(self.rect.centerx - (movement_speed / 2), self.rect.centery - (movement_speed / 2), movement_speed, movement_speed)

    def update(self):
        """Update the node based on its status."""
        if self.status == 'locked':  # Fill the node with black
            copy = self.image.copy()
            copy.fill('black', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(copy, (0, 0))

class LevelSelector(pygame.sprite.Sprite):
    """The level selector class."""
    def __init__(self, pos):
        """Create the level selector.

        Arguments:
        pos -- the level selector initial position
        """
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load('./assets/world/cross.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        """Update the level selector."""
        self.rect.center = self.pos

class World:
    """The world builder class."""
    def __init__(self, first_level, start_level, end_level, display_surface, create_level, controller):
        """Setup the level selector screen, the movement of the cursor and the sprites.

        Arguments:
        first_level -- the lowest level the player can select
        start_level -- the level to place the cursor on
        end_level -- the highest level the player can select
        display_surface -- the screen
        create_level -- the method for building the level
        controller -- the controller class
        """
        # Setup
        self.display_surface = display_surface
        self.controllers = controller.controllers
        self.gamepad = 'xbox_one'
        self.first_level = first_level
        self.current_level = start_level
        self.end_level = end_level
        self.create_level = create_level
        self.background = pygame.image.load('./assets/world/part1.png').convert_alpha()

        # Movement logic
        self.movement_direction = pygame.math.Vector2(0, 0)
        self.movement_speed = 6
        self.moving = False

        # Sprites
        self.setup_nodes()
        self.setup_level_selector()

    def setup_nodes(self):
        """Create and place the nodes."""
        self.nodes = pygame.sprite.Group()
        for index, node in enumerate(levels.values()):
            if index <= self.end_level:
                node_sprite = Node(node['node_pos'], True, self.movement_speed, node['node_graphics'])
                self.nodes.add(node_sprite)
            else:
                node_sprite = Node(node['node_pos'], False, self.movement_speed, node['node_graphics'])
                self.nodes.add(node_sprite)

    def draw_paths(self):
        """Draw the lines joining the nodes together."""
        points = [node['node_pos'] for index, node in enumerate(levels.values()) if index <= self.end_level + 1]
        pygame.draw.lines(self.display_surface, '#daab76', False, points, 6)

    def setup_level_selector(self):
        """Create the level selector sprite."""
        self.level_selector = pygame.sprite.GroupSingle()
        level_selector_sprite = LevelSelector(self.nodes.sprites()[self.current_level].rect.center)
        self.level_selector.add(level_selector_sprite)

    def update_level_selector(self):
        """Update the level selector."""
        if self.moving and self.movement_direction:
            self.level_selector.sprite.pos += self.movement_direction * self.movement_speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.target_rect.collidepoint(self.level_selector.sprite.pos):
                self.moving = False
                self.movement_direction = pygame.math.Vector2(0, 0)

    def get_input(self):
        """Get the input from the devices and move the level selector around."""
        gamepad = controllers[self.gamepad]  # controllers is a value defined in settings
        controller_lb = False
        controller_rb = False
        controller_a = False
        for controller in self.controllers.values():
            if controller.get_button(gamepad['buttons']['LB']):
                controller_lb = True
            elif controller.get_button(gamepad['buttons']['RB']):
                controller_rb = True
            elif controller.get_button(gamepad['buttons']['A']):
                controller_a = True
        keys = pygame.key.get_pressed()
        if not self.moving:
            if (keys[pygame.K_LEFT] or controller_lb) and self.current_level > self.first_level:
                self.movement_direction = self.get_movement_data(False)
                self.current_level -= 1
                self.moving = True
            elif (keys[pygame.K_RIGHT] or controller_rb) and self.current_level < self.end_level:
                self.movement_direction = self.get_movement_data(True)
                self.current_level += 1
                self.moving = True
            elif (keys[pygame.K_SPACE] or controller_a):
                self.create_level(self.current_level)

    def get_movement_data(self, next):
        """Create start and end vectors for the level selector.

        Arguments:
        next -- if this flag is set to True the vector will be generated based on the next node position.
        """
        start_vector = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        if next:
            end_vector = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end_vector = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)
        return (end_vector - start_vector).normalize()

    def run(self):
        """Run the level selector, update and draw everything (must be called every frame)."""
        self.display_surface.blit(self.background, (0, 0))
        self.get_input()
        self.update_level_selector()
        self.level_selector.update()
        self.draw_paths()
        self.nodes.update()
        self.nodes.draw(self.display_surface)
        self.level_selector.draw(self.display_surface)
