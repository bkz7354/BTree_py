import pygame as pg
import box as box_mod

pg.init()
font = pg.font.SysFont("Times new Roman", 12)

def get_rect(box):
    scale = 80

    pos = box.pos
    if box.parent != None:
        pos = [box.parent.pos[0] + box.pos[0], box.parent.pos[1] + box.pos[1]]

    pos = [int(scale*(x - box.padding/2)) for x in pos]
    size = [int(scale*(x + box.padding)) for x in box.size]

    return pos, size


def draw_single(box, surface):
    pos, size = get_rect(box)

    if type(box) == box_mod.ValueBox:
        pg.draw.rect(surface, box.color, pos+size)
        #text = font.render(str(box.value), False, (255, 0, 0))
        #surface.blit(text, coords[0]+box.padding*box.size, coords[1]+box.padding*box.size)
    else:
        pg.draw.rect(surface, box.color, pos+size)


def draw_list(boxes, surface):
    for key, box in boxes.items():
        draw_single(box, surface)
