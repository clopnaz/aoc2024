#!/usr/bin/env python3
import operator
import itertools
import inspect

import sys
import time
import pathlib
import logging
import collections
import re
import copy
import graphlib
import functools
import heapq

# from icecream import ic

logging.basicConfig(level=logging.INFO)

up = (-1, 0)
down = (1, 0)
left = (0, -1)
right = (0, 1)
# dirs = (up, down, left, right)
dirs = {"^": up, "v": down, "<": left, ">": right}
inv_dirs = {
    up: "^",
    down: "v",
    left: "<",
    right: ">",
}


ans = 0
ans2 = 0


def valid_index(x=0, y=0):
    if x < 0:
        return False
    elif y < 0:
        return False
    elif x > grid_size:
        return False
    elif y > grid_size:
        return False
    return True


def distance(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def displacement(a, b):
    return (b[0] - a[0], b[1] - a[1])





# PART 1
lines = []
connections = collections.defaultdict(set)
# for line_no, line in enumerate(open("example")):
for line_no, line in enumerate(open("input")):
    line = line.strip()
    line = line.split('-')
    connections[line[0]].add(line[1])
    connections[line[1]].add(line[0])

def is_group(group): 
    for member in group: 
        others = set(filter(lambda x: x != member, group))
        if not others <= connections[member]:
            return False
    return True



def all_groups(group_len=3):
    groups = set()
    for origin, destinations in connections.items():
        for combo in itertools.combinations(destinations, group_len-1):
            group = tuple(sorted((origin,) + combo))
            if is_group(group):
                groups.add(group) 
    return groups
groups = all_groups(3) 
ta_groups = set()
for group in groups:
    if list(filter(lambda x: x.startswith('t'), group)):
        ta_groups.add(group) 
print(len(ta_groups))
__import__('pdb').set_trace()
# for line_no, line in enumerate(open("input")):

n = 3 
while True:
    n+=1
    groups = all_groups(n) 
    print(f'{n = } {len(groups) = } ')
    if len(groups) == 1:
        break
','.join(sorted(sorted(tuple(groups))[0]))
__import__('pdb').set_trace()


