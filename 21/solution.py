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

def displacement_presses(displacement):
    if displacement[0] < 0:
        up_down_presses = "^" * -displacement[0]
    else:
        up_down_presses = "v" * displacement[0]
    if displacement[1] < 0:
        left_right_presses = "<" * -displacement[1]
    else:
        left_right_presses = ">" * displacement[1]
    return up_down_presses + left_right_presses    

class Pad:
    def __init__(self):
        self.dictify_grid()
        self.curr_button = "A"
        self.loc = self.dict[self.curr_button]
        self.inv_dict = {value: key for key, value in self.dict.items()}

    def dictify_grid(self):
        pad_dict = {}
        for row_no, row in enumerate(self.grid):
            for col_no, col in enumerate(row):
                pad_dict[col] = (row_no, col_no)
        self.dict = pad_dict

    def button_displacement(self, dest_button):
        try:
            return (
                self.dict[dest_button][0] - self.loc[0],
                self.dict[dest_button][1] - self.loc[1],
            )
        except:
            __import__('pdb').set_trace()
            raise
            pass

    def press_code(self, button_code):
        presses = ""
        for button in button_code:
            new_presses_1 = self.robo_presses(button)
            presses += new_presses_1
            self.commit(button)
        return presses

    def commit(self, button):
        self.curr_button = button
        self.loc = self.dict[button]

    def reset(self):
        self.commit("A")

    def all_presses(self, button):
        displacement = self.button_displacement(button)
        if displacement[0] < 0:
            up_down_presses = "^" * -displacement[0]
        else:
            up_down_presses = "v" * displacement[0]
        if displacement[1] < 0:
            left_right_presses = "<" * -displacement[1]
        else:
            left_right_presses = ">" * displacement[1]
        presses = up_down_presses + left_right_presses
        # TODO:
        #      1) starting in bottom row, ending in left col? go *up* first
        #      2) starting in left col, ending in bottom row? go *right* first
        none_distance = self.button_displacement(None)
        denied_move = ''
        if 0 in none_distance:
            # need to worry about crashing the robot
            denied_move = displacement_presses(none_distance)

        for p in set(itertools.permutations(presses, len(presses))):
            p = ''.join(p) 
            if 'v>v' in p: 
                continue
            elif '>^>' in p: 
                continue
            elif '^<^' in p:
                continue
            elif '<v<' in p:
                continue
            else:
                if not (denied_move and p.startswith(denied_move)):
                    yield p + "A"
        self.commit(button)
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

class Pad_1(Pad):
    grid = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [None, "0", "A"]]

    def robo_presses(self, button):
        """the arrows needed to get to button"""
        displacement = self.button_displacement(button)
        presses = ""
        if displacement[0] < 0:
            up_down_presses = "^" * -displacement[0]
        else:
            up_down_presses = "v" * displacement[0]
        if displacement[1] < 0:
            left_right_presses = "<" * -displacement[1]
        else:
            left_right_presses = ">" * displacement[1]
        # TODO:
        #      1) starting in bottom row, ending in left col? go *up* first
        #      2) starting in left col, ending in bottom row? go *right* first
        if self.loc[0] == 3 and self.dict[button][1] == 0:
            presses = up_down_presses + left_right_presses
        # elif self.loc[0] == 3 and self.dict[button][1] == 0:
        presses += "A"
        return presses


