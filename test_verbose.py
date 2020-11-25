#!/usr/bin/env python3

import random as rnd
from VerboseBTree import VerboseBTree

min_int = 0
max_int = 100

def get_sample(sample_size):
    res = []
    for i in range(sample_size):
        res.append(rnd.randint(min_int, max_int))
    return res

def get_unique(sample):
    res = []

    for x in sample:
        if not x in res:
            res.append(x)
    
    return res


def show_result(tree, sample):
    un = get_unique(sample)
    un.sort()

    tree_cont = [x for x in range(min_int, max_int+1) if tree.find(x)]

    if un == tree_cont:
        print("Tree contents match with sample")
        if un:
            print(*un, sep=' ', end='\n')
    else:
        print("Tree contents match with sample")
        print(*un, sep=' ', end='\n')
        print(*tree_cont, sep=' ', end='\n')

    print(tree)

def delete_half(tree, sample):
    for i in range(len(sample)-1, len(sample)//2 - 1, -1):
        tree.remove(sample[i])
        del sample[i]


class SimpleManager:
    def __init__(self):
        self.nodes = {}
        self.counter = 0

    def get_id(self, node):
        return self.nodes[node.u_id]

    def register_node(self, node):
        self.nodes[node.u_id] = self.counter
        self.counter += 1
        node.manager = self
        print("node" + str(self.nodes[node.u_id]) + " registered")

    def insert_value(self, node, val, pos):
        print("inserting " + str(val) + 
                " at pos " + str(pos) + " in node" 
                           + str(self.nodes[node.u_id]))

    def remove_value(self, node, pos):
        print("removing value" 
                " at pos " + str(pos) + " in node" 
                           + str(self.nodes[node.u_id]))
        

    def pull_max(self, node, pos):
        max_node = node.c[pos].get_max_node()
        print("pulling max from" +
                "node" + str(self.get_id(max_node)) + " to " +
                "node" + str(self.get_id(node)))

    def split_child(self, node, pos):
        print("splitting child" + 
                " at pos " + str(pos) + " in node" 
                           + str(self.nodes[node.u_id]))

    def rotate_cw(self, node, pos):
        print("rotating clockwise" + 
                " at pos " + str(pos) + " in node" 
                           + str(self.nodes[node.u_id]))

    def rotate_ccw(self, node, pos):
        print("rotating counterclockwise" + 
                " at pos " + str(pos) + " in node" 
                           + str(self.nodes[node.u_id]))

    def merge_children(self, node, pos):
        print("merging children" + 
                " at pos " + str(pos) + " in node" 
                           + str(self.nodes[node.u_id]))

    def create_root(self, root):
        print("creating root with value " + str(root.key[0]))
    
    def split_root(self, new_root):
        print("splitting root that is node" + str(self.nodes[new_root.u_id]))

    def delete_root(self, root):
        print("deleting root as node" + str(self.get_id(root)))

    def replace_root(self, old_root, new_root):
        print("changing root from" + 
              "node" + str(self.get_id(old_root)) + "to" +
              "node" + str(self.get_id(new_root)))

mng = SimpleManager()
tree = VerboseBTree(3, mng)

sample = get_sample(15)
print("Got following sample")
print(sample, '\n')

for x in sample:
    tree.insert(x)
show_result(tree, sample)

while not tree.empty():
    delete_half(tree, sample)
    show_result(tree, sample)