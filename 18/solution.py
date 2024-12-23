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




if __name__ == "__main__":
    lines = []
    for line_no, line in enumerate(open("input")):
    # for line_no, line in enumerate(open("example")):
        line = line.strip()
        lines.append(line)
    # grid_size = 6
    grid_size = 70
    walls = []
    for line_no, line in enumerate(lines):
        line = line.strip()
        wall_col, wall_row = line.split(',')
        walls.append(tuple([int(wall_row), int(wall_col)]))

    # walls = walls[:1024]
    len(walls)
    # walls = walls[:12]
    print(len(walls))


    # (fscore, (loc))
    num_walls = len(walls) 
    orig_walls = walls
    while True:
        walls = orig_walls[:num_walls]
        def error(loc):
            row = loc[0]
            col = loc[1]
            return grid_size * 2 - row - col
        g_score = {}
        came_from = {}
        start = (0,0)
        g_score[start] = 0
        _exit = (grid_size, grid_size)
        open_set = [(error(start)+g_score[start], start)]
        heapq.heapify(open_set)
        while open_set:
            # I guess we're doing A* 
            current = heapq.heappop(open_set)
            current_loc = current[1]
            if current_loc == _exit: break
            tentative_g_score = g_score[current_loc] + 1
            for direction in dirs:
                # generate new spot
                d_row = dirs[direction][0]
                d_col = dirs[direction][1]
                row = current_loc[0] + d_row
                col = current_loc[1] + d_col
                new_loc = (row, col)
                if not valid_index(x=row, y=col) or new_loc in walls:
                    continue
                elif (new_loc not in g_score) or tentative_g_score < g_score[new_loc]:
                    came_from[new_loc] = current_loc
                    g_score[new_loc] = tentative_g_score
                    fscore = tentative_g_score + error(new_loc)
                    heapq.heappush(open_set, (fscore, new_loc))
                 
        def path(end_loc):
            p = [end_loc]
            while p[-1] in came_from:
                p.append(came_from[p[-1]])
            p.reverse()
            return p

        p = path(current_loc)
        def solu():
            lines = ''
            for row_no in range(grid_size+1):
                for col_no in range(grid_size+1):
                    loc = (row_no, col_no)
                    if loc in walls:
                        lines += '#'
                    elif loc in p:
                        lines += 'O'
                    else: 
                        lines += '.'
                lines += '\n'
            return lines
        x = solu()
        # print(x)
                
        # print(f'{p = }') 
        # print(f'{len(p) = }') 
        # print(f'{g_score[current_loc] = }')
        if current_loc == _exit:
            break
        num_walls -= 1
    final_wall = orig_walls[num_walls]
    final_wall = tuple(reversed(final_wall))
    print(f'{final_wall = }') 
    __import__('pdb').set_trace()

