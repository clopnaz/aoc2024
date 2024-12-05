#!/usr/bin/env python3
import itertools
import pathlib
import logging
import re
logging.basicConfig(level=logging.DEBUG)

def num_mas_from_point(lines, row, col): 
    # look for center A
    if lines[row][col] != 'A':
        return 0
    # skip outer ring, we can't make an X around an A on the border
    if row < 1 or col < 1 or row >= len(lines)-1 or col >= len(lines[row])-1: 
        return 0
    # ok just look for 2 MAS's
    # directions = ((-1,1), (-1, -1))
    try:
        ms_1 = lines[row-1][col+1] + lines[row+1][col-1]
        ms_2 = lines[row-1][col-1] + lines[row+1][col+1]
    except:
        __import__('pdb').set_trace()
    if 'M' in ms_1 and 'S' in ms_1 and 'M' in ms_2 and 'S' in ms_2:
        return 1
    return 0

def num_xmas_from_point(lines, row, col):
    if lines[row][col] != 'X':
        return 0
    directions = ((0,1), (-1,1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1))
    letters = ('X', 'M', 'A', 'S')
    total_xmas = 0
    for direction in directions:
        for letter_index in range(len(letters)):
            letter_row = row + direction[0]*letter_index
            letter_col = col + direction[1]*letter_index
            # skip this direction if we go out of bounds
            try:
                if letter_row < 0 or letter_col < 0 or letter_row > len(lines)-1 or letter_col > len(lines[letter_row])-1:
                    break
            except: 
                __import__('pdb').set_trace()
            # skip this direction if the letter doesn't match 
            if letter_index == 0:
                # first of all, we already checked 'X'
                assert(lines[letter_row][letter_col] == letters[letter_index])
            if lines[letter_row][letter_col] != letters[letter_index]:
                break
            if letter_index == len(letters) - 1:
                if lines[letter_row][letter_col] == letters[letter_index]:
                    # we got to the last index and the letter matches. add one
                    total_xmas += 1 

    return total_xmas


answer_1 = 0
answer_2 = 0
lines = []
with open('input') as fd:
# with open('input2') as fd:
    for line in fd:
        lines.append(line.strip())
for row_no in range(len(lines)):
    for col_no in range(len(lines[row_no])):
        answer_1 += num_xmas_from_point(lines, row_no, col_no)
        if num_xmas_from_point(lines, row_no, col_no):
            print(f"{row_no =}, {col_no =}, {num_xmas_from_point(lines, row_no, col_no)}")
        answer_2 += num_mas_from_point(lines, row_no, col_no)
print(answer_1)
print(answer_2)
