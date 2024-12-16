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
# from icecream import ic

logging.basicConfig(level=logging.DEBUG)

up = (-1, 0)
down = (1, 0)
left = (0, -1)
right = (0, 1)
dirs = (up, down, left, right)

ans = 0 
ans2 = 0 

def num_connections(positions):
    num = 0 
    for position in positions: 
        x = position[0]
        y = position[1]
        for d in dirs:
            if (x + d[0], y+d[1]) in positions:
                num += 1
    return num         

def valid_index(x=0, y=0):
    if x<0:
        return False
    elif y<0:
        return False
    elif x>=len(lines):
        return False
    elif y>=len(lines[x]):
        return False
    return True

class Warehouse():
    def __init__(self, lines):
        self.walls = []
        self.boxes = []
        linerator = (l for l in lines)
        for row_no, row in enumerate(linerator):  
            if not row: 
                break
            row = row.strip()
            for col_no, character in enumerate(row):
                if character == 'O':
                    self.boxes.append((row_no, col_no) )
                    logging.debug('box %s', (row_no,col_no))
                elif character == '@':
                    self.robot = (row_no, col_no)
                    logging.debug('robot %s', (row_no,col_no))
                elif character == '#':
                    self.walls.append((row_no, col_no))
                    logging.debug('wall %s', (row_no,col_no))
                else:
                    assert character == '.', f"unexpected character {character = }"

        self.commands = []
        for line in linerator: 
            line = line.strip()
            for character in line:
                if character == 'v':
                    self.commands.append(down)
                elif character == '>':
                    self.commands.append(right)
                elif character == '^':
                    self.commands.append(up)
                elif character == '<':
                    self.commands.append(left)
                else:
                    assert False, "bad character {character = }"

    def try_move_box(self, box, direction):
        assert box in self.boxes, f"{box = } {self.boxes = }"
        destination = (box[0] + direction[0], box[1] + direction[1])
        if destination in self.boxes:
            if not self.try_move_box(destination, direction):
                return False
        elif destination in self.walls: 
            return False
        self.boxes.remove(box)
        self.boxes.append(destination)
        return True


    def try_move_robot(self, direction):
        destination = (self.robot[0] + direction[0], self.robot[1] + direction[1])
        if destination in self.boxes:
            if not self.try_move_box(destination, direction):
                return False
        elif destination in self.walls: 
            return False
        self.robot = destination
    
    def step(self):
        direction = self.commands.pop(0)
        self.try_move_robot(direction)

    @property
    def gps(self): 
        gps = 0 
        for box in self.boxes:
            gps += box[0] * 100 + box[1]
        return gps                

def expand_map(lines):
    lines = (l for l in lines)
    new_lines = []
    for line in lines: 
        line = line.strip()
        if not line:
            break
        new_line = []
        for character in line:
            if character == 'O':
                new_line.append('[')
                new_line.append(']')
            elif character == '@':
                new_line.append('@')
                new_line.append('.')
            elif character == '#':
                new_line.append('#')
                new_line.append('#')
            elif character == '.':
                new_line.append('.')
                new_line.append('.')
            else:
                assert character == '.', f"unexpected character {character = }"
        new_lines.append(''.join(new_line))
    new_lines.append(line)
    for line in lines: 
        new_lines.append(line)

    return new_lines

