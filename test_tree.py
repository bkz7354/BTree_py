#!/usr/bin/env python3

import random as rnd
from BTree import BTree

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

tree = BTree(3)
sample = get_sample(40)
print("Got following sample")
print(sample, '\n')

for x in sample:
    tree.insert(x)
show_result(tree, sample)

while not tree.empty():
    delete_half(tree, sample)
    show_result(tree, sample)