class Pad_2(Pad):
    grid = [[None, "^", "A"], ["<", "v", ">"]]

    def robo_presses(self, button, nudge=False):
        """the arrows needed to get to button"""
        # TODO:
        #      1) starting in top row, ending in left col? go *down* first
        #      2) starting in left col, ending in top row? go *right* first
        displacement = self.button_displacement(button)
        if displacement[0] < 0:
            # presses.extend('^' * -displacement[0])
            up_down_presses = "^" * -displacement[0]
        else:
            # presses.extend('v' * displacement[0])
            up_down_presses = "v" * displacement[0]
        if displacement[1] < 0:
            # presses.extend('<' * -displacement[1])
            left_right_presses = "<" * -displacement[1]
        else:
            # presses.extend('>' * displacement[1])
            left_right_presses = ">" * displacement[1]
        if self.loc[0] == 0 and self.dict[button][1] == 0:
            # presses = up_down_presses + left_right_presses
            presses = left_right_presses + up_down_presses
        else:
            if nudge:
                presses = left_right_presses + up_down_presses
            else:
                presses = up_down_presses + left_right_presses

        presses = left_right_presses + up_down_presses
        presses = up_down_presses + left_right_presses
        # presses = left_right_presses + up_down_presses
        # presses = left_right_presses + up_down_presses
        presses += "A"
        return presses


num_pad = Pad_1()
d_pad1 = Pad_2()
d_pad2 = Pad_2()
human_pad = Pad_2()
pads = [num_pad, d_pad1, d_pad2]

def reset_all():
    for robot in pads:
        robot.commit('A')

def tell():
    strs = []
    all_pads = pads + [human_pad]
    for pad in all_pads:
        pad_strs = []
        for line in str(pad).splitlines():
            pad_strs.append(line)
        strs.append(pad_strs)
    for line in itertools.zip_longest(*strs, fillvalue=' '*15):
        print('       '.join(line))
    
tell()



@functools.cache
def presses(locs, start='A', pad_no=0, end_pad_no=2):
    if pad_no > end_pad_no:
        raise NotImplementedError()
    loc_presses = []
    pads[pad_no].commit(start)
    for loc in locs:
        loc_presses.append(list(itertools.chain(pads[pad_no].all_presses(loc))))
    loc_presses = list(itertools.product(*loc_presses))
    loc_presses = tuple([''.join(a) for a in loc_presses])
    if pad_no == end_pad_no:
        return loc_presses
    else: 
        new_presses = ()
        for loc_press in loc_presses:
            new_presses = tuple(itertools.chain(new_presses, presses(loc_press, pad_no=pad_no+1, end_pad_no=end_pad_no)))
        return new_presses

def only_shortest(l):
    least_len = len(min(l, key=len))
    return [x for x in l if len(x) == least_len]

@functools.cache
def click(buttons):
    # starting at 'A' move a d_pad to buttons, then back to A and click A
    # print(buttons)
    # __import__('pdb').set_trace()
    pad = Pad_2()
    presses_buttons = []
    for button in buttons:
        all_presses_button = list(pad.all_presses(button))
        presses_buttons.append(only_shortest(all_presses_button)[0])
        pad.commit(button)
    presses_buttons = ''.join(presses_buttons)
    if button != 'A':
        all_presses_A = list(pad.all_presses('A'))
        presses_A = only_shortest(all_presses_A) 
        presses_buttons += presses_A[0]
    return  tuple(split_codes(presses_buttons))

def code_clicker(codes):
    for code in codes:
        yield from click(code)

def split_codes(code): 
    left, a, right = code.partition('A')
    while left or a or right:
        yield left + a
        code = right
        left, a, right = code.partition('A')


    return (c + 'A' for c in code.split('A') if c)

def join_codes(codes): 
    return ''.join(codes)

@functools.cache 
def click(code):
    # returns a generator of the codes required to press code
    # code: any list of buttons where the only A is the last press. 
    assert code[-1] == 'A', f'{code = }'
    pad = Pad_2()
    next_codes = []
    for button in code:
        next_codes.append(only_shortest(list(pad.all_presses(button)))[0])
    return next_codes
    
def click_deeper(codes):
    # code: a code that ends in A 
    # returns the length of the code 
    for code_no, code in enumerate(codes):
        yield from click(code)

@functools.cache
def how_long(code, depth=2):
    assert depth >= 0
    if depth==0:
        return len(code)
    else:
        return sum(how_long(c, depth=depth-1) for c in click(code))


