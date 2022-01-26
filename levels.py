import random

menu = ['data/menu_fon/0 (1).jpg', '-', 1500, 900, 0, 0, 0, 0, [], [], 'menu', False, False, False, [],
        'data/sounds/menu_music.mp3']

level_1 = ['data/cave/', 'data/cave/cave_coll.png', 4500, 1400, 300, 0, 0, 500, [],
           [[0, 1310, 4500, 300], [1040, 1080, 580, 500], [1790, 780, 400, 700], [2400, 1180, 720, 450]], 'level_1',
           False, False, False,
           [[3810, 1240, 60, 60, 'data/fire_shards_anim/', 'level_2']],
           'data/sounds/level_music1.mp3']

level_2 = ['data/fire_world/', 'data/fire_world/fire_world_coll.png', 7437, 2597, 0, 0, 0, 1100, [
    ['heart', 4500, 1800, 50, 50, 'data/heart_anim/0.png'],
    ['heart', 7100, 1777, 50, 50, 'data/heart_anim/0.png'],
    ['heart', 660, 1110, 50, 50, 'data/heart_anim/0.png'],
    ['walker', 800, 2200, 150, 200, 120, 'data/anim_walker/', 5, -4],
    ['bullet_shooter', 1670, 1600, 150, 150, 20, 'data/anim_bullet_s/', 'left', 6, 2],
    ['walker', 1300, 700, 150, 200, 120, 'data/anim_walker/', 5, -4],
    ['walker', 2500, 1150, 150, 150, 10, 'data/anim_flyer/', 0, 7],
    ['walker', 3550, 2200, 80, 120, 80, 'data/anim_walker/', 5, -5],
    ['walker', 3550, 2200, 80, 120, 80, 'data/anim_walker/', 5, 5],
    ['walker', 3200, 1800, 150, 150, 10, 'data/anim_flyer/', 0, -5],
    ['walker', 5800, 2200, 150, 200, 10, 'data/anim_walker/', 5, -5],
    ['walker', 5800, 2200, 150, 200, 10, 'data/anim_walker/', 5, 5],
    ['walker', 6600, 2200, 150, 200, 10, 'data/anim_walker/', 5, -5],
    ['push', 7200, 1050, 150, 200, 10, 'data/anim_push/', 5],
    ['bullet_shooter', 7300, 1610, 150, 150, 20, 'data/anim_bullet_s/', 'right', 8, 3]],

           [[0, 2450, 7500, 500], [0, 1720, 520, 100], [220, 2220, 510, 500], [850, 1940, 600, 100],
            [1480, 1540, 170, 350], [1580, 1750, 650, 150], [2000, 2220, 270, 400], [1730, 2400, 770, 400],
            [2510, 1930, 200, 150], [2700, 1540, 450, 1000], [2700, 1500, 200, 200], [910, 1370, 450, 100],
            [550, 1170, 250, 100], [630, 1120, 120, 100], [1050, 850, 150, 200], [1130, 930, 700, 100],
            [1700, 710, 130, 300], [2110, 1120, 330, 100], [2110, 1020, 60, 200], [2140, 1060, 100, 70],
            [3130, 1900, 260, 600], [4400, 2330, 440, 390], [4380, 1870, 450, 100], [4960, 2100, 400, 100],
            [5080, 2300, 350, 250], [5250, 1950, 380, 600], [5750, 1760, 330, 80], [6100, 1950, 300, 80],
            [6150, 1500, 300, 80], [5700, 1310, 300, 80], [6470, 2160, 350, 100], [6120, 2350, 320, 200],
            [6280, 1120, 500, 150], [6580, 1020, 230, 260], [6990, 1820, 500, 1000], [6850, 1320, 600, 100]],
           'level_2', True, False, False,
           [[7200, 1250, 70, 70, 'data/light_shards_anim/', 'level_3']], 'data/sounds/level_music2.mp3']

