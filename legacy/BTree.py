#!/usr/bin/env python3


class BTree:
    class Node:
        def __init__(self, t, is_leaf, tree_instance):
            self.t = t
            self.fill = 0
            self.key = [None]*(2*t-1)
            self.c = [None]*(2*t)
            self.is_leaf = is_leaf

            self.inst = tree_instance
        
        def find_key(self, val):
            i = 0
            while i < self.fill and self.key[i] < val:
                i += 1
            return i

        def leaf_insert(self, pos, val):
            for i in range(self.fill, pos, -1):
                self.key[i] = self.key[i-1]
            self.key[pos] = val
            self.fill += 1

        def insert(self, val):
            pos = self.find_key(val)

            if self.is_leaf:
                self.leaf_insert(pos, val)
            else:
                if self.c[pos].fill == 2*self.t-1:
                    self.split_child(pos)
                    if val > self.key[pos]:
                        pos += 1
                
                self.c[pos].insert(val)

        def split_child(self, c_id):
            l = self.c[c_id]
            r = self.inst.Node(self.t, l.is_leaf, self.inst)

            for i in range(self.t-1):
                r.key[i] = l.key[self.t + i]
                l.key[self.t + i] = None

            if not l.is_leaf:
                for i in range(self.t):
                    r.c[i] = l.c[self.t + i]
                    l.c[self.t + i] = None

            for i in range(self.fill, c_id, -1):
                self.c[i+1] = self.c[i]
                self.key[i] = self.key[i-1]
            
            self.c[c_id+1] = r
            self.key[c_id] = l.key[self.t-1]
            l.key[self.t-1] = None
            
            self.fill += 1
            l.fill = self.t-1
            r.fill = self.t-1

        def remove(self, val):
            pos = self.find_key(val)

            if pos < self.fill and self.key[pos] == val:
                if self.is_leaf:
                    self.leaf_remove(pos)
                else:
                    self.inner_remove(pos)
            else:
                if self.is_leaf:
                    return
                
                self.c[pos].remove(val)
                self.balance(pos)

        def leaf_remove(self, r_id):
            self.fill -= 1
            self.key[r_id] = None
            for i in range(r_id, self.fill):
                self.key[i] = self.key[i+1]
        
        def inner_remove(self, r_id):
            self.key[r_id] = self.c[r_id].get_max()
            self.c[r_id].remove_max()
            self.balance(r_id)

        def get_max(self):
            if self.is_leaf:
                return self.key[self.fill-1]
            return self.c[self.fill].get_max()
        
        def remove_max(self):
            if self.is_leaf:
                self.leaf_remove(self.fill-1)
            else:
                self.c[self.fill].remove_max()
                self.balance(self.fill)

        def balance(self, r_id):
            if self.c[r_id].fill >= self.t-1:
                return

            if r_id > 0 and self.c[r_id-1].fill > self.t-1:
                self.rotate_cw(r_id-1)
            elif r_id < self.fill and self.c[r_id+1].fill > self.t-1:
                self.rotate_ccw(r_id)
            elif r_id > 0:
                self.merge_children(r_id-1)
            else:
                self.merge_children(r_id)

        def rotate_cw(self, c_id):
            l = self.c[c_id]
            r = self.c[c_id+1]

            for i in range(r.fill, 0, -1):
                r.key[i] = r.key[i-1]
                r.c[i+1] = r.c[i]
            r.c[1] = r.c[0]

            r.key[0] = self.key[c_id]
            self.key[c_id] = l.key[l.fill-1]
            l.key[l.fill-1] = None

            r.c[0] = l.c[l.fill]
            l.c[l.fill] = None

            l.fill -= 1
            r.fill += 1

        def rotate_ccw(self, c_id):
            l = self.c[c_id]
            r = self.c[c_id+1]

            l.key[l.fill] = self.key[c_id]
            self.key[c_id] = r.key[0]
            
            l.fill += 1
            r.fill -= 1

            l.c[l.fill] = r.c[0]

            for i in range(r.fill):
                r.key[i] = r.key[i+1]
                r.c[i] = r.c[i+1]
            r.c[r.fill] = r.c[r.fill+1]
            r.key[r.fill] = None
            r.c[r.fill+1] = None


        def merge_children(self, c_id):
            l = self.c[c_id]
            r = self.c[c_id+1]

            l.key[l.fill] = self.key[c_id]
            for i in range(r.fill):
                l.key[l.fill + 1 + i] = r.key[i]
                l.c[l.fill + 1+ i] = r.c[i]
            l.c[l.fill + 1 + r.fill] = r.c[r.fill]
            l.fill = l.fill + r.fill + 1 

            self.fill -= 1
            for i in range(c_id, self.fill):
                self.key[i] = self.key[i+1]
                self.c[i+1] = self.c[i+2]

        def find(self, val):
            pos = self.find_key(val)
            if pos < self.fill and self.key[pos] == val:
                return True
            
            if not self.is_leaf:
                return self.c[pos].find(val)
            return False

        def __str__(self):
            res = "> " \
                + "".join([
                      str(self.key[i]) + " " for i in range(self.fill)
                  ]) + "\n"
            
            if not self.is_leaf:
                res += "+---"*(self.fill) + "+\n"
                for i in range(self.fill, -1, -1):
                    res += ("|   "*(i+1) + "\n")
                    res += "".join([
                        "|   "*i + line + "\n" 
                        for line in str(self.c[i]).splitlines()
                    ])

            return res

    def __init__(self, t):
        self.t = t
        self.root = None

    def insert(self, val):
        if self.root == None:
            self.root = self.Node(self.t, True, self)
            self.root.key[0] = val
            self.root.fill = 1
            return
        
        if self.root.fill == 2*self.t-1:
            new_root = self.Node(self.t, False, self)
            new_root.c[0] = self.root
            self.root = new_root

            self.root.split_child(0)
        
        self.root.insert(val)

    def remove(self, val):
        if self.root == None:
            return
        
        self.root.remove(val)
        if self.root.fill == 0:
            if self.root.is_leaf:
                self.root = None
            else:
                self.root = self.root.c[0]
    
    def find(self, val):
        if self.root == None:
            return False
        return self.root.find(val)

    def __str__(self):
        if self.root == None:
            return "the tree is empty\n"
        return self.root.__str__()
    
    def empty(self):
        return self.root == None


