import pygame
from data import levels

"""This file defines the level selection screen."""

class Node(pygame.sprite.Sprite):
    """The level node class."""
    def __init__(self, pos, unlocked, movement_speed):
        """Create the node surface and the target rect inside the node.

        Arguments:
        pos -- the position of the node
        unlocked -- the node will appear as unlocked only if this flag is set to True
        movement_speed -- the speed at which the level selector travels
        """
        super().__init__()
        self.image = pygame.Surface((100, 80))
        if unlocked:
            self.image.fill('grey')
        else:
            self.image.fill('red')
        self.rect = self.image.get_rect(center = pos)
        self.target_rect = pygame.Rect(self.rect.centerx - (movement_speed / 2), self.rect.centery - (movement_speed / 2), movement_speed, movement_speed)

class LevelSelector(pygame.sprite.Sprite):
    """The level selector class."""
    def __init__(self, pos):
        """Create the level selector.

        Arguments:
        pos -- the level selector initial position
        """
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface((20, 20))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        """Update the level selector."""
        self.rect.center = self.pos

class World:
    """The world builder class."""
    def __init__(self, start_level, end_level, display_surface, create_level):
        """Setup the level selector screen, the movement of the cursor and the sprites.

        Arguments:
        start_level -- the level to place the cursor on
        end_level -- the highest level the player can select
        display_surface -- the screen
        create_level -- the method for building the level
        """
        # Setup
        self.display_surface = display_surface
        self.end_level = end_level
        self.current_level = start_level
        self.create_level = create_level

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
                node_sprite = Node(node['node_pos'], True, self.movement_speed)
                self.nodes.add(node_sprite)
            else:
                node_sprite = Node(node['node_pos'], False, self.movement_speed)
                self.nodes.add(node_sprite)

    def draw_paths(self):
        """Draw the lines joining the nodes together."""
        points = [node['node_pos'] for index, node in enumerate(levels.values()) if index <= self.end_level + 1]
        pygame.draw.lines(self.display_surface, 'grey', False, points, 6)

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
        """Get the input from the keyboard and move the level selector around."""
        keys = pygame.key.get_pressed()
        if not self.moving:
            if keys[pygame.K_LEFT] and self.current_level > 0:
                self.movement_direction = self.get_movement_data(False)
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_RIGHT] and self.current_level < self.end_level:
                self.movement_direction = self.get_movement_data(True)
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
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
        self.get_input()
        self.update_level_selector()
        self.level_selector.update()
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.level_selector.draw(self.display_surface)
