#!/usr/bin/env python3
import pygame as pg
import animation as ani
import box
import draw_module as draw


def main():
    quit_flag = False
    pg.init()

    screen = pg.display.set_mode((1600, 1000))

    clock = pg.time.Clock()

    
    ani_manager = ani.AnimationManager()
    box_manager = box.BoxManager()

    node = box_manager.new_node()
    ani_manager.queue_animation(node.move([4, 4]))
    for x in range(4):
        ani_manager.queue_animation(node.insert_value(0, box_manager.new_value(x)))


    while not quit_flag:
        time_delta = clock.tick(60) / 1000.0
        ani_manager.update(time_delta)


        screen.fill((0,0,0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_flag = True

        draw.draw_list(box_manager.boxes, screen)
        pg.display.update()


if __name__ == "__main__":
    main()