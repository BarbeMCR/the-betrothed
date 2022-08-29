import shelve
from ranged import MakeshiftBow

"""This file defines several functions used to upgrade savefiles to a higher version."""

def upgrade(version, savefile_path):
    """Redirect to the appropriate upgrade function.

    Arguments:
    version -- the version to upgrade from
    savefile_path -- the path to the savefile
    """
    if 7210 <= version <= 8289: version = _upgrade_013_to_015(savefile_path)

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
