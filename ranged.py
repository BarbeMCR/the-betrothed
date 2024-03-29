from weapons import RangedWeapon, RangedProjectilePack

"""This file defines the ranged weapons."""
__all__ = ['MakeshiftBow']

class MakeshiftBow(RangedWeapon):
    def __init__(self):
        self.name = "Makeshift Bow"
        self.description = "A basic bow made from makeshift materials ready to clear enemies out of your way."
        self.icon_path = './assets/weapon/makeshift_bow.png'
        self.level = 1
        self.damage = {
            1: 1,
            2: 2,
            3: 3,
            4: 4.5,
            5: 6
        }
        self.cooldown = 300
        self.range = 256
        self.speed = 12
        self.projectile = FlintArrows()
        self.projectile_type = FlintArrows
        super().__init__(self.name, self.description, self.icon_path, self.level, self.damage, self.cooldown, self.range, self.speed, self.projectile, self.projectile_type)

class FlintArrows(RangedProjectilePack):
    def __init__(self):
        self.name = "Flint Arrows"
        self.image = './assets/weapon/flint_arrow.png'
        self.count = 50
        super().__init__(self.name, self.image, self.count)
