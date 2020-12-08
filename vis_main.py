#!/usr/bin/env python3
import pygame as pg
import animation as ani
import box
import draw_module as draw
import colors as col
from connector import Connector
from VisBTree import VisBtree
import random as rnd

min_int = 0
max_int = 9999

def get_sample(sample_size):
    res = []
    for _ in range(sample_size):
        res.append(rnd.randint(min_int, max_int))
    return res

def main():
    quit_flag = False
    pg.init()

    screen = pg.display.set_mode((1600, 1000))

    clock = pg.time.Clock()

    ani_manager = ani.AnimationManager()
    box_manager = box.BoxManager()
    connector = Connector(ani_manager, box_manager)
    t = VisBtree(2, connector)
    box.BOXMOVE_DURATION = 0.1
    
    spd = 2
    samp = get_sample(20)
    print(samp)
    for i in samp: 
        t.insert(i)
    

    do1 = True
    while not quit_flag:
        time_delta = clock.tick(60) / 1000.0
        ani_manager.update(time_delta*spd)

        if not ani_manager.is_running() and do1:
            spd = 1.0
            rnd.shuffle(samp)
            while len(samp) > 0:
                t.remove(samp[0])
                del samp[0]
            do1 = False

        screen.fill(col.LIGHT_PURPLE)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_flag = True

        draw.draw_objects(box_manager.nodes, box_manager.values, box_manager.connections, screen)
        pg.display.update()
    
    


if __name__ == "__main__":
    main()