def code_length(codestr, depth=2):
    codes = tuple(split_codes(codestr))
    return sum(how_long(code, depth=depth) for code in codes)


inp = '<A^A>^^AvvvA'
out = 'v<<A>>^A<A>AvA<^AA>A<vAAA>^A'
print(out)
print(''.join(click_deeper(split_codes(inp))))
print(len(out))
print(code_length(inp, depth=1))
out = '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A'
print(out)
print(''.join(click_deeper(click_deeper(split_codes(inp)))))
print(f'{len(out) = }') 
print(code_length(inp, depth=2))
# for codes_no, codes in enumerate(code_clicker(split_codes('<A^A>^^AvvvA')):
# print(''.join(code_clicker(code_clicker(split_codes('<A^A>^^AvvvA')))))

print(f'{code_length(inp, depth=4) = }')
print(f'{code_length(inp, depth=8) = }')
print(f'{code_length(inp, depth=16) = }')
print(f'{code_length(inp, depth=32) = }')
print(f'{code_length(inp, depth=64) = }')




# PART 1
lines = []
for line_no, line in enumerate(open("input")):
# for line_no, line in enumerate(open("example")):
    line = line.strip()
    lines.append(line)

complexity = 0
for line in lines:
    print()
    # get possible layer, then full possible from layer. show it passes tests. 
    # then try minimizing the layer first
    presses_layer = presses(line, end_pad_no=1)
    presses_layer = list(presses_layer)
    # print()
    # print(len(presses_layer))
    # print(len(set(presses_layer)))
    presses_layer = only_shortest(presses_layer)
    # print(len(presses_layer))
    presses_lens = collections.Counter(len(list(a)) for  a in presses_layer)
    all_possible = []
    for code in presses_layer:
        all_possible.extend(presses(code, pad_no=2))

    # print(len(all_possible))
    # print(len(set(all_possible)))
    possible_lens = collections.Counter(len(list(a)) for  a in all_possible)
    all_possible = only_shortest(all_possible)
    # print(len(set(all_possible)))
    if line == '029A': 
        if '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A' in all_possible:
            print('pass')
        else:
            print('fail') 
    elif line == '980A':
        if '<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A' in all_possible:
            print('pass')
        else:
            print('fail') 
    elif line == '179A':
        if '<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A' in all_possible:
            print('pass')
        else:
            print('fail') 
    elif line == '456A':
        if '<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A' in all_possible:
            print('pass')
        else:
            print('fail') 
    elif line == '379A':
        if '<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A' in all_possible:
            print('pass')
        else:
            print('fail') 
    len_counter = collections.Counter(len(list(a)) for  a in all_possible)
    __import__('pdb').set_trace()
    min_len = min(len_counter)
    partial_complexity = int(line[:3]) * min_len
    print(f'{line = } {min_len = } {partial_complexity = }')
    complexity += partial_complexity
    # print(collections.Counter(len(a) for a in all_possible))
print(complexity)
if line == '379A':
    assert complexity == 126384
else: 
    assert complexity == 162740
__import__('pdb').set_trace()
# part 2 
complexity = 0 
# for line in open('input', 'r'): 
for line in open('', 'r'): 
    line = line.strip()
    presses_layer = list(presses(line, end_pad_no=1))
    presses_layer = sorted(presses_layer, key=len)
    all_possible = []
    for code in presses_layer:
        all_possible.extend(presses(code, pad_no=2))
    all_possible = sorted(all_possible, key=len)
    this_codes_length = len(all_possible[0])
    if line == '379A':
        __import__('pdb').set_trace()
    partial_complexity = int(line[:3]) * this_codes_length
    print(f'{line = } {this_codes_length = } {partial_complexity = }')

    complexity += partial_complexity
print(complexity)
if line == '379A':
    assert complexity == 126384
else: 
    assert complexity == 162740
