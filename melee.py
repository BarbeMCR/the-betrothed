from weapons import MeleeWeapon

"""This file defines the melee weapons."""
__all__ = ['IronKnife']

class IronKnife(MeleeWeapon):
    def __init__(self):
        self.name = "Iron Knife"
        self.description = "A basic weapon made of iron used to stab enemies to death."
        self.icon_path = './assets/weapon/iron_knife.png'
        self.level = 1
        self.damage = {1: 1}
        self.cooldown = 400
        self.durability = 250
        self.max_durability = 250
        self.range = 32
        self.height = 48
        self.offset = 32
        self.animation = '/ironknife'
        self.animation_speed = 0.042
        super().__init__(self.name, self.description, self.icon_path, self.level, self.damage, self.cooldown, self.durability, self.max_durability, self.range, self.height, self.offset, self.animation, self.animation_speed)
