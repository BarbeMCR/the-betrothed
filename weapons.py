import pygame

"""This file defines the weapon classes."""

class Weapon:
    """The basic weapon class."""
    def __init__(self, name, icon_path, level, damage, cooldown):
        """Initialize the weapon attributes.

        Arguments:
        name -- the weapon name
        icon_path -- the path to the weapon icon
        level -- the weapon level
        damage -- the damage the weapon deals
        cooldown -- the cooldown time
        """
        self.name = name
        self.icon_path = icon_path
        self.level = level
        self.damage = damage
        self.cooldown = cooldown

class MeleeWeapon(Weapon):
    """The basic melee weapon class."""
    def __init__(self, name, icon_path, level, damage, cooldown, range, height, offset, animation, animation_speed):
        """Initialize the melee weapon attributes.

        Arguments:
        name -- the weapon name
        icon_path -- the path to the weapon icon
        level -- the weapon level
        damage -- the damage the weapon deals
        cooldown -- the cooldown time
        range -- the range of the weapon
        height -- the height of the weapon sprite
        offset -- the offset from the top of the player
        animation -- the folder with the player weapon animation
        animation_speed -- the speed of the player weapon animation
        """
        self.range = range
        self.height = height
        self.offset = offset
        self.animation = animation
        self.animation_speed = animation_speed
        super().__init__(name, icon_path, level, damage, cooldown)

class RangedWeapon(Weapon):
    """The basic ranged weapon class."""
    def __init__(self, name, icon_path, level, damage, cooldown, range, speed, projectile, projectile_type):
        """Initialize the ranged weapon attributes.

        Arguments:
        name -- the weapon name
        icon_path -- the path to the weapon icon
        level -- the weapon level
        damage -- the damage the weapon deals
        cooldown -- the cooldown time
        range -- the range of the weapon
        speed -- the speed at which the projectiles travel (in pixels per second)
        projectile -- the projectile pack class
        projectile_type -- the type of the projectile pack
        """
        self.range = range
        self.speed = speed
        self.projectile = projectile
        self.projectile_type = projectile_type
        super().__init__(name, icon_path, level, damage, cooldown)

class RangedProjectilePack:
    """The basic ranged projectile pack class."""
    def __init__(self, name, image, count):
        """Initialize the ranged projectile pack attributes.

        Arguments:
        name -- the name of the projectile pack
        image -- the projectile image path
        count -- the number of projectiles per pack
        """
        self.name = name
        self.image = image
        self.count = count

class Projectile(pygame.sprite.Sprite):
    """The projectile class."""
    def __init__(self, image, pos, speed, facing_right, start_x):
        """Initialize the projectile.

        Arguments:
        image -- the path to the projectile image
        pos -- the position at which the sprite spawns
        speed -- the speed at which the sprite travels
        facing_right -- whether the player is facing right when the projectile spawns
        start_x -- the starting absolute X position
        """
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = speed
        self.facing_right = facing_right
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
        self.start_x = start_x

    def update(self, shift):
        """Update the projectile.

        Arguments:
        shift -- the camera shift
        """
        self.rect.x += shift
        if self.facing_right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
