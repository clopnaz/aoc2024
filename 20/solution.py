#!/usr/bin/env python3
import operator
import itertools

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


def find_cheats(path, cheat_start, max_cheat_length=2, min_cheat_score=2):
    cheat_scores = collections.Counter()
    cheat_start_index = path.index(cheat_start)
    cheat_ends = path[cheat_start_index+min_cheat_score+1:]

    for cheat_end in cheat_ends:
        cheat_length = distance(cheat_start, cheat_end)
        if 2 <= cheat_length <= max_cheat_length:
            cheat_score = path.index(cheat_end) - path.index(cheat_start) - cheat_length
            if cheat_score >= min_cheat_score:
                cheat_scores.update([cheat_score])
    return cheat_scores

if __name__ == "__main__":
    lines = []
    for line_no, line in enumerate(open("input")):
    # for line_no, line in enumerate(open("example_1")):
        line = line.strip()
        lines.append(line)

    path_locs = []
    for row_no, row in enumerate(lines):
        for col_no, char in enumerate(row):
            if char == 'S':
                S = (row_no, col_no)
            elif char == 'E':
                E = (row_no, col_no)
            elif char == '.':
                path_locs.append((row_no, col_no)) 
    path_locs.append(E)
    path = []
    path.append(S)
    while path_locs:
        current = path[-1]
        curr_x = current[0]
        curr_y = current[1]
        for path_loc in path_locs:
            px = path_loc[0]
            py = path_loc[1]
            if curr_x - px == 0 and abs(curr_y - py) == 1:
                path.append(path_loc)
                break
            elif curr_y - py == 0 and abs(curr_x - px) == 1:
                path.append(path_loc)
                break
        path_locs.remove(path[-1])
    path_locs = tuple(path_locs)
    print('begin cheating')
    cheat_scores = collections.Counter()
    for loc_no, loc in enumerate(path):
        if loc_no % 50 == 0:
            print(f'{loc_no}/{len(path)}\r', end='')
        new_cheats = find_cheats(path, loc, min_cheat_score=50, max_cheat_length=20)
        cheat_scores.update(find_cheats(path, loc, min_cheat_score=100, max_cheat_length=20))
    print(cheat_scores)
    print(sum([value for key,value in cheat_scores.items()]))
    __import__('pdb').set_trace()


