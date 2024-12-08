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

# lines = tuple([tuple(line.strip()) for line in open('example')])
# lines = tuple([tuple(line.strip()) for line in open('example_1')])
# lines = tuple([tuple(line.strip()) for line in open('example_2')])
lines = [line.strip() for line in open('input')]
print('\n'.join([''.join(l) for l in lines]))

all_antennas = []
for line in lines: 
    all_antennas.extend(line[:])
frequencies = set(all_antennas) - set('.')
print(f'{frequencies = }')

def find_antenna(lines, f):
    for row_no, row in enumerate(lines):
        for col_no, col in enumerate(row):
            if lines[row_no][col_no] == f:
                yield (row_no, col_no)
def valid_loc(lines, row=0, col=0):
    if row<0:
        return False
    elif col<0: 
        return False
    elif row>=len(lines):
        return False
    elif col>=len(lines):
        return False
    else:
        return True
nodes = []
for frequency in frequencies:
    antenna_locs = list(find_antenna(lines, frequency))
    for antenna_a_no, antenna_loc_a in enumerate(antenna_locs):
        for antenna_b_no, antenna_loc_b in enumerate(antenna_locs):
            if antenna_a_no == antenna_b_no: 
                continue
            else:
                distance_xy = (
                        antenna_loc_a[0] - antenna_loc_b[0],
                        antenna_loc_a[1] - antenna_loc_b[1],
                )
                
                node_1 = (
                    antenna_loc_a[0] + distance_xy[0],
                    antenna_loc_a[1] + distance_xy[1]
                )
                node_2 = (
                    antenna_loc_b[0] - distance_xy[0],
                    antenna_loc_b[1] - distance_xy[1]
                )
                if valid_loc(lines, row=node_1[0], col=node_1[1]):
                    nodes.append(node_1)
                if valid_loc(lines, row=node_2[0], col=node_2[1]):
                    nodes.append(node_2)
print(f'{nodes = }')
lines2 = [list(l) for l in lines]
for node in nodes:
    lines2[node[0]][node[1]] = '#'
print('\n'.join(''.join(l) for l in lines2))
antinodes = [(row_no,col_no) for row_no, row in enumerate(lines2) for col_no, col in enumerate(row) if col=='#']
print(f'{antinodes = }') 
num_antinodes = len(antinodes)
print(f'{num_antinodes = }') 

def print_antinodes(lines, nodes):
    print('*PRINT_ANTINODES')
    lines = [list(l) for l in lines]
    for node in nodes:
        lines[node[0]][node[1]] = '#'
    print('\n'.join(''.join(l) for l in lines))
    antinodes = [(row_no,col_no) for row_no, row in enumerate(lines) for col_no, col in enumerate(row) if col=='#']
    # print(f'{antinodes = }') 
    num_antinodes = len(antinodes)
    print(f'{num_antinodes = }') 

def all_nodes(lines, antenna_loc_a, antenna_loc_b):
    print(f'{antenna_loc_a = }')
    print(f'{antenna_loc_b = }')
    distance_xy = (
            antenna_loc_a[0] - antenna_loc_b[0],
            antenna_loc_a[1] - antenna_loc_b[1],
    )
    new_nodes = []
    # node_1 
    node_index = 0 
    while True:
        new_node = (
            antenna_loc_a[0] + node_index * distance_xy[0],
            antenna_loc_a[1] + node_index * distance_xy[1]
        )
        if valid_loc(lines, row=new_node[0], col=new_node[1]):
            new_nodes.append(new_node)
            node_index += 1
        else:
            break
    # node_2 
    node_index = 0 
    while True:
        new_node = (
            antenna_loc_b[0] - node_index * distance_xy[0],
            antenna_loc_b[1] - node_index * distance_xy[1]
        )
        if valid_loc(lines, row=new_node[0], col=new_node[1]):
            new_nodes.append(new_node)
            node_index += 1
        else:
            break
    return new_nodes
nodes_2 = []
for frequency in frequencies:
    antenna_locs = list(find_antenna(lines, frequency))
    for antenna_a_no, antenna_loc_a in enumerate(antenna_locs):
        for antenna_b_no, antenna_loc_b in enumerate(antenna_locs):
            if antenna_a_no == antenna_b_no: 
                continue
            else:
                new_nodes = all_nodes(lines, antenna_loc_a, antenna_loc_b)
                nodes_2.extend(new_nodes)
print_antinodes(lines, nodes_2)
