"""This file contains all the information about the levels."""

chapter_1a = {
    'node_pos': (140, 200),
    'node_graphics': './assets/world/chapter1a.png',
    'unlock': 1,
    'enable_water': True,
    'enable_mountains': True,
    'horizon': 7,
    'background': './leveldata/empty72.csv',
    'barriers': './leveldata/chapter1a/chapter1a_barriers.csv',
    'borders': './leveldata/chapter1a/chapter1a_borders.csv',
    'buildings': './leveldata/empty72.csv',
    'enemies': './leveldata/chapter1a/chapter1a_enemies.csv',
    'energy': './leveldata/chapter1a/chapter1a_energy.csv',
    'grass': './leveldata/chapter1a/chapter1a_grass.csv',
    'roofs': './leveldata/empty72.csv',
    'roots': './leveldata/empty72.csv',
    'setup': './leveldata/chapter1a/chapter1a_setup.csv',
    'terrain': './leveldata/chapter1a/chapter1a_terrain.csv',
    'trees': './leveldata/chapter1a/chapter1a_trees.csv',
    'windows': './leveldata/empty72.csv'
}
chapter_1b = {
    'node_pos': (390, 200),
    'node_graphics': './assets/world/chapter1b.png',
    'unlock': 2,
    'enable_water': True,
    'enable_mountains': True,
    'horizon': 6,
    'background': './leveldata/empty144.csv',
    'barriers': './leveldata/chapter1b/chapter1b_barriers.csv',
    'borders': './leveldata/chapter1b/chapter1b_borders.csv',
    'buildings': './leveldata/chapter1b/chapter1b_buildings.csv',
    'enemies': './leveldata/chapter1b/chapter1b_enemies.csv',
    'energy': './leveldata/chapter1b/chapter1b_energy.csv',
    'grass': './leveldata/chapter1b/chapter1b_grass.csv',
    'roofs': './leveldata/chapter1b/chapter1b_roofs.csv',
    'roots': './leveldata/chapter1b/chapter1b_roots.csv',
    'setup': './leveldata/chapter1b/chapter1b_setup.csv',
    'terrain': './leveldata/chapter1b/chapter1b_terrain.csv',
    'trees': './leveldata/chapter1b/chapter1b_trees.csv',
    'windows': './leveldata/chapter1b/chapter1b_windows.csv'
}
chapter_2a = {
    'node_pos': (720, 200),
    'node_graphics': './assets/world/chapter2a.png',
    'unlock': 2,
    'enable_water': False,
    'enable_mountains': True,
    'horizon': 7,
    'background': './leveldata/chapter2a/chapter2a_background.csv',
    'barriers': './leveldata/chapter2a/chapter2a_barriers.csv',
    'borders': './leveldata/chapter2a/chapter2a_borders.csv',
    'buildings': './leveldata/chapter2a/chapter2a_buildings.csv',
    'enemies': './leveldata/chapter2a/chapter2a_enemies.csv',
    'energy': './leveldata/chapter2a/chapter2a_energy.csv',
    'grass': './leveldata/chapter2a/chapter2a_grass.csv',
    'roofs': './leveldata/chapter2a/chapter2a_roofs.csv',
    'roots': './leveldata/chapter2a/chapter2a_roots.csv',
    'setup': './leveldata/chapter2a/chapter2a_setup.csv',
    'terrain': './leveldata/chapter2a/chapter2a_terrain.csv',
    'trees': './leveldata/chapter2a/chapter2a_trees.csv',
    'windows': './leveldata/chapter2a/chapter2a_windows.csv'
}

levels = {
    0: {
        0: chapter_1a,
        1: chapter_1b,
        2: chapter_2a,
        'background': './assets/world/part1.png'
    }
}

# chapter_1a = {'node_pos': (140, 180), 'content': "This is Chapter I - A", 'unlock': 1}
# chapter_1b = {'node_pos': (390, 180), 'content': "This is Chapter I - B", 'unlock': 1}  # 'unlock': 2
# chapter_2a = {'node_pos': (720, 180), 'content': "This is Chapter II - A", 'unlock': 3}
# chapter_2b = {'node_pos': (900, 180), 'content': "This is Chapter II - B", 'unlock': 4}
# chapter_2c = {'node_pos': (1070, 180), 'content': "This is Chapter II - C", 'unlock': 5}
# chapter_3a = {'node_pos': (1070, 330), 'content': "This is Chapter III - A", 'unlock': 6}
# chapter_3b = {'node_pos': (900, 330), 'content': "This is Chapter III - B", 'unlock': 7}
# chapter_3c = {'node_pos': (720, 330), 'content': "This is Chapter III - C", 'unlock': 7}
# chapter_4 = (250, 330)
# chapter_5 = (250, 480)
# chapter_6a,b,c = (x, 480)  x = 720, 900, 1070
# chapter_7a,b,c, = (x, 630)  x = 1070, 900, 720
# chapter_8a,b = (x, 630)  x = 390, 140

# levels = {
    # 0: chapter_1a,
    # 1: chapter_1b,
    # 2: chapter_2a,
    # 3: chapter_2b,
    # 4: chapter_2c,
    # 5: chapter_3a,
    # 6: chapter_3b,
    # 7: chapter_3c
# }
