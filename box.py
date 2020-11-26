import pygame as pg
import uuid
from animation import BaseAnimation


VALUEBOX_SIZE = (1.0, 1.0)
BOXMOVE_DURATION = 1

class Box:
    def __init__(self, manager, pos_, size_=VALUEBOX_SIZE, parent=None, padding=0):
        self.u_id = uuid.uuid1()
        self.size = size_
        self.pos=pos_
        self.color=(100, 100, 100)
        self.parent = parent
        self.padding = padding
        self.manager

    def draw(self, screen):
        pg.draw.rect(screen, self.color, (self.pos, (50, 50)))

    def move(self, pos):
        pass

class ValueBox(Box):
    def __init__(self, manager, pos, val, parent=None):
        Box.__init__(self, manager, pos, parent=parent)
        self.color = (200, 200, 200)
        self.value = val


class NodeBox(Box):
    def __init__(self, manager, pos, parent=None):
        Box.__init__(self, manager, pos, parent=parent)
        self.contained_values = []
        self.adjust_size()

    def adjust_size(self):
        self.size[0] = len(self.contained_values)

    def insert_value(self, pos, value_box):
        self.contained_values.append(value_box)
        value_box.parent = self
        self.adjust_size()
    

class BoxManager:
    def __init__(self, animation_manager):
        self.animation = animation_manager
        self.boxes = {}
    
    def new_node(self):
        res = NodeBox(self, (0, 0))
        self.boxes[res.u_id] = res
        return res
    
    def new_value(self, val):
        res = ValueBox(self, (0,0), )

class MoveBoxAnimation(BaseAnimation):
    def __init__(self, box, pos1, pos2, duration=BOXMOVE_DURATION)
        BaseAnimation.__init__(self, duration)
        self.fr = pos1
        self.to = pos2
        self.box = box

    def update_objects(self):
        box.pos = [t*x2 + (1-t)*x2 for x1, x2 in zip(pos1, pos2)]

