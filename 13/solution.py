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



if __name__ == '__main__': 
    lines = []
    for line in open('input'):
    # for line in open('example'):
    # for line in open('example_1'):
    # for line in open('example_2'):
    # for line in open('example_3'):
    # for line in open('example_4'):
        line = line.strip()
        if line:
            lines.append(line)
    
    ans = 0
    for line_group in itertools.batched(lines, 3): 
        """
        XA*A + XB*B = XP
        YA*A + YB*B = YP

        XB*YA*B - XA*YB*B = YA*XP - XA*YP
        B = (YA*XP - XA*YP) / (XB*YA - XA*YB)
        A = (XP - XB*B) / XA
        """
        XA = int(re.search(r'X\+(\d+)', line_group[0]).groups()[0])
        YA = int(re.search(r'Y\+(\d+)', line_group[0]).groups()[0])
        XB = int(re.search(r'X\+(\d+)', line_group[1]).groups()[0])
        YB = int(re.search(r'Y\+(\d+)', line_group[1]).groups()[0])
        XP = int(re.search(r'X\=(\d+)', line_group[2]).groups()[0])
        YP = int(re.search(r'Y\=(\d+)', line_group[2]).groups()[0])
        B = (YA*XP - XA*YP) / (XB*YA - XA*YB)
        A = (XP - XB*B) / XA
        if A.is_integer() and B.is_integer():
            tok = 3*int(A) + int(B)
            ans += tok
    ans_2 = 0 
    for line_group in itertools.batched(lines, 3): 
        """
        XA*A + XB*B = XP
        YA*A + YB*B = YP

        XB*YA*B - XA*YB*B = YA*XP - XA*YP
        B = (YA*XP - XA*YP) / (XB*YA - XA*YB)
        A = (XP - XB*B) / XA
        """
        # ic(line_group)
        XA = int(re.search(r'X\+(\d+)', line_group[0]).groups()[0])
        YA = int(re.search(r'Y\+(\d+)', line_group[0]).groups()[0])
        XB = int(re.search(r'X\+(\d+)', line_group[1]).groups()[0])
        YB = int(re.search(r'Y\+(\d+)', line_group[1]).groups()[0])
        XP = 10000000000000+int(re.search(r'X\=(\d+)', line_group[2]).groups()[0])
        YP = 10000000000000+int(re.search(r'Y\=(\d+)', line_group[2]).groups()[0])
        B = (YA*XP - XA*YP) / (XB*YA - XA*YB)
        A = (XP - XB*B) / XA
        if A.is_integer() and B.is_integer():
            tok = 3*int(A) + int(B)
            ans_2 += tok
    print(f'{ans = }')
    print(f'{ans_2 = }')




