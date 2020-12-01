#!/usr/bin/env python3
import pygame as pg
import animation as ani
import box
import draw_module as draw
import colors as col

def main():
    quit_flag = False
    pg.init()

    screen = pg.display.set_mode((1600, 1000))

    clock = pg.time.Clock()

    
    ani_manager = ani.AnimationManager()
    box_manager = box.BoxManager()

    node = box_manager.new_node()
    box_manager.set_root(node)
    ani_manager.queue_animation(node.move([4, 4]))
    for x in range(2):
        ani_manager.queue_animation(node.insert_value(0, box_manager.new_value(x)))

    node2 = box_manager.new_node()
    box_manager.connect_nodes(node, node2, 0)
    for x in range(3):
        ani_manager.queue_animation(node2.insert_value(0, box_manager.new_value(x)))
    ani_manager.queue_animation(node.insert_value(0, box_manager.new_value(x)))    


    while not quit_flag:
        if not ani_manager.is_running():
            ani_manager.queue_animation(box_manager.arrange_boxes([5, 2]))
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