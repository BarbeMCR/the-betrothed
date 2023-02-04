from weapons import MeleeWeapon

"""This file defines the melee weapons."""
__all__ = ['WoodenKnife', 'IronKnife']

class WoodenKnife(MeleeWeapon):
    def __init__(self):
        self.name = "Wooden Knife"
        self.description = "A makeshift weapon made of fresh wood. With enough patience, you can use this to stab enemies to their death."
        self.icon_path = './assets/weapon/wooden_knife.png'
        self.level = 1
        self.damage = {
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5
        }
        self.cooldown = 400
        self.durability = 100
        self.max_durability = 100
        self.range = 32
        self.height = 48
        self.offset = 32
        self.animation = '/woodenknife'
        self.animation_speed = 0.042
        super().__init__(self.name, self.description, self.icon_path, self.level, self.damage, self.cooldown, self.durability, self.max_durability, self.range, self.height, self.offset, self.animation, self.animation_speed)

class IronKnife(MeleeWeapon):
    def __init__(self):
        self.name = "Iron Knife"
        self.description = "The classic melee weapon. Handle with caution!"
        self.icon_path = './assets/weapon/iron_knife.png'
        self.level = 1
        self.damage = {
            1: 2,
            2: 4,
            3: 6.5,
            4: 9,
            5: 12
        }
        self.cooldown = 500
        self.durability = 300
        self.max_durability = 300
        self.range = 32
        self.height = 48
        self.offset = 32
        self.animation = '/ironknife'
        self.animation_speed = 0.042
        super().__init__(self.name, self.description, self.icon_path, self.level, self.damage, self.cooldown, self.durability, self.max_durability, self.range, self.height, self.offset, self.animation, self.animation_speed)