class Warehouse_2():
    def __init__(self, lines):
        self.walls = []
        self.leftboxes = []
        self.rightboxes = []
        linerator = (l for l in lines)
        for row_no, row in enumerate(linerator):  
            if not row: 
                break
            row = row.strip()
            for col_no, character in enumerate(row):
                if character == '[':
                    self.leftboxes.append((row_no, col_no) )
                elif character == ']':
                    self.rightboxes.append((row_no, col_no) )
                elif character == '@':
                    self.robot = (row_no, col_no)
                elif character == '#':
                    self.walls.append((row_no, col_no))
                else:
                    assert character == '.', f"unexpected character {character = }"

        self.commands = []
        for line in linerator: 
            line = line.strip()
            for character in line:
                if character == 'v':
                    self.commands.append(down)
                elif character == '>':
                    self.commands.append(right)
                elif character == '^':
                    self.commands.append(up)
                elif character == '<':
                    self.commands.append(left)
                else:
                    assert False, "bad character {character = }"

    def can_move_box(self, box, direction):
        if box in self.leftboxes:
            leftbox = box
            rightbox = (box[0] + right[0], box[1] + right[1])
        elif box in self.rightboxes:
            rightbox = box
            leftbox = (box[0] + left[0], box[1] + left[1])
        else:
            assert False, f"no box {box = } {self.leftboxes = } {self.rightboxes = }"
        leftdestination = (leftbox[0] + direction[0], leftbox[1] + direction[1])
        if direction != right: # boxes can't bump into themselves
            if leftdestination in self.leftboxes or leftdestination in self.rightboxes:
                if not self.can_move_box(leftdestination, direction):
                    return False
            elif leftdestination in self.walls: 
                return False
        if direction != left: # boxes can't bump into themselves
            rightdestination = (rightbox[0] + direction[0], rightbox[1] + direction[1])
            if rightdestination in self.leftboxes or rightdestination in self.rightboxes:
                if not self.can_move_box(rightdestination, direction):
                    return False
            elif rightdestination in self.walls: 
                return False
        return True

    def try_move_box(self, box, direction):
        if self.can_move_box(box, direction):
            if box in self.leftboxes:
                leftbox = box
                rightbox = (box[0] + right[0], box[1] + right[1])
            elif box in self.rightboxes:
                rightbox = box
                leftbox = (box[0] + left[0], box[1] + left[1])
            else:
                assert False, f"no box {box = } {self.leftboxes = } {self.rightboxes = }"
            leftdestination = (leftbox[0] + direction[0], leftbox[1] + direction[1])
            rightdestination = (rightbox[0] + direction[0], rightbox[1] + direction[1])
            assert leftdestination not in self.walls
            assert rightdestination not in self.walls
            if direction != right: # boxes can't bump into themselves
                if leftdestination in self.leftboxes or leftdestination in self.rightboxes:
                    assert self.try_move_box(leftdestination, direction)
            if direction != left: # boxes can't bump into themselves
                if rightdestination in self.leftboxes or rightdestination in self.rightboxes:
                    assert self.try_move_box(rightdestination, direction)
            self.leftboxes.remove(leftbox)
            self.leftboxes.append(leftdestination)
            self.rightboxes.remove(rightbox)
            self.rightboxes.append(rightdestination)
            return True
        else:
            return False


    def try_move_robot(self, direction):
        destination = (self.robot[0] + direction[0], self.robot[1] + direction[1])
        if destination in self.leftboxes or destination in self.rightboxes:
            if not self.try_move_box(destination, direction):
                return False
        elif destination in self.walls: 
            return False
        self.robot = destination
    
    def step(self):
        direction = self.commands.pop(0)
        self.try_move_robot(direction)

    @property
    def gps(self): 
        gps = 0 
        for box in self.leftboxes:
            gps += box[0] * 100 + box[1]
        return gps                
if __name__ == '__main__': 
    lines = []
    for line_no, line in enumerate(open('input')):
    # for line_no, line in enumerate(open('example')):
    # for line_no, line in enumerate(open('example_2')):
    # for line_no, line in enumerate(open('example_3')):
        line = line.strip()
        lines.append(line)
    w = Warehouse(lines)    
    while w.commands:
        w.step()
    logging.info(f'{w.gps = }')

    new_lines = expand_map(lines)
    print('\n'.join(new_lines))
    w2 = Warehouse_2(new_lines)
    while w2.commands:
        w2.step()
    logging.info(f'{w2.gps = }')


    
