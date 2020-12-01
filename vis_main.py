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
    for i in get_sample(100):
        t.insert(i)

    while not quit_flag:
        time_delta = clock.tick(60) / 1000.0
        ani_manager.update(time_delta)


        screen.fill(col.LIGHT_PURPLE)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_flag = True

        draw.draw_objects(box_manager.nodes, box_manager.values, box_manager.connections, screen)
        pg.display.update()
    
    


if __name__ == "__main__":
    main()