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



class Pad:
    def __init__(self):
        self.dictify_grid()
        self.inv_dict = {value: key for key, value in self.dict.items()}

    def dictify_grid(self):
        pad_dict = {}
        for row_no, row in enumerate(self.grid):
            for col_no, col in enumerate(row):
                pad_dict[col] = (row_no, col_no)
        self.dict = pad_dict

    def button_displacement(self, dest_button):
        return (
            self.dict[dest_button][0] - self.loc[0],
            self.dict[dest_button][1] - self.loc[1],
        )

    def presses(self, orig, dest):
        orig = self.dict[orig]
        dest = self.dict[dest]
        row_diff = dest[0] - orig[0] 
        col_diff = dest[1] - orig[1]
        if row_diff < 0:
            up_down_presses = "^" * -row_diff
        else:
            up_down_presses = "v" * row_diff
        if col_diff < 0:
            left_right_presses = "<" * -col_diff
        else:
            left_right_presses = ">" * col_diff
        if self.dict[None][1] == orig[1]: 
            # can crash in this col, get out of it first
            return left_right_presses + up_down_presses + 'A'
        else:
            return up_down_presses + left_right_presses + 'A'

    def expand(self, codes):
        expanded_codes = []
        for code in codes:
            for a,b in itertools.pairwise('A' + code):
                expanded_codes.append(self.presses(a,b))
        return expanded_codes

    def __repr__(self):
        row_vals = set()
        col_vals = set()
        for loc in self.inv_dict.keys():
            row_vals.add(loc[0])
            col_vals.add(loc[1])
        lines = ''
        for row_no in range(max(row_vals)+1):
            line = ''
            for col_no in range(max(col_vals)+1):
                if self.inv_dict.get((row_no, col_no), None) is not None:
                    if self.loc == (row_no, col_no):
                        line += f' [{self.inv_dict[row_no, col_no]}] '
                    else:
                        line += f'  {self.inv_dict[row_no, col_no]}  '
                else:
                    line += '     '
            lines += line + '\n'
        return lines 

class NumPad(Pad):
    grid = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [None, "0", "A"]]


class DPad(Pad):
    grid = [[None, "^", "A"], ["<", "v", ">"]]




complexity_1 = 0
# for line in open('example', 'r'):
for line in open('input', 'r'):
    line = line.strip()
    code = (line,)
    print(code)
    code = NumPad().expand(code)
    # print(code)
    code = DPad().expand(code)
    # print(code)
    code = DPad().expand(code)
    # print(code)
    # print(code)
    code_string = ''.join(code)
    __import__('pdb').set_trace()
    partial_complexity =  len(code_string) * int(line[:3])
    complexity_1 += partial_complexity
    print(f'{len(code_string) = } {int(line[:3]) = } {partial_complexity = }')
print(f'{complexity_1 = }')
__import__('pdb').set_trace()
