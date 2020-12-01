import pygame as pg
import box as box_mod
import numpy as np
import colors as col

pg.init()
font = pg.font.SysFont("Times new Roman", 30)
SCALE = 80

class Perspective:
    def __init__(self):
        pass

    def scale(self, vect):
        # scales vector from relative to scrren coords
        pass

    def shift(self, vect):
        # shifts vector in relative coordinates
        pass

    def get_coord(self):
        # gets screen coordinates from relative (shift + scale)
        pass

    def get_box(pos, size):
        # scales and shifts the box
        pass

def scale_coords(coords):
    return (coords*SCALE).astype(int)

def get_rect(box):
    pos = box.pos
    if box.parent != None:
        pos = pos + box.parent.pos

    pos =  pos - box.padding/2
    size = box.size + box.padding

    return scale_coords(pos), scale_coords(size)

def render_value(size, value):
    text = str(value).zfill(4)

    surf = font.render(text, True, (0, 0, 0))
    surf_size = np.array(surf.get_size())

    scale = min(size/surf_size)
    return pg.transform.scale(surf, (surf_size*scale).astype(int))

def draw_value_box(box, surface):
    pos, size = get_rect(box)

    pg.draw.rect(surface, box.color, pos.tolist() + size.tolist())
    pg.draw.rect(surface, col.BLACK, pos.tolist() + size.tolist(), 2)

    text_surf = render_value(size*0.8, box.value)
    text_size = np.array(text_surf.get_size())
    surface.blit(text_surf, (pos + (size-text_size)/2).astype(int))

def draw_connection(conn, surface):
    beg = scale_coords(conn.beg)
    end = scale_coords(conn.get_end())

    pg.draw.aaline(surface, conn.color, beg, end, 2)

def draw_node_box(box, surface):
    pos, size = get_rect(box)

    pg.draw.rect(surface, box.color, pos.tolist() + size.tolist())


def draw_objects(nodes, values, connections, surface):
    for _, box in nodes.items():
        draw_node_box(box, surface)
    for _, conn in connections.items():
        draw_connection(conn, surface)
    for _, box in values.items():
        draw_value_box(box, surface)
