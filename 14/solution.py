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

class Robot():
    def __init__(self, x0, y0, vx, vy, width, height):
        self.x0 = x0
        self.y0 = y0
        self.vx = vx
        self.vy = vy
        self.x = x0
        self.y = y0
        self.width = width
        self.height = height

    def simulate(self, t):
        self.x += t * self.vx
        self.y += t * self.vy
        while self.x >= self.width:
            self.x -= self.width
        while self.x < 0:
            self.x += self.width
        while self.y >= self.height:
            self.y -= self.height 
        while self.y < 0:
            self.y += self.height

    @property
    def quadrant(self):
        if self.x < (width)//2 and self.y < (height)//2:
            return 2
        elif self.x > (width)//2 and self.y < (height)//2:
            return 1
        elif self.x < (width)//2 and self.y > (height)//2:
            return 3
        elif self.x > (width)//2 and self.y > (height)//2:
            return 4
        else:
            return 0
    @property
    def position(self):
        return (self.x, self.y)
if __name__ == '__main__': 
    lines = []
    robots = []
    # for line in open('input'):
    quads = [0,0,0,0,0]
    width = 101
    height = 103
    for line_no, line in enumerate(open('input')):
    # width = 11
    # height = 7
    # for line_no, line in enumerate(open('example')):
        line = line.strip()
        match = re.search(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)', line)
        groups = match.groups()
        robot = Robot(
                int(groups[0]),
                int(groups[1]), 
                int(groups[2]), 
                int(groups[3]), 
                width,
                height
        )
        robot.simulate(100)
        # print(f'({robot.x},{robot.y}) {robot.quadrant}')
        robots.append(robot)
        quads[robot.quadrant] += 1

    
    print(quads)

    
    ans = quads[1] * quads[2] * quads[3] * quads[4]
    print(f'{ans = }')

    robots = []
    for line_no, line in enumerate(open('input')):
    # width = 11
    # height = 7
    # for line_no, line in enumerate(open('example')):
        line = line.strip()
        match = re.search(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)', line)
        groups = match.groups()
        robot = Robot(
                int(groups[0]),
                int(groups[1]), 
                int(groups[2]), 
                int(groups[3]), 
                width,
                height
        )
        # print(f'({robot.x},{robot.y}) {robot.quadrant}')
        robots.append(robot)


    generation = 0 
    dt = 0.05
    max_n = 0 
    while True:
        for robot in robots:
            robot.simulate(1)
        generation += 1
        display = []
        for y in range(height):
            line = []
            for x in range(width):
                line.append(' ')
            display.append(line)            
        positions = set((r.position for r in robots))
        for x in range(width):
            for y in range(height):
                if (x,y) in positions:
                    display[y][x] = '*'
        display = '\n'.join(''.join(l) for l in display)
        # time.sleep(dt)
        n = num_connections(positions)
        # print(f'{n = } {max_n = }') 
        if n > 800 and n > max_n:
            print(display)
            print(generation)
            __import__('pdb').set_trace()
            max_n = n
        if n > max_n:
            max_n = n
    print(quads)

    
    ans = quads[1] * quads[2] * quads[3] * quads[4]
    print(f'{ans = }')




