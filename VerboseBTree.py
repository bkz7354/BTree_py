from BTree import BTree
import uuid

class VerboseBTree(BTree):
    class Node(BTree.Node):
        def __init__(self, t, is_leaf, tree_instance):
            BTree.Node.__init__(self, t, is_leaf, tree_instance)
            self.u_id = uuid.uuid1()
            self.manager = tree_instance.manager
            self.manager.register_node(self)

        def leaf_insert(self, pos, val):
            self.manager.insert_value(self, pos, val)
            BTree.Node.leaf_insert(self, pos, val)
        
        def leaf_remove(self, r_id):
            self.manager.remove_value(self, r_id)
            BTree.Node.leaf_remove(self, r_id)
        
        def split_child(self, c_id):
            BTree.Node.split_child(self, c_id)
            self.manager.split_child(self, c_id)
        
        def get_max_node(self):
            if self.is_leaf:
                return self
            return self.c[self.fill].get_max_node()

        def inner_remove(self, r_id):
            self.manager.pull_max(self, r_id)
            BTree.Node.inner_remove(self, r_id)

        def rotate_cw(self, c_id):
            self.manager.rotate_cw(self, c_id)
            BTree.Node.rotate_cw(self, c_id)

        def rotate_ccw(self, c_id):
            self.manager.rotate_ccw(self, c_id)
            BTree.Node.rotate_ccw(self, c_id)

        def merge_children(self, c_id):
            self.manager.merge_children(self, c_id)
            BTree.Node.merge_children(self, c_id)
        
        def __str__(self):
            return "[" + str(self.manager.get_id(self)) + "] " + BTree.Node.__str__(self)

    def __init__(self, t, manager):
        BTree.__init__(self, t)
        self.manager = manager
    
    def insert(self, val):
        if self.root == None:
            self.root = self.Node(self.t, True, self)
            self.root.key[0] = val
            self.root.fill = 1
            self.manager.create_root(self.root)
            return
        
        if self.root.fill == 2*self.t-1:
            new_root = self.Node(self.t, False, self)
            new_root.c[0] = self.root
            self.root = new_root

            self.root.split_child(0)
            self.manager.split_root(self.root)
        
        self.root.insert(val)

    def remove(self, val):
        if self.root == None:
            return
        
        self.root.remove(val)
        if self.root.fill == 0:
            if self.root.is_leaf:
                self.manager.delete_root(self.root)
                self.root = None
            else:
                self.manager.replace_root(self.root, self.root.c[0])
                self.root = self.root.c[0]
    