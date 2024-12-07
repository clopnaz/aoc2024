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

# lines = [line.strip() for line in open('example')]
lines = [line.strip() for line in open('input')]
# print(lines)
for line in lines: 
    firstnum,nums = line.split(':') 
    firstnum = int(firstnum)
    nums = [int(num) for num in nums.split()]
    good = False
    op_choices = [operator.mul, operator.add, 'cat']
    # for ops in itertools.combinations_with_replacement(op_choices, len(nums)-1):
    for ops in itertools.product(op_choices, repeat=len(nums)-1):
        guess = nums[0]
        for op, num in zip(ops, nums[1:]): 
            if op == 'cat':
                guess = int(f'{guess}{num}')
            else:
                guess = op(guess, num)

        if guess == firstnum:
            good = True
            print(f'{firstnum}: {nums = } {ops = }')
            ans += firstnum
            break
        else:
            pass
            # print(f'bad: {nums = } {ops = } {firstnum = } {guess = }')
print(ans)

