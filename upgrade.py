import shelve
from weapons import *
from melee import *
from ranged import *
from magical import *

"""This file defines several functions used to upgrade savefiles to a higher version."""

def upgrade(version, savefile_path):
    """Redirect to the appropriate upgrade function.

    Arguments:
    version -- the version to upgrade from
    savefile_path -- the path to the savefile
    """
    if 7210 <= version <= 8289: version = _upgrade_013_to_015(savefile_path)
    if 8290 <= version <= 11059: version = _upgrade_015_to_016(savefile_path)
    if 11060 <= version <= 11129: version = _upgrade_016_to_017(savefile_path)
    if 11130 <= version <= 11199: version = _upgrade_017_to_018(savefile_path)
    if 11200 <= version <= 102039: version = _upgrade_018_to_020(savefile_path)
    if 102040 <= version <= 103099: version = _upgrade_020_to_021(savefile_path)

def _upgrade_013_to_015(savefile_path):
    """Upgrade a 0.13 savefile to version 0.15.

    Arguments:
    savefile_path -- the path to the savefile
    """
    savefile = shelve.open(savefile_path, writeback=True)
    del savefile['first_level']
    savefile['selection']['melee'].level = 1
    savefile['selection']['melee'].damage = {1: 1}
    savefile['selection']['ranged'] = MakeshiftBow()
    savefile.close()
    return 8290

def _upgrade_015_to_016(savefile_path):
    """Upgrade a 0.15 savefile to version 0.16.

    Arguments:
    savefile_path -- the path to the savefile
    """
    savefile = shelve.open(savefile_path, writeback=True)
    savefile['health']['renzo'] = float(savefile['health']['renzo'])
    savefile.close()
    return 11060

def _upgrade_016_to_017(savefile_path):
    """Upgrade a 0.16 savefile to version 0.17.

    Arguments:
    savefile_path -- the path to the savefile
    """
    savefile = shelve.open(savefile_path, writeback=True)
    savefile['stamina'] = {'renzo': 1800}
    savefile.close()
    return 11130

def _upgrade_017_to_018(savefile_path):
    """Upgrade a 0.17 savefile to version 0.18.

    Arguments:
    savefile_path -- the path to the savefile
    """
    savefile = shelve.open(savefile_path, writeback=True)
    savefile['selection']['melee'].description = IronKnife().description
    savefile['selection']['melee'].durability = IronKnife().durability
    savefile['selection']['melee'].max_durability = IronKnife().max_durability
    savefile['selection']['ranged'].description = MakeshiftBow().description
    savefile['selection']['magical'] = StarterStaff()
    savefile.close()
    return 11200

def _upgrade_018_to_020(savefile_path):
    """Upgrade a 0.18 savefile to version 0.20.

    Arguments:
    savefile_path -- the path to the savefile
    """
    savefile = shelve.open(savefile_path, writeback=True)
    savefile['current_part'] = 1
    savefile['selection'] = {
        'melee': WoodenKnife(),
        'ranged': MakeshiftBow(),
        'magical': StarterStaff()
    }
    savefile['inventory'] = {
        'weapons': [
            IronKnife(),
            WoodenKnife(),
            MakeshiftBow(),
            StarterStaff(),
            IronKnife(),
            MakeshiftBow(),
            StarterStaff(),
            IronKnife(),
            WoodenKnife(),
            IronKnife(),
            IronKnife(),
            MakeshiftBow(),
            WoodenKnife(),
            IronKnife(),
            StarterStaff(),
            WoodenKnife(),
            WoodenKnife(),
            MakeshiftBow(),
            StarterStaff()
        ]
    }
    savefile.close()
    return 102040

def _upgrade_020_to_021(savefile_path):
    """Upgrade a 0.20 savefile to version 0.21.

    Arguments:
    savefile_path -- the path to the savefile
    """
    savefile = shelve.open(savefile_path, writeback=True)
    savefile['experience'] = {'renzo': 0}
    savefile['selection']['melee'].durability = type(savefile['selection']['melee'])().durability
    savefile['selection']['melee'].max_durability = type(savefile['selection']['melee'])().max_durability
    savefile['selection']['melee'].max_durability_step = type(savefile['selection']['melee'])().max_durability_step
    savefile['selection']['melee'].repair_cost = type(savefile['selection']['melee'])().repair_cost
    savefile['selection']['magical'].power = type(savefile['selection']['magical'])().power
    savefile['selection']['magical'].max_power = type(savefile['selection']['magical'])().max_power
    savefile['selection']['magical'].max_power_step = type(savefile['selection']['magical'])().max_power_step
    savefile['selection']['magical'].refill_cost = type(savefile['selection']['magical'])().refill_cost
    for obj_list in savefile['inventory'].values():
        for obj in obj_list:
            if isinstance(obj, MeleeWeapon):
                obj.durability = type(obj)().durability
                obj.max_durability = type(obj)().max_durability
                obj.max_durability_step = type(obj)().max_durability_step
                obj.repair_cost = type(obj)().repair_cost
            elif isinstance(obj, MagicalWeapon):
                obj.power = type(obj)().power
                obj.max_power = type(obj)().max_power
                obj.max_power_step = type(obj)().max_power_step
                obj.refill_cost = type(obj)().refill_cost
    savefile.close()
    return 103100
