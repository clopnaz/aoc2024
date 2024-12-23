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





# PART 1
lines = []
# for line_no, line in enumerate(open("input")):

def secret_generator(number):
    yield number
    for n in range(2000):
        number = (number ^ (number * 64)) % 16777216
        number = (number ^ (number // 32)) % 16777216
        number = (number ^ (number * 2048)) % 16777216
        yield number

def price_generator(number):
    for number in secret_generator(number):
        yield number % 10 

one_two_three = 123
assert [a for a in secret_generator(one_two_three)][10] == 5908254

# for line_no, line in enumerate(open("example")):
for line_no, line in enumerate(open("input")):
    line = line.strip()
    lines.append(line)




ans = 0 
for line_no, line in enumerate(lines):
    number = int(line)
    for n in secret_generator(number):
        pass
    ans += number
print(f'part 1 answer: {ans}')

print('part 2')
def diff(iterable): 
    yield None
    for a,b in itertools.pairwise(iterable):
        yield b-a

def quad_history(price_generator): 
    history = (None,)*4
    for d in diff(price_generator):
        history = history[1:] + (d,)
        yield history


def change_key_gen(values):
    for key in itertools.combinations(values, 4):
        sums = tuple(itertools.accumulate(key))
        if not (min(sums) < -9 or max(sums) > 9): 
            yield(key)

change_keys = tuple(change_key_gen(list(range(-9,10))))
print(f'{len(change_keys) = }') 
print(f'{len(set(change_keys)) = }') 

     

for history, price in zip(quad_history(price_generator(123)), price_generator(123)):
    if history == (-1, -1, 0, 2):
        print(f'{history = } {price = }')
        assert price == 6
        break

profits = collections.Counter()
for line_no, line in enumerate(open('input', 'r')):
# for line_no, line in enumerate(open('example', 'r')):
    num = int(line)
    occurred = set()
    for history, price in zip(quad_history(price_generator(num)), price_generator(num)):
        if None in history: 
            continue
        elif history in occurred:
            continue
        else:
            profits[history] += price
            occurred.add(history)
print(f'{profits.most_common()[0] = }')
__import__('pdb').set_trace()

