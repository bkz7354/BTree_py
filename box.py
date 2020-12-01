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

def x_vector(x):
    return np.array([x, 0])

def y_vector(y):
    return np.array([0, y])

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

    def adjust_size(self):
        self.size = np.array([VALUEBOX_SIZE[0]*len(self.contained_values), VALUEBOX_SIZE[1]])
    
    def adjust_values(self):
        for i, value_box in enumerate(self.contained_values):
            value_box.parent = self
            value_box.pos = x_vector(i*VALUEBOX_SIZE[0])

    def adjust(self):
        self.adjust_size()
        self.adjust_values()

    def get_relative(self, pos):
        return x_vector(pos*VALUEBOX_SIZE[0])

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

                return ParallelAnimation(animation_list)

        return EmptyAnimation(begin_shift(self, pos, shift))

    def shift_connections(self, pos, shift):
        class begin_shift:
            def __init__(self, box, pos, shift):
                self.box = box
                self.move_vect = x_vector(shift*VALUEBOX_SIZE[0])
        
            def __call__(self, animation):
                animation_list = []

                for conn in self.box.connections[pos:]:
                    animation_list.append(MoveConnAnimation(conn, conn.beg, conn.beg + self.move_vect))

                return ParallelAnimation(animation_list)

        return EmptyAnimation(begin_shift(self, pos, shift))


    def resize(self, shift):
        class begin_resize:
            def __init__(self, box):
                self.box = box
                self.move_vect = x_vector(shift*VALUEBOX_SIZE[0])

            def __call__(self, animation):
                return ResizeBoxAnimation(self.box, self.box.size, self.box.size + self.move_vect)

        return EmptyAnimation(begin_resize(self))

    def insert_leaf(self, insert_idx, value_box):
        class insert_begin:
            def __init__(self, box):
                self.box = box
            def __call__(self, animation):
                shift = self.box.shift_values(insert_idx, 1)
                resize = self.box.resize(1)

                value_box.parent = self.box
                value_box.pos = self.box.rel_from_abs(value_box.pos)
                self.box.contained_values.insert(insert_idx, value_box)
                move = value_box.move(self.box.get_relative(insert_idx))

                return ParallelAnimation([shift, resize, move])

        return EmptyAnimation(insert_begin(self))
    
    def split_insert(self, value_box, insert_idx):
        class insert_begin:
            def __init__(self, box):
                self.box = box

            def __call__(self, animation):
                val_shift = self.box.shift_values(insert_idx, 1)
                conn_shift = self.box.shift_connections(insert_idx+1, 1)
                resize = self.box.resize(1)

                value_box.parent = self.box
                value_box.pos = self.box.rel_from_abs(value_box.pos)
                self.box.contained_values.insert(insert_idx, value_box)
                move = value_box.move(self.box.get_relative(insert_idx))

                return ParallelAnimation([val_shift, conn_shift, resize, move])

        return EmptyAnimation(insert_begin(self))

    def split_child(self, c_idx):
        new_node = self.manager.new_node()

        class begin_split:
            def __init__(self, node):
                self.node = node

            def __call__(self, animation):
                node = self.node
                child = node.connections[c_idx].target

                median = len(child.contained_values)//2
                moved_value = child.contained_values[median]
                moved_value.pos = moved_value.pos + child.pos
                moved_value.parent = None
                value_move = node.split_insert(moved_value, c_idx)

                new_node.pos = child.pos + x_vector(VALUEBOX_SIZE[0]*(median+1))
                new_node.contained_values = child.contained_values[median+1:]
                for i, conn in enumerate(child.connections[median+1:]):
                    conn.plug(new_node, i)

                del child.contained_values[median:]
                del child.connections[median+1:]

                child.adjust()
                new_node.adjust()

                def connect_callback(animation):
                    node.manager.connect_nodes(node, new_node, c_idx+1)
                    return animation

                return SequentialAnimation([value_move, 
                                            EmptyAnimation(connect_callback),
                                            node.manager.arrange_boxes([5, 2])])


        return EmptyAnimation(begin_split(self)), new_node

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
        class begin_arrange:
            def __init__(self, manager, root_pos):
                self.manager = manager
                self.root_pos = root_pos
            
            def __call__(self, animation):
                if self.manager.root_id is None:
                    return EmptyAnimation()

                root_pos = np.array(self.root_pos)
                animation_list = []

                root = self.manager.nodes[self.manager.root_id]
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

        return EmptyAnimation(begin_arrange(self, root_pos))

    def split_root(self):
        new_root = self.new_node()
        new_node = self.new_node()

        class begin_split:
            def __init__(self, manager):
                self.manager = manager

            def __call__(self, animation):
                old_root = self.manager.nodes[self.manager.root_id]

                median = len(old_root.contained_values)//2

                new_root.pos = old_root.pos + np.array([VALUEBOX_SIZE[0]*median, 0])        
                new_node.pos = old_root.pos + np.array([VALUEBOX_SIZE[0]*(median + 1), 0])

                new_root.contained_values.append(old_root.contained_values[median])
                
                new_node.contained_values = old_root.contained_values[median+1:]
                for i, conn in enumerate(old_root.connections[median+1:]):
                    conn.plug(new_node, i)

                del old_root.contained_values[median:]
                del old_root.connections[median+1:]

                new_root.adjust()
                old_root.adjust()
                new_node.adjust()
                
                self.manager.connect_nodes(new_root, old_root, 0)
                self.manager.connect_nodes(new_root, new_node, 1)

                self.manager.set_root(new_root)

                return self.manager.arrange_boxes([5, 2])
        
        return EmptyAnimation(begin_split(self)), new_root, new_node



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

class MoveConnAnimation(SingularAnimation):
    def __init__(self, conn, pos_from, pos_to, duration=BOXMOVE_DURATION):
        #print("move box: ", pos_from, pos_to)
        SingularAnimation.__init__(self, duration)
        self.fr = np.array(pos_from)
        self.to = np.array(pos_to)
        self.conn = conn

    def update_objects(self):
        t = self.progress
        self.conn.beg = t*self.to + (1-t)*self.fr
        