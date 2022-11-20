from weapons import MagicalWeapon, Projectile

"""This file defines the magical weapons."""
__all__ = ['StarterStaff']

class StarterStaff(MagicalWeapon):
    def __init__(self):
        self.name = "Starter Staff"
        self.description = "The staff beginners use to learn about magic. Now it's all yours!"
        self.icon_path = './assets/weapon/starter_staff.png'
        self.level = 1
        self.damage = {1: 1}
        self.cooldown = 500
        self.power = 125
        self.max_power = 125
        self.range = 384
        self.speed = 9
        self.cost = 1
        self.projectile_image = './assets/weapon/basic_fireball.png'
        super().__init__(self.name, self.description, self.icon_path, self.level, self.damage, self.cooldown, self.power, self.max_power, self.range, self.speed, self.cost, self.projectile_image)

    def on_impact(self, kill, pos, facing_right, level_class):
        if kill:
            level_class.player.sprite.heal(0.05*self.level)
        start_x = (level_class.start_x - pos[0]) * -1
        new_projectile = Projectile(self.projectile_image, pos, self.speed, facing_right, start_x, False)
        level_class.magical_sprites.add(new_projectile)
