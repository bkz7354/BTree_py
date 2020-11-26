import pygame as pg
import box.py

font = pg.font.SysFont("Times new Roman", 12)


def draw_single(box, surface):
    coords = box.pos
    if box.parent != None:
        coords = [box.parent.pos[0]+box.pos[0], box.parent.pos[1]+box.pos[1]]
    if type(box) == "ValueBox":
        pg.draw.rect(surface, box.color, coords, box.size, box.size)
        text = font.render(str(box.value), False, (255, 0, 0))
        surface.blit(text, coords[0]+box.padding*box.size, coords[1]+box.padding*box.size)
    else:
        pg.draw.rect(surface, box.color, coords, box.size*40, box.size*40)


def draw_list(boxes, surface):
    for i in range(boxes):
        draw_single(boxes[i], surface)
