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

def make_rexpression(towels):
    # return r'(' + '|'.join(towels) + r')+'
    return r'(?:' + '|'.join([f'(?P<{name}>{name})' for name in towels]) + r')+'
    # return r'((' + ')|('.join(towels) + r'))+'


def find_redundant_towels(towels):
    towels = copy.deepcopy(towels)
    towels = sorted(towels, key=lambda x: len(x), reverse=True)
    backwards = {}
    for towel in copy.copy(towels):
        new_towels = copy.deepcopy(towels)
        new_towels.remove(towel)
        rexpression = make_rexpression(new_towels)
        match = re.fullmatch(rexpression, towel) 
        if match is not None:
            towels.remove(towel) 
    return towels
@functools.cache
def redundify(towel, towels):
    # print(f'{towel = }') 
    towels = tuple([t for t in towels if t!=towel])
    num_redunds = 0 
    for t in towels:
        if towel.startswith(t):
            remaining = towel.removeprefix(t)
            # print(f'{towel = :>12} {t = } {remaining = }')
            if remaining in towels: 
                # print('match')
                num_redunds += 1
            num_redunds += redundify(remaining, towels)
    # print(f'{towel = } {redunds = }')
    return num_redunds
            



if __name__ == "__main__":
    lines = []
    for line_no, line in enumerate(open("input")):
    # for line_no, line in enumerate(open("example")):
        line = line.strip()
        lines.append(line)

    towels = []
    designs = []
    lineiter = iter(lines)
    for line in lineiter:
        line = line.strip()
        if not line: 
            break
        towels.extend(l.strip() for l in line.split(','))
    for line in lineiter:
        line = line.strip()
        designs.append(line)
    towels = tuple(sorted(towels, key=lambda x: len(x), reverse=True))
    orig_towels = towels
    # lol
    print(f'{towels[0] = }')
    # redd = redundify(towels[0], towels)
    towels = find_redundant_towels(towels)
    towels = tuple(towels)
    print(f'{len(towels) = }')
    rexpression = make_rexpression(towels)
    rc = re.compile(rexpression)
    all_matches = []
    all_redunds = 0
    for design_no, design in enumerate(designs):
        match = rc.fullmatch(design)
        if match is not None:
            print(f'{design_no:>4}: {design}') 
            all_matches.append(match)
            all_redunds += redundify(design, orig_towels)
    print(f'{len(all_matches) = }')
    print(f'{all_redunds = }')
    __import__('pdb').set_trace()


