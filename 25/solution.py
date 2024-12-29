#!/usr/bin/env python
import pdb
import itertools
import functools
import pprint
import copy
import collections

lines = ()
# for line in open('example'):
# for line in open('example_2'):
# for line in open('input'):

# print('\n'.join(lines))


def show_schem(schem):
    print('\n'.join(schem))

with open('input') as fd: 
    locks = ()
    keys = ()
    schem = ()
    for line in fd: 
        line = line.strip()
        if not line: 
            if schem[0] == '.'*5:
                keys += (schem,)
            elif schem[-1] == '.'*5:
                locks += (schem,) 
            else: 
                Exception()
            schem = ()
        else:
            schem += (line,) 
    if schem[0] == '.'*5:
        keys += (schem,)
    elif schem[-1] == '.'*5:
        locks += (schem,) 
    else: 
        Exception()

def encode_key(key): 
    key = tuple(reversed(key) )
    return encode_lock(key)

def encode_lock(lock): 
    lock_codes = [0]*len(lock[0])
    for row_no, row in enumerate(lock): 
        for col_no, col in enumerate(row):
            if lock[row_no][col_no] == '#': 
                lock_codes[col_no] = row_no
    return lock_codes            

# print('keys') 
# for key in keys:
#     show_schem(key) 
#     print(encode_key(key))
# 
# print('locks')
# for lock in locks: 
#     show_schem(lock) 
#     print(encode_lock(lock))

def fits(key_code, lock_code): 
    for k, l in zip(key_code, lock_code):
        if k + l > 5:
            return False
    return True


ans_1 = 0 
for key in keys: 
    for lock in locks: 
        # show_schem(key) 
        # print(encode_key(key))
        # print()
        # show_schem(lock)
        # print(encode_lock(lock))
        if fits(encode_key(key), encode_lock(lock)):
            # print('fits!') 
            ans_1 += 1
        # else: 
        #     print('no fit!') 

print(f'{ans_1 }')

pdb.set_trace()
