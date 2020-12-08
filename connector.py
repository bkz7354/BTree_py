
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

    def leaf_remove(self, node, pos):
        box = self.node_boxes[node.u_id]

        ani = box.leaf_remove(pos)
        self.ani_manager.queue_animation(ani)

    def pull_max(self, node, pos):
        box = self.node_boxes[node.u_id]
        box_fr = self.node_boxes[node.c[pos].get_max_node().u_id]

        ani = box.pull_max(pos, box_fr)
        self.ani_manager.queue_animation(ani)

    def rotate_cw(self, node, pos):
        box = self.node_boxes[node.u_id]

        ani = box.rotate_cw(pos)
        self.ani_manager.queue_animation(ani)


    def rotate_ccw(self, node, pos):
        box = self.node_boxes[node.u_id]

        ani = box.rotate_ccw(pos)
        self.ani_manager.queue_animation(ani)

    def merge_children(self, node, pos):
        box = self.node_boxes[node.u_id]

        ani = box.merge_children(pos)
        del self.node_boxes[node.c[pos+1].u_id]
        self.ani_manager.queue_animation(ani) 

    def change_root(self, old_root, new_root):
        del self.node_boxes[old_root.u_id]
        new_box = self.node_boxes[new_root.u_id]

        ani = self.box_manager.change_root(new_box)
        self.ani_manager.queue_animation(ani)

    def delete_root(self, root):
        ani = self.box_manager.delete_root()
        del self.node_boxes[root.u_id]

        self.ani_manager.queue_animation(ani)