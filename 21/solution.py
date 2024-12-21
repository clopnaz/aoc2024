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

def displacement(a, b):
    return (b[0] - a[0],  b[1] - a[1])

class Pad:
    def __init__(self): 
        self.dictify_grid()
        self.curr_button = 'A'
        self.loc = self.dict[self.curr_button]
        self.inv_dict = {value: key for key,value in self.dict.items()}

    def dictify_grid(self):
        pad_dict = {}
        for row_no, row in enumerate(self.grid):
            for col_no, col in enumerate(row):
                pad_dict[col] = (row_no, col_no)
        self.dict = pad_dict
    
    def button_displacement(self, dest_button):
        return (b[0] - a[0],  b[1] - a[1])

    def press_code(self, button_code): 
        presses = ''
        for button in button_code: 
            new_presses_1 = self.robo_presses(button)
            new_presses_2 = self.robo_presses(button, nudge=True)
            if len(new_presses_1) != len(new_presses_2):
                __import__('pdb').set_trace()
                pass # wut
            presses += new_presses_1
            self.commit(button)
        return presses

    def commit(self, button): 
        self.curr_button = button
        self.loc = self.dict[button]

    def reset(self):
        self.commit('A')

class Pad_1(Pad):
    grid = [['7','8','9'],['4','5','6'],['1','2','3'],[None,'0','A']]

    def robo_presses(self, button):
        """ the arrows needed to get to button """
        displacement = self.button_displacement(button) 
        presses = ''
        if displacement[0] < 0: 
            up_down_presses = '^' * -displacement[0]
        else: 
            up_down_presses = 'v' * displacement[0]
        if displacement[1] < 0: 
            left_right_presses = '<' * -displacement[1]
        else:
            left_right_presses = '>' * displacement[1]
        # TODO: 
        #      1) starting in bottom row, ending in left col? go *up* first
        #      2) starting in left col, ending in bottom row? go *right* first
        if self.loc[0] == 3 and self.dict[button][1] == 0:
            presses = up_down_presses + left_right_presses
        #elif self.loc[0] == 3 and self.dict[button][1] == 0:
        presses += 'A'
        return presses

    def all_presses(self, button): 
        displacement = self.button_displacement(button) 
        if displacement[0] < 0: 
            up_down_presses = '^' * -displacement[0]
        else: 
            up_down_presses = 'v' * displacement[0]
        if displacement[1] < 0: 
            left_right_presses = '<' * -displacement[1]
        else:
            left_right_presses = '>' * displacement[1]
        __import__('pdb').set_trace()
        # TODO: 
        #      1) starting in bottom row, ending in left col? go *up* first
        #      2) starting in left col, ending in bottom row? go *right* first
        presses = up_down_presses + left_right_presses
        for p in itertools.permutations(presses, len(presses)):
            yield p + 'A'


class Pad_2(Pad):
    grid = [[None, '^', 'A'], ['<', 'v', '>']]

    def robo_presses(self, button, nudge=False):
        """ the arrows needed to get to button """
        # TODO: 
        #      1) starting in top row, ending in left col? go *down* first
        #      2) starting in left col, ending in top row? go *right* first
        displacement = self.button_displacement(button) 
        if displacement[0] < 0: 
            # presses.extend('^' * -displacement[0])
            up_down_presses = '^' * -displacement[0]
        else: 
            # presses.extend('v' * displacement[0])
            up_down_presses = 'v' * displacement[0]
        if displacement[1] < 0: 
            # presses.extend('<' * -displacement[1])
            left_right_presses = '<' * -displacement[1]
        else:
            # presses.extend('>' * displacement[1])
            left_right_presses = '>' * displacement[1]
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
        presses += 'A'
        return presses

r1 = Pad_1()
r2 = Pad_2()
r3 = Pad_2()
robots = [r1, r2, r3]

def press_code(code, robot_no = 0): 
    robots[robot_no] 


if __name__ == "__main__":
    lines = []
    # for line_no, line in enumerate(open("input")):
    for line_no, line in enumerate(open("example")):
        line = line.strip()
        lines.append(line)
    
    complexity_sum = 0
    for code_1 in lines:
        #print(f'{len(code_1) = :<4}: {code_1 = }') 
        code_2 = pad_1.press_code(code_1)
        #print(f'{len(code_2) = :<4}: {code_2 = }') 
        code_3 = pad_2.press_code(code_2)
        # print(f'{len(code_3) = :<4}: {code_3 = }') 
        code_4 = pad_3.press_code(code_3)
        print(f'{len(code_4) = :<4}: {code_4 = }') 
        complexity_1 = int(code_1[:3])
        complexity_2 = len(code_4)
        complexity = int(code_1[:3]) * len(code_4) 
        print(f'{code_1}: complexity = {complexity_1} * {complexity_2} = {complexity}')            
        complexity_sum += complexity

    print(f'{complexity_sum = }') 

    __import__('pdb').set_trace()
