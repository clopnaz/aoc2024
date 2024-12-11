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

logging.basicConfig(level=logging.DEBUG)

up = (-1, 0)
down = (1, 0)
left = (0, -1)
right = (0, 1)

ans = 0 
ans2 = 0 

def blink_the_obvious_way(stones): 
    for stone_no in range(len(stones)):
        if stones[stone_no] == '0':
            stones[stone_no] = '1' 
        elif not len(stones[stone_no]) % 2:
            new_stone = stones[stone_no][len(stones[stone_no])//2:].lstrip('0')
            if new_stone:
                stones.append( new_stone)
            else:
                stones.append( '0')
            stones[stone_no] = stones[stone_no][:len(stones[stone_no])//2].lstrip('0')
        else: 
            stones[stone_no] = str(int(stones[stone_no])*2024)

def blink_one_stone(stone): 
    if stone == '0':
        return  ('1',)
    elif not len(stone) % 2:
        new_stone = stone[len(stone)//2:].lstrip('0')
        if new_stone:
            return (stone[:len(stone)//2].lstrip('0'), new_stone)
        else:
            return ('0', stone[:len(stone)//2].lstrip('0'))
    else: 
        return (str(int(stone)*2024),)

def blink_til_proton_decay(stone, gens_left=6, factor=1):
    if gens_left==0:
        return (stone,)
    if stone == '0':
        return  (*blink_til_proton_decay('1', gens_left=gens_left-1),)
    elif not len(stone) % 2:
        left = stone[:len(stone)//2].lstrip('0')
        right = stone[len(stone)//2:].lstrip('0')
        if not right:
            right = '0'
        return *blink_til_proton_decay(left, gens_left=gens_left-1), *blink_til_proton_decay(right, gens_left=gens_left-1) 
    else: 
        return (*blink_til_proton_decay(str(int(stone)*2024), gens_left=gens_left-1),)

def create_blink_dict(stones):
    new_stones = {}
    for inscription in stones:
        num_stones = stones[inscription]
        for new_inscription in blink_one_stone(inscription):
            if new_inscription in new_stones:
                new_stones[new_inscription] += num_stones
            else:
                new_stones[new_inscription] = num_stones
    return new_stones


def blink_at_dicts(stones, gens):
    old_stones = stones
    stones = {}
    for stone in old_stones:
        if stone in stones:
            stones[stone] += 1
        else:
            stones[stone] = 1
    for gen in range(gens):
        stones = create_blink_dict(stones)
    return sum(stones.values())


if __name__ == '__main__': 
    lines = []
    for line in open('input'):
    # for line in open('example'):
    # for line in open('example_1'):
        line = line.strip()
        stones = line.split(' ')

    print(f'{blink_at_dicts(stones, 25) = }')
    print(f'{blink_at_dicts(stones, 75) = }')
