#!/usr/bin/env python3
import operator
import itertools
import pathlib
import logging
import re
import copy
import graphlib

logging.basicConfig(level=logging.DEBUG)

up = (-1, 0)
down = (1, 0)
left = (0, -1)
right = (0, 1)

ans = 0 
ans2 = 0 


def all_nines(lines):
    for row_no, row in enumerate(lines):
        for col_no, num in enumerate(row):
            if num == 9:
                yield (row_no, col_no) 

def all_zeros(lines):
    for row_no, row in enumerate(lines):
        for col_no, num in enumerate(row):
            if int(num) == 0:
                yield (row_no, col_no) 

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

def score_path(lines, x, y, prev_xy=None):
    peaks_reachable = []
    curr_level = int(lines[x][y])
    if curr_level == 9:
        return [(x,y)]
    next_level = curr_level + 1 
    for direction in (up, down, left, right):
        next_xy = (x + direction[0], y + direction[1])
        if next_xy != prev_xy and valid_index(lines, next_xy[0], next_xy[1]):
            if int(lines[next_xy[0]][next_xy[1]]) == next_level:
                peaks_reachable.extend(score_path(lines, next_xy[0], next_xy[1], (x,y)))
    return peaks_reachable

def score_path_2(lines, x, y, prev_xy=None):
    score = 0 
    curr_level = int(lines[x][y])
    if curr_level == 9:
        return 1
    next_level = curr_level + 1 
    for direction in (up, down, left, right):
        next_xy = (x + direction[0], y + direction[1])
        if next_xy != prev_xy and valid_index(lines, next_xy[0], next_xy[1]):
            if int(lines[next_xy[0]][next_xy[1]]) == next_level:
                score += score_path_2(lines, next_xy[0], next_xy[1], (x,y))

    return score

if __name__ == '__main__': 
    lines = []
    for line in open('input'):
    # for line in open('example'):
    # for line in open('example_1'):
        line = line.strip()
        print(line)
        lines.append([n for n in line])

    total_score_1 = 0 
    total_score_2 = 0 
    for zero in all_zeros(lines):
        total_score_1 += len(set(score_path(lines, zero[0], zero[1])))
        total_score_2 += score_path_2(lines, zero[0], zero[1])
        
    print(f'{total_score_1 = }')
    print(f'{total_score_2 = }')
