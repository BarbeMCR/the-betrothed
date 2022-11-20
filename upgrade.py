import shelve
from melee import IronKnife
from ranged import MakeshiftBow
from magical import StarterStaff

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
