from weapons import MeleeWeapon

"""This file defines the melee weapons."""
__all__ = ['IronKnife']

class IronKnife(MeleeWeapon):
    def __init__(self):
        self.name = "Iron Knife"
        self.icon_path = './assets/weapon/iron_knife.png'
        self.animation = '/ironknife'
        self.damage = 1
        self.cooldown = 400
        self.range = 32
        self.height = 48
        self.offset = 32
        self.animation_speed = 0.042
        super().__init__(self.name, self.icon_path, self.animation, self.damage, self.cooldown, self.range, self.height, self.offset, self.animation_speed)
