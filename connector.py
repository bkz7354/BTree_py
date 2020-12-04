
class Connector:
    def __init__(self, ani_manager, box_manager):
        self.ani_manager = ani_manager
        self.box_manager = box_manager
        self.node_boxes = {}

    def create_root(self, root_node, val):
        ani, box = self.box_manager.create_root(val)
        self.node_boxes[root_node.u_id] = box
        self.ani_manager.queue_animation(ani)

    def split_root(self, root_node):
        new_node = root_node.c[1]

        ani, root_box, child_box = self.box_manager.split_root()
        self.node_boxes[root_node.u_id] = root_box
        self.node_boxes[new_node.u_id] = child_box
        
        self.ani_manager.queue_animation(ani)
    
    def leaf_insert(self, node, pos, val):
        box = self.node_boxes[node.u_id]

        ani = box.leaf_insert(pos, self.box_manager.new_value(val))
        self.ani_manager.queue_animation(ani)

    def split_child(self, node, pos):
        box = self.node_boxes[node.u_id]

        ani, new_box = box.split_child(pos)
        self.node_boxes[node.c[pos+1].u_id] = new_box
        self.ani_manager.queue_animation(ani)