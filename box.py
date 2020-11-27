import pygame as pg
import uuid
import numpy as np
from animation import *
import copy

VALUEBOX_SIZE = np.array([1.0, 1.0])
BOXMOVE_DURATION = 0.5

class Box:
    def __init__(self, manager, pos, size, parent=None, padding=0):
        self.u_id = uuid.uuid1()
        self.size = np.array(size)
        self.pos  = np.array(pos)
        self.color = (100, 100, 100)
        self.parent = parent
        self.padding = padding
        self.manager = manager

    def move(self, pos):
        class move_begin:
            def __init__(self, pos, box):
                self.box = box
                self.pos = np.array(pos)

            def __call__(self, animation):
                return MoveBoxAnimation(self.box, self.box.pos, pos)
        
        return EmptyAnimation(move_begin(pos, self))

class ValueBox(Box):
    def __init__(self, manager, pos, val, parent=None):
        Box.__init__(self, manager, pos, copy.deepcopy(VALUEBOX_SIZE), parent=parent)
        self.color = (200, 200, 200)
        self.value = val


class NodeBox(Box):
    def __init__(self, manager, pos, parent=None):
        Box.__init__(self, manager, pos, copy.deepcopy(VALUEBOX_SIZE), parent=parent, padding=0.1)
        self.contained_values = []
        self.size[0] = 0

    def get_relative(self, pos):
        return [pos*VALUEBOX_SIZE[0], 0]

    def relative_from_absolute(self, abs_pos):
        return abs_pos - self.pos
    
    def shift_values(self, pos, shift):
        class begin_shift:
            def __init__(self, box, pos, shift):
                self.box = box
                self.move_vect = np.array([shift*VALUEBOX_SIZE[0], 0])
        
            def __call__(self, animation):
                animation_list = []

                for value_box in self.box.contained_values[pos:]:
                    animation_list.append(MoveBoxAnimation(value_box, value_box.pos, value_box.pos + self.move_vect))
                animation_list.append(ResizeBoxAnimation(self.box, self.box.size, self.box.size + self.move_vect))

                return ParallelAnimation(animation_list)

        return EmptyAnimation(begin_shift(self, pos, shift))

    def insert_value(self, insert_idx, value_box):
        class shift_begin:
            def __init__(self, box):
                self.box = box
            def __call__(self, animation):
                shiftAnimation = self.box.shift_values(insert_idx, 1)

                return shiftAnimation
        
        class move_begin:
            def __init__(self, box):
                self.box = box
            def __call__(self, animation):
                value_box.parent = self.box
                value_box.pos = self.box.relative_from_absolute(value_box.pos)
                self.box.contained_values.insert(insert_idx, value_box)

                return value_box.move(self.box.get_relative(insert_idx))

        shiftAnimation = EmptyAnimation(shift_begin(self))
        moveAnimation = EmptyAnimation(move_begin(self))

        return SequentialAnimation([shiftAnimation, moveAnimation])
    
    def remove_value(self, remove_idx):
        value_box = self.contained_values[remove_idx] 

        fullAnimation = None # Do something here
        return fullAnimation, value_box # returns animation and the removed box
        



class BoxManager:
    def __init__(self):
        self.boxes = {}
    
    def new_node(self):
        res = NodeBox(self, [0, 0])
        self.boxes[res.u_id] = res
        return res
    
    def new_value(self, val):
        res = ValueBox(self, [0,0], val)
        self.boxes[res.u_id] = res
        return res
    

class MoveBoxAnimation(SingularAnimation):
    def __init__(self, box, pos_from, pos_to, duration=BOXMOVE_DURATION):
        #print("move box: ", pos_from, pos_to)
        SingularAnimation.__init__(self, duration)
        self.fr = np.array(pos_from)
        self.to = np.array(pos_to)
        self.box = box

    def update_objects(self):
        t = self.progress
        self.box.pos = t*self.to + (1-t)*self.fr

class ResizeBoxAnimation(SingularAnimation):
    def __init__(self, box, size_from, size_to, duration=BOXMOVE_DURATION):
        #print("resize box: ", size_from, size_to)
        SingularAnimation.__init__(self, duration)
        self.fr = size_from
        self.to = size_to
        self.box = box

    def update_objects(self):
        t = self.progress
        self.box.size = t*self.to + (1-t)*self.fr

