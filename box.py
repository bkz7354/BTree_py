import pygame as pg
import uuid
import numpy as np
from animation import *
import copy
import colors as col

VALUEBOX_SIZE = np.array([1.0, 1.0])
BOXMOVE_DURATION = 0.2
ROW_DISTANCE = VALUEBOX_SIZE[1]
NODE_DISTANCE = VALUEBOX_SIZE[0]

class Box:
    def __init__(self, manager, pos, size, parent=None, padding=0):
        self.u_id = uuid.uuid1()
        self.size = np.array(size)
        self.pos  = np.array(pos)
        self.color = col.DARK_BLUE
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
    
    def update(self):
        pass

class ValueBox(Box):
    def __init__(self, manager, pos, val, parent=None):
        Box.__init__(self, manager, pos, VALUEBOX_SIZE, parent=parent)
        self.value = val


class NodeBox(Box):
    def __init__(self, manager, pos, parent=None):
        Box.__init__(self, manager, pos, VALUEBOX_SIZE, parent=parent, padding=0.1)
        self.contained_values = []
        self.connections = []

        self.color = col.BLUE
        self.size[0] = 0


    def get_relative(self, pos):
        return [pos*VALUEBOX_SIZE[0], 0]

    def rel_from_abs(self, abs_pos):
        return abs_pos - self.pos
    
    def abs_from_rel(self, rel_pos):
        return self.pos + rel_pos
    
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
                value_box.pos = self.box.rel_from_abs(value_box.pos)
                self.box.contained_values.insert(insert_idx, value_box)

                return value_box.move(self.box.get_relative(insert_idx))

        shiftAnimation = EmptyAnimation(shift_begin(self))
        moveAnimation = EmptyAnimation(move_begin(self))

        return SequentialAnimation([shiftAnimation, moveAnimation])
    
    def remove_value(self, remove_idx):
        value_box = self.contained_values[remove_idx] 

        fullAnimation = None # Do something here
        return fullAnimation, value_box # returns animation and the removed box
        
    def add_connection(self, conn, idx):
        self.connections.insert(idx, conn)
        conn.beg = self.get_relative(idx) + np.array([0, VALUEBOX_SIZE[1]])

    
    
class Connection:
    def __init__(self, target_node):
        self.target = target_node
        self.color = col.BLACK
        self.u_id = uuid.uuid1()

        self.beg = None
    
    def plug(self, parent_node, idx):
        self.parent = parent_node
        parent_node.add_connection(self, idx)

    def get_end(self):
        return self.target.pos + [self.target.size[0]/2, 0]

class BoxManager:
    def __init__(self):
        self.values = {}
        self.nodes = {}
        self.connections = {}
    
        self.root_id = None

    def new_node(self):
        res = NodeBox(self, [0, 0])
        self.nodes[res.u_id] = res
        return res
    
    def new_value(self, val):
        res = ValueBox(self, [0,0], val)
        self.values[res.u_id] = res
        return res
    
    def connect_nodes(self, parent_node, child_node, c_idx):
        conn = Connection(child_node)
        conn.plug(parent_node, c_idx)
        self.connections[conn.u_id] = conn
        return conn

    def set_root(self, node):
        self.root_id = node.u_id

    def arrange_boxes(self, root_pos=[0, 0]):
        if self.root_id is None:
            return EmptyAnimation()

        root_pos = np.array(root_pos)
        animation_list = []

        root = self.nodes[self.root_id]
        animation_list.append(root.move(root_pos - np.array([root.size[0]/2, 0])))
        center_x, root_y = root_pos

        prev_row = [root]
        row_number = 1
        while True:
            new_row = [conn.target for node in prev_row for conn in node.connections]
            if len(new_row) == 0:
                break
            
            row_y = root_y + row_number*(VALUEBOX_SIZE[0] + ROW_DISTANCE)
            value_number = sum([len(node.contained_values) for node in new_row])
            row_width = value_number*VALUEBOX_SIZE[0] + (len(new_row)-1)*NODE_DISTANCE

            row_x = center_x - row_width/2
            for i, node in enumerate(new_row):
                animation_list.append(node.move(np.array([row_x, row_y])))
                row_x += node.size[0] + NODE_DISTANCE
            
            prev_row = new_row
            row_number += 1

        return ParallelAnimation(animation_list)




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
        
        self.box.update()

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

