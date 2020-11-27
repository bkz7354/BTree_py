import pygame as pg
import uuid
from animation import *
import copy

VALUEBOX_SIZE = [1.0, 1.0]
BOXMOVE_DURATION = 1

class Box:
    def __init__(self, manager, pos_, size_, parent=None, padding=0):
        self.u_id = uuid.uuid1()
        self.size = size_
        self.pos=pos_
        self.color=(100, 100, 100)
        self.parent = parent
        self.padding = padding
        self.manager = manager

    def move(self, pos):
        class move_begin:
            def __init__(self, pos, box):
                self.box = box
                self.pos = copy.deepcopy(pos)

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
        return [xa - x0 for xa, x0 in zip(abs_pos, self.pos)]
    
    def shift_values(self, pos, shift):
        class begin_shift:
            def __init__(self, box, pos, shift):
                self.box = box
                self.move_vect = [shift*VALUEBOX_SIZE[0], 0]
        
            def __call__(self, animation):
                animation_list = []

                for value_box in self.box.contained_values[pos:]:
                    animation_list.append(MoveBoxAnimation(value_box, value_box.pos, [x + d for x, d in zip(value_box.pos, self.move_vect)]))
                new_size = [x + d for x, d in zip(self.box.size, self.move_vect)]
                animation_list.append(ResizeBoxAnimation(self.box, self.box.size, new_size))

                return ParallelAnimation(animation_list)

        return EmptyAnimation(begin_shift(self, pos, shift))

    def insert_value(self, pos, value_box):
        def shift_begin(animation):
            shiftAnimation = self.shift_values(pos, 1)
            return shiftAnimation
        
        def move_begin(animation):
            value_box.parent = self
            value_box.pos = self.relative_from_absolute(value_box.pos)
            self.contained_values.insert(pos, value_box)
            return value_box.move(self.get_relative(pos))

        shiftAnimation = EmptyAnimation(shift_begin)
        moveAnimation = EmptyAnimation(move_begin)

        return SequentialAnimation([shiftAnimation, moveAnimation])
        



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
        SingularAnimation.__init__(self, duration)
        self.fr = pos_from
        self.to = pos_to
        self.box = box

    def update_objects(self):
        t = self.progress
        self.box.pos = [t*x2 + (1-t)*x1 for x1, x2 in zip(self.fr, self.to)]

class ResizeBoxAnimation(SingularAnimation):
    def __init__(self, box, size_from, size_to, duration=BOXMOVE_DURATION):
        SingularAnimation.__init__(self, duration)
        self.fr = size_from
        self.to = size_to
        self.box = box

    def update_objects(self):
        t = self.progress
        self.box.size = [t*x2 + (1-t)*x1 for x1, x2 in zip(self.fr, self.to)]
        pass

