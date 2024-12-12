#!/usr/bin/env python3
import operator
import itertools
import pathlib
import logging
import collections
import re
import copy
import graphlib
import functools
# from icecream import ic

logging.basicConfig(level=logging.DEBUG)

up = (-1, 0)
down = (1, 0)
left = (0, -1)
right = (0, 1)
dirs = (up, down, left, right)

ans = 0 
ans2 = 0 



def valid_index(lines, x=0, y=0):
    if x<0:
        return False
    elif y<0:
        return False
    elif x>=len(lines):
        return False
    elif y>=len(lines[x]):
        return False
    return True

@functools.cache
def matching_neighbors(lines, origin):
    origin_plant = lines[origin[0]][origin[1]]
    matches = []
    for direction in dirs:
        loc = (origin[0] + direction[0], origin[1]+direction[1])
        if valid_index(lines, loc[0], loc[1]) and lines[loc[0]][loc[1]] == origin_plant:
            matches.append(loc)
    return tuple(matches)

def unit_perimiter(lines, loc):
    num_neighbors = len(matching_neighbors(lines, loc)) 
    return 4 - num_neighbors

def side_directions(lines, loc):
    loc_plant = lines[loc[0]][loc[1]]
    matches = []
    for direction in dirs:
        new_loc = (loc[0] + direction[0], loc[1]+direction[1])
        if not(valid_index(lines, new_loc[0], new_loc[1])) or lines[new_loc[0]][new_loc[1]] != loc_plant:
            matches.append(direction)
    return tuple(matches)

def unit_sides(lines, loc):
    loc_sides = set(side_directions(lines, loc))
    for direction in loc_sides:
        assert len(direction) == 2
    shared_sides = []
    for neighbor in matching_neighbors(lines, loc):
        neighbor_sides = set(side_directions(lines, neighbor))
        for neighbor_side in neighbor_sides:
            assert len(neighbor_side) == 2
        shared_sides.extend(loc_sides & neighbor_sides)

    return loc_sides, shared_sides


def paint_region(lines, origin):
    region = set(((origin),))
    matches = set(matching_neighbors(lines, origin))
    while matches - region: 
        region = region | matches
        matches = set()
        for origin in region:
            matches.update(matching_neighbors(lines, origin))
    region = region | matches
    return sorted(region)


if __name__ == '__main__': 
    lines = []
    # for line in open('input'):
    # for line in open('example'):
    # for line in open('example_1'):
    # for line in open('example_2'):
    # for line in open('example_3'):
    for line in open('example_4'):
        line = tuple(line.strip())
        lines.append(line)
    lines = tuple(lines)
    regions = set()
    print('\n'.join([' '.join(l) for l in lines]))
    painted_locs = []
    for row_no in range(len(lines)):
        print(f'{row_no = } ({len(lines) = }')
        for col_no in range(len(lines[row_no])):
            loc = (row_no,col_no)
            if loc not in painted_locs:
                region = tuple(paint_region(lines, loc))
                regions.update(((region),))
                painted_locs.extend(region)
    cost = 0
    cost_2 = 0 
    for region in regions:
        perimiter = 0
        num_unit_sides = 0
        num_shared_sides = 0
        for loc in region:
            perimiter += unit_perimiter(lines, loc)
            loc_sides, shared_sides = unit_sides(lines, loc)
            num_unit_sides += len(loc_sides)
            num_shared_sides += len(shared_sides)
        cost += perimiter * len(region) 
        assert num_shared_sides % 2 == 0 
        actual_num_sides = num_unit_sides - num_shared_sides//2
        cost_2 += actual_num_sides * len(region)
        # print(f'{region = }') 
        # print(f'{num_unit_sides = }')
        # print(f'{num_shared_sides = }')
        # print(f'{actual_num_sides = }')
    # print('{lines = }')
    # print('{regions = }')
    print(f'{cost = }')
    print(f'{cost_2 = }')
