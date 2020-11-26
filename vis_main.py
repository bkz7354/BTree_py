#!/usr/bin/env python3
import pygame as pg
import animation as ani
import box

def main():
    pg.init()

    screen = pg.display.set_mode((1600, 1000))

    clock = pg.time.Clock()

    quit_flag = False
    ani_manager = ani.AnimationManager()
    ani_manager.start_animation(ani.BaseAnimation(1), lambda: print("First animation done"))
    ani_manager.chain_animations([ani.BaseAnimation(1), ani.BaseAnimation(0.5)], lambda: print("Chain of animations done"))

    while not quit_flag:
        time_delta = clock.tick(60) / 1000.0
        ani_manager.update(time_delta)

        screen.fill((0,0,0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_flag = True

        pg.display.update()


if __name__ == "__main__":
    main()