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


def example_mode(line):
    # fill in the string just like the example
    newline = []
    file_index = 0
    for batch in itertools.batched(line, 2):
        newline.extend((file_index,)*int(batch[0]))
        if len(batch) == 2:
            newline.extend((-1,)*int(batch[1]))
        file_index += 1
    return newline

def tuple_mode(line):
    # a different notation for the expanded drive
    newline = []
    file_index = 0
    for batch in itertools.batched(line, 2):
        newline.append((file_index, int(batch[0])))
        if len(batch) == 2:
            newline.append((-1, int(batch[1])))
        file_index += 1
    return newline

def defrag(drive):
    drive = drive[:]
    frags = sum([1 for x in drive if x == -1])
    while -1 in drive:
        frags -=1 
        if frags % 1000:
            print(f'{frags = }') 
        print(f'{frags = }')
        last_block = drive.pop()
        if last_block != -1:
            first_free_block_index = drive.index(-1) 
            drive[first_free_block_index] = last_block
    return drive

def find_hole(drive_tuple, size): 
    # find the first space big enough to fit file size
    for read_index in range(len(drive_tuple)):
        if drive_tuple[read_index][0] == -1:
            # it's free space
            if drive_tuple[read_index][1] >= size:
                # it's big enough
                return read_index

def defrag_2(drive_tuple): 
    drive_tuple = copy.deepcopy(drive_tuple)
    read_id = max(hunk[0] for hunk in drive_tuple)
    while read_id > 0: 
        # print(f'{read_index = }') 
        for read_index in range(len(drive_tuple)):
            if drive_tuple[read_index][0] == read_id:
                break
        file = drive_tuple[read_index]
        # file: (file_no, size) 
        hole_index = find_hole(drive_tuple, size=file[1]) 
        if hole_index is not None and hole_index < read_index: 
            # fill up the space
            assert drive_tuple[hole_index][0] == -1, "tried to overwrite a file"
            old_free = drive_tuple[hole_index]
            drive_tuple[hole_index] = (-1, old_free[1] - file[1])
            # insert the file 
            drive_tuple.insert(hole_index, drive_tuple[read_index]) 
            read_index += 1 # since we added an element
            # blank out the file's original location
            if drive_tuple[read_index-1][0] == -1:
                # add to existing blank space
                old_free = drive_tuple[read_index-1]
                drive_tuple[read_index-1] = (-1, old_free[1] + file[1])
                drive_tuple[read_index] = (-1, 0) # zero length empty space
            else: 
                # change to blank space
                drive_tuple[read_index] = (-1, drive_tuple[read_index][1])
        read_id -= 1            
        print(read_id)
    return drive_tuple

def expand_tuple(drive_tuple):
    expanded_tuple = []
    for hunk in drive_tuple:
        expanded_tuple.extend((hunk[0],)*hunk[1])
    return expanded_tuple

def checksum(drive):
    s = 0 
    for block_index, file_no in enumerate(drive):
        if file_no != -1:
            s += block_index * file_no
    return s

def display(drive_tuple):        
    expanded = expand_tuple(drive_tuple) 
    for i in range(len(expanded)):
        if expanded[i] == -1:
            expanded[i] = '.'
    print(''.join(f'{a}' for a in expanded))



if __name__ == '__main__': 
    # line = open('example').read()
    line = open('input').read()
    line = line.strip()
    drive = tuple_mode(line)
    expanded_before = expand_tuple(drive)
    defragged = defrag_2(drive)
    expanded = expand_tuple(defragged)
    display(defragged)
    print(checksum(expanded))
    __import__('pdb').set_trace()


