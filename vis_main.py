#!/usr/bin/env python3
import pygame as pg
import animation as ani
import box
import draw_module as draw

quit_flag = False

def animation_loop(screen, clock, ani_manager, box_manager):
    global quit_flag

    while ani_manager.is_running() and not quit_flag:
        time_delta = clock.tick(60) / 1000.0
        ani_manager.update(time_delta)

        screen.fill((0,0,0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_flag = True


        draw.draw_list(box_manager.boxes, screen)
        pg.display.update()

def main():
    global quit_flag
    pg.init()

    screen = pg.display.set_mode((1600, 1000))

    clock = pg.time.Clock()

    
    ani_manager = ani.AnimationManager()
    box_manager = box.BoxManager(ani_manager)

    node = box_manager.new_node()
    node.move([4, 4])

    insert_list = [1, 2, 3]

    while not quit_flag:
        if(ani_manager.is_running):
            animation_loop(screen, clock, ani_manager, box_manager)
        time_delta = clock.tick(60) / 1000.0
        
        if len(insert_list) > 0:
            node.insert_value(0, box_manager.new_value(insert_list[0]))
            del insert_list[0]

        screen.fill((0,0,0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_flag = True

        draw.draw_list(box_manager.boxes, screen)
        pg.display.update()


if __name__ == "__main__":
    main()