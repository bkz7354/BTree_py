import pygame as pg
import box as box_mod
import numpy as np
import colors as col

INITIAL_SCALE = 50
INITIAL_SHIFT = np.array([-10, -5])


class Perspective:
    """
    The class that manages the conversion from coordinates used in box 
    module to screen coordinates 
    """
    def __init__(self, pos_c, scale_factor):
        self.pos_c = pos_c
        self.scale_factor = scale_factor

    def change_focus(self, dx_px, dy_px):
        new_pos = np.array([dx_px, dy_px]).astype(float)
        self.pos_c = self.pos_c - new_pos/self.scale_factor

    def change_zoom(self, new_scale):
        self.scale_factor = new_scale

    def scale(self, vect):
        return vect*self.scale_factor

    def shift(self, vect):
        return vect - self.pos_c

    def screen_coord(self, pos):
        return self.scale(self.shift(pos))

    def screen_box(self, box):
        pos = box.pos - box.padding*np.array([1,1])
        if box.parent is not None:
            pos += box.parent.pos

        size = box.size + 3*box.padding*np.array([1,1])

        return self.screen_coord(pos), self.scale(size)

persp = Perspective(INITIAL_SHIFT, INITIAL_SCALE)




def render_value(box_size, value):
    font = pg.font.SysFont("Times new Roman", 30)
    text = str(value).zfill(4)

    surf = font.render(text, True, (0, 0, 0))
    surf_size = np.array(surf.get_size())

    scale = min(box_size/surf_size)
    return pg.transform.scale(surf, (surf_size*scale).astype(int))

def draw_value_box(box, surface):
    pos, size = persp.screen_box(box)

    pg.draw.rect(surface, box.color, pos.tolist() + size.tolist())
    pg.draw.rect(surface, col.BLACK, pos.tolist() + size.tolist(), 2)

    text_surf = render_value(size*0.8, box.value)
    text_size = np.array(text_surf.get_size())
    surface.blit(text_surf, (pos + (size-text_size)/2).astype(int))

def draw_connection(conn, surface):
    end_coords = np.array([conn.beg + conn.parent.pos, conn.get_end()])
    beg, end = persp.screen_coord(end_coords)

    pg.draw.aaline(surface, conn.color, beg, end, 2)

def draw_node_box(box, surface):
    pos, size = persp.screen_box(box)

    pg.draw.rect(surface, box.color, pos.tolist() + size.tolist())


def draw_objects(nodes, values, connections, surface):
    for _, box in nodes.items():
        if box.display:
            draw_node_box(box, surface)
    for _, conn in connections.items():
        draw_connection(conn, surface)
    for _, box in values.items():
        if box.display:
            draw_value_box(box, surface)
