"""This file defines the weapon classes."""

class Weapon:
    """The basic weapon class."""
    def __init__(self, name, icon_path, animation, damage, cooldown):
        """Initialize the weapon attributes.

        Arguments:
        name -- the weapon name
        icon_path -- the path to the weapon icon
        animation -- the folder with the player weapon animation
        damage -- the damage the weapon deals
        cooldown -- the cooldown time
        """
        self.name = name
        self.icon_path = icon_path
        self.animation = animation
        self.damage = damage
        self.cooldown = cooldown

class MeleeWeapon(Weapon):
    """The basic melee weapon class."""
    def __init__(self, name, icon_path, animation, damage, cooldown, range, height, offset, animation_speed):
        """Initialize the melee weapon attributes.

        Arguments:
        name -- the weapon name
        icon_path -- the path to the weapon icon
        animation -- the folder with the player weapon animation
        damage -- the damage the weapon deals
        cooldown -- the cooldown time
        range -- the range the weapon has
        height -- the height of the weapon sprite
        offset -- the offset from the top of the player
        animation_speed -- the speed of the player weapon animation
        """
        self.range = range
        self.height = height
        self.offset = offset
        self.animation_speed = animation_speed
        super().__init__(name, icon_path, animation, damage, cooldown)
