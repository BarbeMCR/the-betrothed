from weapons import MagicalWeapon, Projectile

"""This file defines the magical weapons."""
__all__ = ['StarterStaff']

class StarterStaff(MagicalWeapon):
    def __init__(self):
        self.name = "Starter Staff"
        self.description = "The staff used by beginners to learn about magic. Now it's all yours!"
        self.attack_desc = "Generates a new fireball clone after the original hits an enemy. If an original fireball kills an enemy, the player is healed by 0.05 HP per level."
        self.icon_path = './assets/weapon/starter_staff.png'
        self.level = 1
        self.damage = {
            1: 1,
            2: 2.5,
            3: 4,
            4: 6,
            5: 8
        }
        self.cooldown = 500
        self.power = 75
        self.max_power = 75
        self.max_power_step = 15
        self.range = 384
        self.speed = 9
        self.cost = 1
        self.projectile_image = './assets/weapon/basic_fireball.png'
        self.refill_cost = 1
        super().__init__(self.name, self.description, self.attack_desc, self.icon_path, self.level, self.damage, self.cooldown, self.power, self.max_power, self.max_power_step, self.range, self.speed, self.cost, self.projectile_image, self.refill_cost)

    def on_impact(self, kill, pos, facing_right, level_class):
        if kill:
            level_class.player.sprite.heal(0.05*self.level)
        start_x = (level_class.start_x - pos[0]) * -1
        new_projectile = Projectile(self.projectile_image, pos, self.speed, facing_right, start_x, False)
        level_class.magical_sprites.add(new_projectile)
