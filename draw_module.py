import pygame as pg
import box as box_mod
import numpy as np

pg.init()
font = pg.font.SysFont("Times new Roman", 30)
SCALE = 80

def get_rect(box):
    

    pos = box.pos
    if box.parent != None:
        pos = pos + box.parent.pos

    pos =  ((pos - box.padding/2)*SCALE).astype(int)
    size = ((box.size + box.padding)*SCALE).astype(int)

    return pos, size

def render_value(size, value):
    text = str(value).zfill(4)

    surf = font.render(text, True, (0, 0, 0))
    surf_size = np.array(surf.get_size())

    scale = min(size/surf_size)
    return pg.transform.scale(surf, (surf_size*scale).astype(int))

def draw_value_box(box, surface):
    pos, size = get_rect(box)

    pg.draw.rect(surface, box.color, pos.tolist() + size.tolist())
    pg.draw.rect(surface, (0,0,0), pos.tolist() + size.tolist(), 2)

    text_surf = render_value(size*0.8, box.value)
    text_size = np.array(text_surf.get_size())
    surface.blit(text_surf, (pos + (size-text_size)/2).astype(int))

def draw_node_box(box, surface):
    pos, size = get_rect(box)

    pg.draw.rect(surface, box.color, pos.tolist() + size.tolist())

def draw_single(box, surface):
    if type(box) == box_mod.ValueBox:
        draw_value_box(box, surface)
    else:
        draw_node_box(box, surface)


def draw_list(boxes, surface):
    for key, box in boxes.items():
        draw_single(box, surface)