level_3 = ['data/lightnings_world/', 'data/lightnings_world/lightnings_coll.png', 5000, 1500, 300, 0, 0, 500,
           [['bullet_shooter', 3850, 1100, 150, 100, 40, 'data/anim_bullet_s/', 'right', 8, 1],
            ['bullet_shooter', 4850, 1290, 150, 100, 40, 'data/anim_bullet_s/', 'right', 9, 1],
            ['walker', 1800, 700, 130, 70, 10, 'data/anim_mouse/', 5, -5],
            ['walker', 1900, 700, 130, 70, 10, 'data/anim_mouse/', 5, 5],
            ['walker', 2000, 700, 130, 70, 10, 'data/anim_mouse/', 5, -4],
            ['walker', 1800, 700, 130, 70, 10, 'data/anim_mouse/', 5, 3],
            ['walker', 1850, 700, 130, 70, 10, 'data/anim_mouse/', 5, 8],
            ['push', 1800, 600, 150, 200, 60, 'data/anim_push/', 2],
            ['push', 1800, 600, 150, 200, 60, 'data/anim_push/', 3]],
           [[0, 1450, 5000, 300], [0, 1180, 330, 100], [3969, 1150, 350, 100], [3270, 885, 450, 100],
            [2900, 650, 200, 280], [1600, 770, 1300, 150], [1500, 640, 190, 200], [778, 610, 550, 100],
            [0, 430, 540, 150]], 'level_3', False, True, False,
           [[100, 350, 60, 60, 'data/time_shards_anim/', 'level_4']],
           'data/sounds/level_music3.mp3']

level_4 = ['data/ice_world/', 'data/ice_world/ice_coll.png', 5000, 1500, 300, 0, 0, 500,
           [['heart', 4800, 1270, 50, 50, 'data/heart_anim/0.png'],
            ['bullet_shooter', 700, 550, 150, 100, 40, 'data/anim_bullet_s/', 'roof', 3, 1],
            ['bullet_shooter', 900, 550, 150, 100, 40, 'data/anim_bullet_s/', 'roof', 6, 1],
            ['bullet_shooter', 1100, 550, 150, 100, 40, 'data/anim_bullet_s/', 'roof', 4, 1],
            ['bullet_shooter', 1300, 550, 150, 100, 40, 'data/anim_bullet_s/', 'roof', 5, 1],
            ['bullet_shooter', 1500, 500, 150, 100, 40, 'data/anim_bullet_s/', 'roof', 7, 1],
            ['laser_shooter', 3390, 1030, 100, 70, 30, 'data/anim_laser/', 'l'],
            ['laser_shooter', 3900, 800, 100, 70, 30, 'data/anim_laser/', 'l']],
           [[0, 1470, 5100, 200], [0, 400, 1670, 50], [1920, 670, 460, 100], [2650, 700, 470, 100],
            [2150, 1375, 200, 100], [2237, 1330, 500, 300], [2700, 1170, 1000, 600], [3520, 920, 700, 680],
            [4200, 1150, 400, 680], [4600, 1320, 450, 300]], 'level_4', False, False, True,
           [[100, 350, 60, 60, 'data/max_shards_anim/', 'level_5']],
           'data/sounds/level_music4.mp3']

level_5 = ['data/forest/', 'data/forest/forest_coll.png', 4500, 1400, 300, 0, 0, 500,
           [['final_boss', 4000, 650, 500, 600, 1100, 'data/boss_anim/0.png']],
           [[0, 1300, 5000, 300], [1680, 1000, 390, 400], [2200, 750, 430, 700], [3100, 1030, 350, 120]], 'level_5',
           True, True, True,
           [],
           'data/sounds/level_music5.mp3']

level_6 = ['data/end/', 'data/end/end_coll.png', 2200, 1000, 300, 0, 0, 100,
           [],
           [[0, 850, 5000, 300]], 'level_6',
           True, True, True,
           [],
           'data/sounds/level_music6.mp3']

levels_di = {'menu': menu, 'level_1': level_1, 'level_2': level_2, 'level_3': level_3, 'level_4': level_4,
             'level_5': level_5, 'level_6': level_6}
print(random.randrange(0, 1))
#  fon, size_x, size_y, hero_x, hero_y, space_x, space_y, enemies, cubes
