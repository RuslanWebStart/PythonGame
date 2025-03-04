
# 🌲 🌊 🚁 🟩 🔥 🏥 ❤️ 'ВЕДРО' 🏦 ⛅ ⚡ 🏆
from pynput import keyboard
from map import Map
import time
import os
import json
from helicopter import Helicopter
from clouds import Clouds

TICK_SLEEP = 0.05
TREE_UPDATE = 50
CLOUDS_UPDATE = 100
FIRE_UPDATE = 100
MAP_W, MAP_H = 20, 10

tmp = Map(MAP_W, MAP_H)
clouds = Clouds(MAP_W, MAP_H)
helicopter = Helicopter(MAP_W, MAP_H)
tick = 1

MOVES = {'w':(-1, 0), 'd': (0, 1), 's': (1, 0), 'a': (0, -1)}
# f - сохранение, g - восстановление
def press_key(key):
    global helicopter, tick, clouds, tmp
    char = key.char.lower()

    # обработка движения
    if char in MOVES.keys():
        dx, dy = MOVES[char][0], MOVES[char][1]
        helicopter.move(dx, dy)

    # сохранение игры 
    elif char == 'f':
        data = {
            'helicopter': helicopter.export_data(),
            'clouds': clouds.export_data(),
            'tmp': tmp.export_data(),
            'tick': tick
            }
        with open('level.json', 'w') as lvl:
            json.dump(data, lvl)
            
    # загрузка игры 
    elif char == 'g':
        with open('level.json', 'r') as lvl:
            data = json.load(lvl)
            tick = data['tick'] or 1
            helicopter.import_data(data['helicopter'])
            tmp.import_data(data['tmp'])
            clouds.import_data(data['clouds'])

listener = keyboard.Listener(
    on_press = None,
    on_release = press_key,)
listener.start()




while True:
    os.system('cls')
    tmp.process_helicopter(helicopter, clouds)
    helicopter.prin_menu()
    tmp.print_map(helicopter, clouds)
    print('TICK', tick)
    tick += 1
    time.sleep(TICK_SLEEP)
    if (tick % TREE_UPDATE == 0):
        tmp.generate_tree()
    if (tick % FIRE_UPDATE == 0):
        tmp.update_fires()
    if (tick % CLOUDS_UPDATE == 0):
        clouds.update_clouds()
