import pygame as pg
import uuid
from animation import BaseAnimation
from animation import AnimationManager

VALUEBOX_SIZE = [1.0, 1.0]
BOXMOVE_DURATION = 1

class Box:
    def __init__(self, manager, pos_, size_=VALUEBOX_SIZE, parent=None, padding=0):
        self.u_id = uuid.uuid1()
        self.size = size_
        self.pos=pos_
        self.color=(100, 100, 100)
        self.parent = parent
        self.padding = padding
        self.manager = manager

    def move(self, pos):
        self.manager.animation.start_animation(MoveBoxAnimation(self, self.pos, pos))

class ValueBox(Box):
    def __init__(self, manager, pos, val, parent=None):
        Box.__init__(self, manager, pos, parent=parent)
        self.color = (200, 200, 200)
        self.value = val


class NodeBox(Box):
    def __init__(self, manager, pos, parent=None):
        Box.__init__(self, manager, pos, parent=parent, padding=0.1)
        self.contained_values = []
        self.size[0] = 0

    def get_relative(self, pos):
        return [pos*VALUEBOX_SIZE[0], 0]

    def relative_from_absolute(self, abs_pos):
        return [xa - x0 for xa, x0 in zip(abs_pos, self.pos)]
    
    def shift_values(self, pos, shift):
        animation_list = []

        move_vect = [shift*VALUEBOX_SIZE[0], 0]
        for box in self.contained_values[pos:]:
            animation_list.append(MoveBoxAnimation(box, box.pos, [x + d for x, d in zip(box.pos, move_vect)]))
        self.size[0] += move_vect

        return animation_list

    def insert_value(self, pos, value_box):
        animation_manager = self.manager.animation
        
        value_box.parent = self
        value_box.pos = self.relative_from_absolute(value_box.pos)

        shiftlist = self.shift_values(pos, 1)

        def callback():
            self.contained_values.insert(pos, value_box)
            value_box.move(self.get_relative(pos))

        animation_manager.synchronous_animations(shiftlist, callback)
        



class BoxManager:
    def __init__(self, animation_manager):
        self.animation = animation_manager
        self.boxes = {}
    
    def new_node(self):
        res = NodeBox(self, [0, 0])
        self.boxes[res.u_id] = res
        return res
    
    def new_value(self, val):
        res = ValueBox(self, (0,0), val)

class MoveBoxAnimation(BaseAnimation):
    def __init__(self, box, pos_from, pos_to, duration=BOXMOVE_DURATION):
        BaseAnimation.__init__(self, duration)
        self.fr = pos_from
        self.to = pos_to
        self.box = box

    def update_objects(self):
        t = self.progress
        self.box.pos = [t*x2 + (1-t)*x1 for x1, x2 in zip(self.fr, self.to)]
        pass

