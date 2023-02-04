import pygame
from text import render
from misc import import_folder
from settings import controllers, tile_size
from weapons import MeleeWeapon, RangedWeapon, MagicalWeapon

"""This file contains the inventory."""

class Inventory:
    """The inventory class."""
    def __init__(self, display_surface, game):
        """Setup the inventory screen.

        Arguments:
        display_surface -- the screen
        game -- the Game class
        """
        # Setup
        self.display_surface = display_surface
        self.game = game
        self.controllers = self.game.controller.controllers
        self.gamepad = self.game.gamepad
        self.background = pygame.image.load('./assets/menu/menu_bg.png').convert_alpha()
        self.cursor = import_folder('./assets/menu/inventory/cursor')
        self.page_cursor = pygame.image.load('./assets/menu/inventory/page_cursor.png').convert_alpha()
        self.object_section_border = pygame.image.load('./assets/menu/inventory/object_tools_border.png').convert_alpha()
        self.object_box_border = pygame.image.load('./assets/menu/inventory/object_box_border.png').convert_alpha()
        self.font_file = './font.ttf'
        self.page_name_font = pygame.font.Font(self.font_file, 10)
        self.object_name_font = pygame.font.Font(self.font_file, 18)
        self.object_description_font = pygame.font.Font(self.font_file, 12)
        self.object_level_font = pygame.font.Font(self.font_file, 15)
        self.selection_mode = True
        self.selected_object = 0
        self.action_cursor = pygame.image.load('./assets/menu/cursor_settings.png').convert_alpha()
        self.action_cursor_pos = 0
        self.actions = []
        self.action_names = []
        self.cursor_pos = 0
        self.cursor_row = 0
        self.offset = 0
        self.page = 0
        self.pages = ["Weapons", "Selection"]
        self.names = ['weapons']
        self.page_icons = [
            './assets/menu/inventory/weapons_icon.png',
            './assets/menu/inventory/selection_icon.png'
        ]
        self._load_page_icons()
        self.selection_hotspots = {
            'melee': (125, 150),
            'ranged': (250, 150),
            'magical': (375, 150)
            #'helmet': (125, 275)
            #'chestplate': (250, 275)
            #'gloves': (375, 275)
            #'pants': (125, 400)
            #'boots': (250, 400)
            #'shield': (375, 400)
            #'special': (580, 150)
            #'item': (580, 275)
            #'ability': (580, 400)
        }
        self.selection_cursor_pos = 'melee'
        self.selection_names = {
            'melee': "Melee weapon",
            'ranged': "Ranged weapon",
            'magical': "Magical weapon"
            #'helmet': "Helmet"
            #'chestplate': "Chestplate"
            #'gloves': "Gloves"
            #'pants': "Pants"
            #'boots': "Boots"
            #'shield': "Shield"
            #'special': "Special weapon"
            #'item': "Item"
            #'ability': "Ability"
        }
        self.cursor_animation_speed = 10  # Animation frames per second
        self.cursor_animation_frame_index = 0
        self.now = 0  # This is a dummy value
        self.gen_time = pygame.time.get_ticks()

        # SFX
        self.sfx = pygame.mixer.Sound('./assets/audio/sfx/menu_select.ogg')

        # Input initialization
        self.keydown_left = False
        self.keydown_right = False
        self.keydown_up = False
        self.keydown_down = False
        self.keydown_space = False
        self.keydown_tab = False
        self.keydown_ctrl = False
        self.keydown_esc = False
        self.buttondown_left = False
        self.buttondown_right = False
        self.buttondown_up = False
        self.buttondown_down = False
        self.buttondown_lb = False
        self.buttondown_rb = False
        self.buttondown_a = False
        self.buttondown_b = False

    def _load_page_icons(self):
        """Create surfaces by overwriting file names in 'self.page_icons'."""
        for index, filename in enumerate(self.page_icons):
            self.page_icons[index] = pygame.image.load(filename).convert_alpha()

    def display_objects(self):
        """Display the inventory objects."""
        object_col = 0
        object_row = 0
        for obj in self.game.inventory[self.names[self.page]][5*self.offset:5*self.offset+15]:
            obj_surf = pygame.image.load(obj.icon_path).convert_alpha()
            obj_surf = pygame.transform.scale_by(obj_surf, 1.5)
            obj_x = 80 + 125*object_col
            obj_y = 150 + 125*object_row
            obj_rect = obj_surf.get_rect(center=(obj_x, obj_y))
            self.display_surface.blit(obj_surf, obj_rect)
            object_col += 1
            if object_col >= 5:
                object_col = 0
                object_row += 1

    def display_cursor(self):
        """Draw and animate the cursor."""
        if self.selection_mode:
            self.cursor_animation_frame_index += self.cursor_animation_speed*self.game.level.delta
            if self.cursor_animation_frame_index >= len(self.cursor):
                self.cursor_animation_frame_index = 0
            cursor_surf = self.cursor[int(self.cursor_animation_frame_index)]
        else:
            cursor_surf = pygame.image.load('./assets/menu/inventory/cursor/cursor1.png').convert_alpha()
        cursor_x = 80 + 125*self.cursor_pos
        cursor_y = 150 + 125*self.cursor_row
        cursor_rect = cursor_surf.get_rect(center=(cursor_x, cursor_y))
        self.display_surface.blit(cursor_surf, cursor_rect)

    def display_selection_objects(self):
        """Display objects in selection."""
        for obj, hotspot in self.selection_hotspots.items():
            obj_surf = pygame.image.load(self.game.selection[obj].icon_path).convert_alpha()
            obj_surf = pygame.transform.scale_by(obj_surf, 1.5)
            obj_rect = obj_surf.get_rect(center=hotspot)
            self.display_surface.blit(obj_surf, obj_rect)

    def display_selection_name(self):
        """Display the name of the currently selected object below the icon."""
        selection_title = self.object_level_font.render("Currently hovering over:", False, 'white')
        selection_title_rect = selection_title.get_rect(topleft=(705, 222))
        self.display_surface.blit(selection_title, selection_title_rect)
        selection_name = self.object_description_font.render(self.selection_names[self.selection_cursor_pos], False, 'white')
        selection_name_rect = selection_name.get_rect(topleft=(705, selection_title_rect.bottom+10))
        self.display_surface.blit(selection_name, selection_name_rect)

    def display_selection_cursor(self):
        """Draw and animate the cursor in selection."""
        if self.selection_mode:
            self.cursor_animation_frame_index += self.cursor_animation_speed*self.game.level.delta
            if self.cursor_animation_frame_index >= len(self.cursor):
                self.cursor_animation_frame_index = 0
            cursor_surf = self.cursor[int(self.cursor_animation_frame_index)]
        else:
            cursor_surf = pygame.image.load('./assets/menu/inventory/cursor/cursor1.png').convert_alpha()
        cursor_rect = cursor_surf.get_rect(center=self.selection_hotspots[self.selection_cursor_pos])
        self.display_surface.blit(cursor_surf, cursor_rect)

    def display_page_cursor(self):
        """Draw the page cursor."""
        cursor_x = 80 + 125*self.page
        cursor_rect = self.page_cursor.get_rect(center=(cursor_x, 40))
        self.display_surface.blit(self.page_cursor, cursor_rect)

    def display_page_icons(self):
        """Draw the page icons."""
        for index, icon in enumerate(self.page_icons):
            icon_x = 80 + 125*index
            icon_rect = icon.get_rect(midtop=(icon_x, 15))
            self.display_surface.blit(icon, icon_rect)

    def display_page_name(self):
        """Display the current page name below the icon."""
        page_name = self.page_name_font.render(self.pages[self.page], False, 'white')
        page_name_x = 80 + 125*self.page
        page_name_rect = page_name.get_rect(midbottom=(page_name_x, 65))
        self.display_surface.blit(page_name, page_name_rect)

    def display_object_section(self):
        """Display everything in the object section."""
        level_table = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
        level_color_table = {1: '#c0c0c0', 2: '#00ff66', 3: '#17599c', 4: '#5c35ae', 5: '#a62d19'}
        object_section_border_rect = self.object_section_border.get_rect(midright=(1265, 352))
        self.display_surface.blit(self.object_section_border, object_section_border_rect)
        object_box_border_rect = self.object_box_border.get_rect(topleft=object_section_border_rect.topleft+pygame.math.Vector2(20, 20))
        self.display_surface.blit(self.object_box_border, object_box_border_rect)
        if not self.selection_mode:
            if self.page == 0:
                obj = self.game.inventory[self.names[self.page]][self.selected_object]
            elif self.page == 1:
                obj = self.game.selection[self.selection_cursor_pos]
            # Icon
            object_icon = pygame.image.load(obj.icon_path).convert_alpha()
            object_icon = pygame.transform.scale_by(object_icon, 2)
            object_icon_rect = object_icon.get_rect(center=object_box_border_rect.center)
            self.display_surface.blit(object_icon, object_icon_rect)
            # Name
            object_name = self.object_name_font.render(obj.name, False, 'white')
            object_name_rect = object_name.get_rect(topleft=object_box_border_rect.topright+pygame.math.Vector2(25, 0))
            self.display_surface.blit(object_name, object_name_rect)
            # Description
            object_description_rect = pygame.Rect(object_box_border_rect.topright+pygame.math.Vector2(25, 40), (360, 120))
            render(obj.description, self.object_description_font, self.display_surface, object_description_rect, 'white', -2)
            if isinstance(obj, MeleeWeapon):  # Melee weapons
                # Level
                level = self.object_level_font.render(f"Level {level_table[obj.level]}", False, level_color_table[obj.level])
                level_rect = level.get_rect(topleft=object_box_border_rect.bottomleft+pygame.math.Vector2(0, 20))
                self.display_surface.blit(level, level_rect)
                # Damage
                damage = self.object_description_font.render(f"Damage: {obj.damage[obj.level]} HP", False, 'white')
                damage_rect = damage.get_rect(topleft=level_rect.bottomleft+pygame.math.Vector2(0, 10))
                self.display_surface.blit(damage, damage_rect)
                # Cooldown
                cooldown = self.object_description_font.render(f"Cooldown: {format(obj.cooldown/1000, '.2f')} s", False, 'white')
                cooldown_rect = cooldown.get_rect(topleft=damage_rect.bottomleft+pygame.math.Vector2(0, 5))
                self.display_surface.blit(cooldown, cooldown_rect)
                # Durability
                if obj.durability/obj.max_durability < 0.1: durability_color = '#bb0000'
                elif 0.1 <= obj.durability/obj.max_durability < 0.25: durability_color = 'gold'
                else: durability_color = 'white'
                durability = self.object_description_font.render(f"Durability: {obj.durability} / {obj.max_durability}", False, durability_color)
                durability_rect = durability.get_rect(topleft=cooldown_rect.bottomleft+pygame.math.Vector2(0, 5))
                self.display_surface.blit(durability, durability_rect)
                # Range
                obj_range = self.object_description_font.render(f"Range: {format(obj.range/tile_size, '.1f')} bl", False, 'white')
                obj_range_rect = obj_range.get_rect(topleft=durability_rect.bottomleft+pygame.math.Vector2(0, 5))
                self.display_surface.blit(obj_range, obj_range_rect)
            elif isinstance(obj, RangedWeapon):  # Ranged weapons
                # Level
                level = self.object_level_font.render(f"Level {level_table[obj.level]}", False, level_color_table[obj.level])
                level_rect = level.get_rect(topleft=object_box_border_rect.bottomleft+pygame.math.Vector2(0, 20))
                self.display_surface.blit(level, level_rect)
                # Damage
                damage = self.object_description_font.render(f"Damage: {obj.damage[obj.level]} HP", False, 'white')
                damage_rect = damage.get_rect(topleft=level_rect.bottomleft+pygame.math.Vector2(0, 10))
                self.display_surface.blit(damage, damage_rect)
                # Cooldown
                cooldown = self.object_description_font.render(f"Cooldown: {format(obj.cooldown/1000, '.2f')} s", False, 'white')
                cooldown_rect = cooldown.get_rect(topleft=damage_rect.bottomleft+pygame.math.Vector2(0, 5))
                self.display_surface.blit(cooldown, cooldown_rect)
                # Range
                obj_range = self.object_description_font.render(f"Range: {format(obj.range/tile_size, '.1f')} bl", False, 'white')
                obj_range_rect = obj_range.get_rect(topleft=cooldown_rect.bottomleft+pygame.math.Vector2(0, 5))
                self.display_surface.blit(obj_range, obj_range_rect)
                # Speed
                speed = self.object_description_font.render(f"Speed: {format(obj.speed*60/tile_size, '.2f')} bl/s", False, 'white')
                speed_rect = speed.get_rect(topleft=obj_range_rect.bottomleft+pygame.math.Vector2(0, 5))
                self.display_surface.blit(speed, speed_rect)
                # Projectile info
                projectile = self.object_description_font.render(f"Projectile: {obj.projectile.name} ({obj.projectile.count} remaining)", False, 'white')
                projectile_rect = projectile.get_rect(topleft=speed_rect.bottomleft+pygame.math.Vector2(0, 5))
                self.display_surface.blit(projectile, projectile_rect)
            elif isinstance(obj, MagicalWeapon):  # Magical weapons
                # Level
                level = self.object_level_font.render(f"Level {level_table[obj.level]}", False, level_color_table[obj.level])
                level_rect = level.get_rect(topleft=object_box_border_rect.bottomleft+pygame.math.Vector2(0, 20))
                self.display_surface.blit(level, level_rect)
                # Damage
                damage = self.object_description_font.render(f"Damage: {obj.damage[obj.level]} HP", False, 'white')
                damage_rect = damage.get_rect(topleft=level_rect.bottomleft+pygame.math.Vector2(0, 10))
                self.display_surface.blit(damage, damage_rect)
                # Cooldown
                cooldown = self.object_description_font.render(f"Cooldown: {format(obj.cooldown/1000, '.2f')} s", False, 'white')
                cooldown_rect = cooldown.get_rect(topleft=damage_rect.bottomleft+pygame.math.Vector2(0, 5))
                self.display_surface.blit(cooldown, cooldown_rect)
                # Power
                if obj.power/obj.max_power < 0.1: power_color = '#bb0000'
                elif 0.1 <= obj.power/obj.max_power < 0.25: power_color = 'gold'
                else: power_color = 'white'
                power = self.object_description_font.render(f"Power: {obj.power} / {obj.max_power}", False, power_color)
                power_rect = power.get_rect(topleft=cooldown_rect.bottomleft+pygame.math.Vector2(0, 5))
                self.display_surface.blit(power, power_rect)
                # Range
                obj_range = self.object_description_font.render(f"Range: {format(obj.range/tile_size, '.1f')} bl", False, 'white')
                obj_range_rect = obj_range.get_rect(topleft=power_rect.bottomleft+pygame.math.Vector2(0, 5))
                self.display_surface.blit(obj_range, obj_range_rect)
                # Speed
                speed = self.object_description_font.render(f"Speed: {format(obj.speed*60/tile_size, '.2f')} bl/s", False, 'white')
                speed_rect = speed.get_rect(topleft=obj_range_rect.bottomleft+pygame.math.Vector2(0, 5))
                self.display_surface.blit(speed, speed_rect)
                # Cost
                cost = self.object_description_font.render(f"Cost: {obj.cost} EP", False, 'gold')
                cost_rect = cost.get_rect(topleft=speed_rect.bottomleft+pygame.math.Vector2(0, 5))
                self.display_surface.blit(cost, cost_rect)
                # Attack info
                attack_text = self.object_description_font.render("Attack info:", False, 'white')
                attack_rect = attack_text.get_rect(topleft=level_rect.topright+pygame.math.Vector2(150, 0))
                self.display_surface.blit(attack_text, attack_rect)
                attack_info_rect = pygame.Rect(level_rect.topright+pygame.math.Vector2(150, 30), (290, 300))
                render(obj.attack_desc, self.object_description_font, self.display_surface, attack_info_rect, 'white', -2)
        else:
            inventory_text = self.object_name_font.render("Inventory", False, 'white')
            inventory_text_rect = inventory_text.get_rect(topleft=object_box_border_rect.topright+pygame.math.Vector2(25, 0))
            self.display_surface.blit(inventory_text, inventory_text_rect)
            instruction_text_rect = pygame.Rect(object_box_border_rect.topright+pygame.math.Vector2(25, 40), (360, 120))
            render("Select an object to view its data and possible actions.", self.object_description_font, self.display_surface, instruction_text_rect, 'white', -2)

    def get_actions(self):
        """Get the right actions for the currently selected object."""
        obj = self.game.inventory[self.names[self.page]][self.selected_object]
        if isinstance(obj, (MeleeWeapon, MagicalWeapon)):
            #[return, equip, upgrade, repair, move_to_top]
            self.actions = [self.return_to_selection, self.equip, self.move_to_top]
            self.action_names = ["Cancel", "Equip", "Move to Top"]
        elif isinstance(obj, RangedWeapon):
            #[return, equip, upgrade, give_prj, move_to_top]
            self.actions = [self.return_to_selection, self.equip, self.give_projectiles, self.move_to_top]
            self.action_names = ["Cancel", "Equip", "Give Projectiles", "Move to Top"]

    def get_selection_actions(self):
        """Get the right actions for the currently selected object in selection."""
        obj = self.game.selection[self.selection_cursor_pos]
        if isinstance(obj, (MeleeWeapon, MagicalWeapon)):
            #[return, upgrade, repair]
            self.actions = [self.return_to_selection]
            self.action_names = ["Cancel"]
        elif isinstance(obj, RangedWeapon):
            #[return, upgrade]
            self.actions = [self.return_to_selection]
            self.action_names = ["Cancel"]

    def display_action_text(self):
        """Display the text for the object actions."""
        y = 480
        for text in self.action_names:
            text_surf = self.object_name_font.render(text, False, 'white')
            text_rect = text_surf.get_rect(topleft=(750, y))
            self.display_surface.blit(text_surf, text_rect)
            y += 32

    def display_action_cursor(self):
        """Display the action cursor."""
        action_cursor_y = 465 + 32*self.action_cursor_pos
        action_cursor_rect = self.action_cursor.get_rect(topright=(750, action_cursor_y))
        self.display_surface.blit(self.action_cursor, action_cursor_rect)

    def return_to_selection(self):
        """Return to selection mode."""
        self.selection_mode = True

    def equip(self):
        """Equip an object."""
        obj = self.game.inventory[self.names[self.page]][self.selected_object]
        inv_list = self.game.inventory[self.names[self.page]]
        sel = self.game.selection
        if isinstance(obj, MeleeWeapon):
            inv_list[self.selected_object], sel['melee'] = sel['melee'], obj
        elif isinstance(obj, RangedWeapon):
            inv_list[self.selected_object], sel['ranged'] = sel['ranged'], obj
        elif isinstance(obj, MagicalWeapon):
            inv_list[self.selected_object], sel['magical'] = sel['magical'], obj
        self.selection_mode = True

    def move_to_top(self):
        """Move an object to the top of the inventory."""
        inv_list = self.game.inventory[self.names[self.page]]
        inv_list.insert(0, inv_list.pop(self.selected_object))
        self.selection_mode = True

    def give_projectiles(self):
        """Give 10 ranged projectiles to the selected ranged weapon."""
        if isinstance(self.game.inventory[self.names[self.page]][self.selected_object].projectile, self.game.selection['ranged'].projectile_type):
            if self.game.inventory[self.names[self.page]][self.selected_object].projectile.count >= 10:
                self.game.inventory[self.names[self.page]][self.selected_object].projectile.count -= 10
                self.game.selection['ranged'].projectile.count += 10

    def get_input(self):
        """Get the input from the devices and do the correct actions."""
        gamepad = controllers[self.gamepad]
        controller_left = False
        controller_right = False
        controller_up = False
        controller_down = False
        controller_lb = False
        controller_rb = False
        controller_a = False
        controller_b = False
        for controller in self.controllers.values():
            if self.gamepad == 'ps4' or self.gamepad == 'switch_pro':
                if controller.get_button(gamepad['buttons']['LEFT']):
                    controller_left = True
                elif controller.get_button(gamepad['buttons']['RIGHT']):
                    controller_right = True
                elif controller.get_button(gamepad['buttons']['UP']):
                    controller_up = True
                elif controller.get_button(gamepad['buttons']['DOWN']):
                    controller_down = True
            else:
                if controller.get_hat(0) == gamepad['hat']['LEFT']:
                    controller_left = True
                elif controller.get_hat(0) == gamepad['hat']['RIGHT']:
                    controller_right = True
                elif controller.get_hat(0) == gamepad['hat']['UP']:
                    controller_up = True
                elif controller.get_hat(0) == gamepad['hat']['DOWN']:
                    controller_down = True
            if controller.get_button(gamepad['buttons']['LB']):
                controller_lb = True
            elif controller.get_button(gamepad['buttons']['RB']):
                controller_rb = True
            if controller.get_button(gamepad['buttons']['A']):
                controller_a = True
            if controller.get_button(gamepad['buttons']['B']):
                controller_b = True
        keys = pygame.key.get_pressed()
        if self.page == 0:
            if self.selection_mode:
                if (keys[pygame.K_LEFT] or controller_left) and not (self.keydown_left or self.buttondown_left):
                    self.cursor_pos -= 1
                    if self.cursor_pos < 0:
                        self.cursor_pos = 4
                        self.cursor_row -= 1
                        if self.cursor_row < 0:
                            self.cursor_row = 0
                            self.offset -= 1
                            if self.offset < 0:
                                self.cursor_pos = 0
                                self.cursor_row = 0
                                self.offset = 0
                    self.sfx.play()
                    self.keydown_left = True
                    self.buttondown_left = True
                elif (keys[pygame.K_RIGHT] or controller_right) and not (self.keydown_right or self.buttondown_right):
                    self.cursor_pos += 1
                    if self.cursor_pos >= 5:
                        self.cursor_pos = 0
                        self.cursor_row += 1
                        if self.cursor_row >= 3:
                            self.cursor_row = 2
                            self.offset += 1
                    if 5*self.offset+5*self.cursor_row+self.cursor_pos >= len(self.game.inventory[self.names[self.page]]):
                        self.cursor_row = (len(self.game.inventory[self.names[self.page]])-1) // 5
                        self.cursor_pos = (len(self.game.inventory[self.names[self.page]])-1) % 5
                        if self.cursor_row >= 3:
                            self.offset = self.cursor_row - 2
                            self.cursor_row = 2
                    self.sfx.play()
                    self.keydown_right = True
                    self.buttondown_right = True
                elif (keys[pygame.K_UP] or controller_up) and not (self.keydown_up or self.buttondown_up):
                    self.cursor_row -= 1
                    if self.cursor_row < 0:
                        self.cursor_row = 0
                        self.offset -= 1
                        if self.offset < 0:
                            self.offset = 0
                    self.sfx.play()
                    self.keydown_up = True
                    self.buttondown_up = True
                elif (keys[pygame.K_DOWN] or controller_down) and not (self.keydown_down or self.buttondown_down):
                    #self.cursor_row += 1
                    #if self.cursor_row >= 3:
                    #    self.cursor_row = 2
                    #    self.offset += 1
                    #if 5*self.offset+5*self.cursor_row+self.cursor_pos >= len(self.game.inventory[self.names[self.page]]):
                    #    self.cursor_row = (len(self.game.inventory[self.names[self.page]])-1) // 5
                    #    self.cursor_pos = (len(self.game.inventory[self.names[self.page]])-1) % 5
                    #    if self.cursor_row >= 3:
                    #        self.offset = self.cursor_row - 2
                    #        self.cursor_row = 2
                    if 5*self.offset+5*self.cursor_row+self.cursor_pos+5 < len(self.game.inventory[self.names[self.page]]):
                        self.cursor_row +=1
                        if self.cursor_row >= 3:
                            self.cursor_row = 2
                            self.offset += 1
                    self.sfx.play()
                    self.keydown_down = True
                    self.buttondown_down = True
                if ((keys[pygame.K_LCTRL] and keys[pygame.K_TAB]) or controller_lb) and not (self.keydown_tab or self.buttondown_lb):
                    self.page -= 1
                    if self.page < 0:
                        self.page = len(self.pages) - 1
                    self.cursor_pos = 0
                    self.cursor_row = 0
                    self.offset = 0
                    self.cursor_animation_frame_index = 0
                    self.sfx.play()
                    self.keydown_ctrl = True
                    self.keydown_tab = True
                    self.buttondown_lb = True
                elif (keys[pygame.K_TAB] or controller_rb) and not (self.keydown_tab or self.buttondown_rb or self.keydown_ctrl):
                    self.page += 1
                    if self.page >= len(self.pages):
                        self.page = 0
                    self.cursor_pos = 0
                    self.cursor_row = 0
                    self.offset = 0
                    self.cursor_animation_frame_index = 0
                    self.sfx.play()
                    self.keydown_tab = True
                    self.buttondown_rb = True
                if (keys[pygame.K_SPACE] or controller_a) and not (self.keydown_space or self.buttondown_a):
                    self.selection_mode = False
                    self.selected_object = 5*self.offset + 5*self.cursor_row + self.cursor_pos
                    self.sfx.play()
                    self.keydown_space = True
                    self.buttondown_a = True
                if (keys[pygame.K_ESCAPE] or controller_b) and not (self.keydown_esc or self.buttondown_b):
                    self.sfx.play()
                    self.keydown_esc = True
                    self.buttondown_b = True
                    self.game.level.resume_level()
            else:
                if (keys[pygame.K_UP] or controller_lb) and not (self.keydown_up or self.buttondown_lb):
                    self.action_cursor_pos -= 1
                    if self.action_cursor_pos < 0:
                        self.action_cursor_pos = 0
                    self.sfx.play()
                    self.keydown_up = True
                    self.buttondown_lb = True
                elif (keys[pygame.K_DOWN] or controller_rb) and not (self.keydown_down or self.buttondown_rb):
                    self.action_cursor_pos += 1
                    if self.action_cursor_pos >= len(self.actions):
                        self.action_cursor_pos = len(self.actions) - 1
                    self.sfx.play()
                    self.keydown_down = True
                    self.buttondown_rb = True
                if (keys[pygame.K_SPACE] or controller_a) and not (self.keydown_space or self.buttondown_a):
                    self.sfx.play()
                    self.keydown_space = True
                    self.buttondown_a = True
                    self.actions[self.action_cursor_pos]()
                    self.action_cursor_pos = 0
                if (keys[pygame.K_ESCAPE] or controller_b) and not (self.keydown_esc or self.buttondown_b):
                    self.sfx.play()
                    self.keydown_esc = True
                    self.buttondown_b = True
                    self.game.level.resume_level()
        elif self.page == 1:
            if self.selection_mode:
                if (keys[pygame.K_LEFT] or controller_left) and not (self.keydown_left or self.buttondown_left):
                    selection_list = list(self.selection_hotspots)
                    if selection_list.index(self.selection_cursor_pos)-1 < 0:
                        self.selection_cursor_pos = selection_list[1]
                    self.selection_cursor_pos = selection_list[selection_list.index(self.selection_cursor_pos) - 1]
                    self.sfx.play()
                    self.keydown_left = True
                    self.buttondown_left = True
                elif (keys[pygame.K_RIGHT] or controller_right) and not (self.keydown_right or self.buttondown_right):
                    selection_list = list(self.selection_hotspots)
                    if selection_list.index(self.selection_cursor_pos)+1 >= len(selection_list):
                        self.selection_cursor_pos = selection_list[len(selection_list)-2]
                    self.selection_cursor_pos = selection_list[selection_list.index(self.selection_cursor_pos) + 1]
                    self.sfx.play()
                    self.keydown_right = True
                    self.buttondown_right = True
                if ((keys[pygame.K_LCTRL] and keys[pygame.K_TAB]) or controller_lb) and not (self.keydown_tab or self.buttondown_lb):
                    self.page -= 1
                    if self.page < 0:
                        self.page = len(self.pages) - 1
                    self.cursor_pos = 0
                    self.cursor_row = 0
                    self.offset = 0
                    self.cursor_animation_frame_index = 0
                    self.sfx.play()
                    self.keydown_ctrl = True
                    self.keydown_tab = True
                    self.buttondown_lb = True
                elif (keys[pygame.K_TAB] or controller_rb) and not (self.keydown_tab or self.buttondown_rb or self.keydown_ctrl):
                    self.page += 1
                    if self.page >= len(self.pages):
                        self.page = 0
                    self.cursor_pos = 0
                    self.cursor_row = 0
                    self.offset = 0
                    self.cursor_animation_frame_index = 0
                    self.sfx.play()
                    self.keydown_tab = True
                    self.buttondown_rb = True
                if (keys[pygame.K_SPACE] or controller_a) and not (self.keydown_space or self.buttondown_a):
                    self.selection_mode = False
                    self.sfx.play()
                    self.keydown_space = True
                    self.buttondown_a = True
                if (keys[pygame.K_ESCAPE] or controller_b) and not (self.keydown_esc or self.buttondown_b):
                    self.sfx.play()
                    self.keydown_esc = True
                    self.buttondown_b = True
                    self.game.level.resume_level()
            else:
                if (keys[pygame.K_UP] or controller_lb) and not (self.keydown_up or self.buttondown_lb):
                    self.action_cursor_pos -= 1
                    if self.action_cursor_pos < 0:
                        self.action_cursor_pos = 0
                    self.sfx.play()
                    self.keydown_up = True
                    self.buttondown_lb = True
                elif (keys[pygame.K_DOWN] or controller_rb) and not (self.keydown_down or self.buttondown_rb):
                    self.action_cursor_pos += 1
                    if self.action_cursor_pos >= len(self.actions):
                        self.action_cursor_pos = len(self.actions) - 1
                    self.sfx.play()
                    self.keydown_down = True
                    self.buttondown_rb = True
                if (keys[pygame.K_SPACE] or controller_a) and not (self.keydown_space or self.buttondown_a):
                    self.sfx.play()
                    self.keydown_space = True
                    self.buttondown_a = True
                    self.actions[self.action_cursor_pos]()
                    self.action_cursor_pos = 0
                if (keys[pygame.K_ESCAPE] or controller_b) and not (self.keydown_esc or self.buttondown_b):
                    self.sfx.play()
                    self.keydown_esc = True
                    self.buttondown_b = True
                    self.game.level.resume_level()

        if not keys[pygame.K_LEFT]: self.keydown_left = False
        if not keys[pygame.K_RIGHT]: self.keydown_right = False
        if not keys[pygame.K_UP]: self.keydown_up = False
        if not keys[pygame.K_DOWN]: self.keydown_down = False
        if not keys[pygame.K_SPACE]: self.keydown_space = False
        if not keys[pygame.K_TAB]: self.keydown_tab = False
        if not keys[pygame.K_LCTRL]: self.keydown_ctrl = False
        if not keys[pygame.K_ESCAPE]: self.keydown_esc = False
        if not controller_left: self.buttondown_left = False
        if not controller_right: self.buttondown_right = False
        if not controller_up: self.buttondown_up = False
        if not controller_down: self.buttondown_down = False
        if not controller_lb: self.buttondown_lb = False
        if not controller_rb: self.buttondown_rb = False
        if not controller_a: self.buttondown_a = False
        if not controller_b: self.buttondown_b

    def run(self):
        self.now = pygame.time.get_ticks()
        self.display_surface.blit(self.background, (0, 0))
        self.display_page_icons()
        self.display_page_cursor()
        self.display_page_name()
        if self.now - self.gen_time >= 250:
            self.get_input()
        if self.page == 0:
            self.display_objects()
            self.display_cursor()
            self.display_object_section()
            if not self.selection_mode:
                self.get_actions()
                self.display_action_text()
                self.display_action_cursor()
        elif self.page == 1:
            self.display_selection_objects()
            self.display_selection_cursor()
            self.display_object_section()
            if not self.selection_mode:
                self.get_selection_actions()
                self.display_action_text()
                self.display_action_cursor()
            else:
                self.display_selection_name()
