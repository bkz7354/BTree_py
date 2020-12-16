#!/usr/bin/env python3
import pygame as pg
import animation as ani
import box
import draw_module as draw
import GUI_module as GUI
import colors as col
from connector import Connector
from VisBTree import VisBtree
import random as rnd
import copy

min_int = 0
max_int = 9999

def get_sample(sample_size):
    res = []
    for _ in range(sample_size):
        res.append(rnd.randint(min_int, max_int))
    return res

def select_random(val_list, n):
    list_copy = val_list.copy()
    rnd.shuffle(list_copy)
    return list_copy[0:n]


def main():
    quit_flag = False
    pg.init()

    screen = pg.display.set_mode((1200, 800))
    GUI_manager = GUI.InterfaceManager(screen, 'pygame_theme.json') 

    clock = pg.time.Clock()

    ani_manager = ani.AnimationManager()
    box_manager = box.BoxManager()
    connector = Connector(ani_manager, box_manager)

    tree = VisBtree(3, connector)
    tree_contents = []

    while not quit_flag:
        time_delta = clock.tick(60) / 1000.0
        ani_manager.update(time_delta*GUI_manager.get_speed())
        

        for event in pg.event.get():
            GUI_manager.process_event(event)
            if event.type == pg.QUIT:
                quit_flag = True
            elif event.type == GUI.INSERT_EVENT:
                tree.insert(event.value)
                tree_contents.append(event.value)
            elif event.type == GUI.REMOVE_EVENT:
                if event.value in tree_contents:
                    tree.remove(event.value)
                    tree_contents.remove(event.value)
            elif event.type == GUI.INSERT_RNG_EVENT:
                for x in get_sample(event.value):
                    tree.insert(x)
                    tree_contents.append(x)
            elif event.type == GUI.REMOVE_RNG_EVENT:
                for x in select_random(tree_contents, event.value):
                    tree.remove(x)
                    tree_contents.remove(x)

        draw.persp.change_focus(*GUI_manager.get_mouse_move())

        screen.fill(col.LIGHT_PURPLE)
        draw.draw_objects(box_manager.nodes, box_manager.values, box_manager.connections, screen)
        GUI_manager.update_and_draw(time_delta)
        pg.display.update()
    
    


if __name__ == "__main__":
    main()