#!/usr/bin/env python3
import itertools
import pathlib
import logging
import re
import copy

logging.basicConfig(level=logging.DEBUG)


up = (-1, 0)
down = (1, 0) 
left = (0, -1) 
right = (0, 1)

ans = 0 
ans2 = 0 
def find_guard(lines):
    for line_no, line in enumerate(lines):
        match = re.search(r'v|\^|\>|\<', ''.join(line))
        if match is not None: 
            return  (line_no, match.span()[0])
    return None

# def replace_str(string, new, idx):
#     string = list(string)
#     string[idx] = new
#     return ''.join(string)

class LoopingException(Exception):
    pass

def turned_guard(lines):
    guard_pos = find_guard(lines)
    if guard_pos is None:
        return None
    guard_dir = lines[guard_pos[0]][guard_pos[1]]
    if guard_dir == '^':
        # up  -> right
        return '>'
    elif guard_dir == '>': 
        # right -> down 
        return 'v'
    elif guard_dir == 'v': 
        # down -> left
        return '<'
    elif guard_dir == '<': 
        # left -> up
        return '^'
    else:
        print('you goofed')
        __import__('pdb').set_trace()


def turn_guard(lines, guard_pos, prev_pos):
    # turn 90 degrees right
    guard_dir = lines[guard_pos[0]][guard_pos[1]]
    prev_pos[guard_dir][guard_pos[0]][guard_pos[1]] = 'X'
    if guard_dir == '^':
        # up  -> right
        lines[guard_pos[0]][guard_pos[1]] = '>'
        return lines
    elif guard_dir == '>': 
        # right -> down 
        lines[guard_pos[0]][guard_pos[1]] = 'v'
        return lines
    elif guard_dir == 'v': 
        # down -> left
        lines[guard_pos[0]][guard_pos[1]] = '<'
        return lines
    elif guard_dir == '<': 
        # left -> up
        lines[guard_pos[0]][guard_pos[1]] = '^'
        return lines
    else:
        print('you goofed')
        __import__('pdb').set_trace()
    
def is_obstructed(lines, front_pos):
    # oob = not obstructed
    if escaped(lines, front_pos):
        return False
    elif lines[front_pos[0]][front_pos[1]] == '#':
        return True
    else:
        return False

def get_front_pos(lines, guard_pos, guard_dir=None):
    if guard_dir == None:
        guard_dir = lines[guard_pos[0]][guard_pos[1]]
    if guard_dir == '^':
        # up 
        front_pos = (guard_pos[0] + up[0], guard_pos[1] + up[1])
    elif guard_dir == 'v': 
        # down
        front_pos = (guard_pos[0] + down[0], guard_pos[1] + down[1])
    elif guard_dir == '<': 
        # left
        front_pos = (guard_pos[0] + left[0], guard_pos[1] + left[1])
    elif guard_dir == '>': 
        # right
        front_pos = (guard_pos[0] + right[0], guard_pos[1] + right[1])
    else:
        print('you goofed')
        __import__('pdb').set_trace()
    assert (front_pos[0] != guard_pos[0]) or (front_pos[1] != guard_pos[1])
    return front_pos

def escaped(lines, front_pos):
    if front_pos[0] < 0:
        return True
    elif front_pos[1] < 0:
        return True
    elif front_pos[0] == len(lines):
        return True
    elif front_pos[1] == len(lines[front_pos[0]]):
        return True
    else:
        return False


def would_loop(lines, prev_pos):
    """
    if the guard has been somewhere on his right, facing his right, 
    he would definitely get back to where he is now if he went that way. 
    """
    guard_pos = find_guard(lines)
    if guard_pos is None:
        return False
    turned_dir = turned_guard(lines)
    turned_front_pos = get_front_pos(lines, guard_pos, guard_dir=turned_dir)
    if turned_dir == '>':
        to_his_right = prev_pos[turned_dir][guard_pos[0]][guard_pos[1]+1:]
    elif turned_dir == '<':
        to_his_right = reversed(prev_pos[turned_dir][guard_pos[0]][:guard_pos[1]])
    elif turned_dir == 'v':
        to_his_right = [prev_pos[turned_dir][n][guard_pos[1]] for n in range(guard_pos[0], len(prev_pos[turned_dir]))] 
    elif turned_dir == '^':
        to_his_right = [prev_pos[turned_dir][n][guard_pos[1]] for n in reversed(range(guard_pos[0]))]
    to_his_right = ''.join(to_his_right)
    if 'X' in to_his_right.split('#')[0]:
        return get_front_pos(lines, guard_pos)
    elif '#' not in to_his_right:
        return False
    else:
        try: 
            walk(lines, prev_pos, add_stones=False)
            return False
        except LoopingException:
            return True



def move_guard(lines, prev_pos):
    guard_pos = find_guard(lines)
    # get dir
    guard_dir = lines[guard_pos[0]][guard_pos[1]]
    # get new location
    front_pos = get_front_pos(lines, guard_pos)
    # remove guard
    prev_pos[guard_dir][guard_pos[0]][guard_pos[1]] = 'X'
    lines[guard_pos[0]][guard_pos[1]] = 'X'
    if not escaped(lines, front_pos):
        # add guard 
        lines[front_pos[0]][front_pos[1]] = guard_dir
    return lines

def am_i_looping(lines, prev_pos):
    guard_pos = find_guard(lines)
    if guard_pos is None:
        return False
    front_pos = get_front_pos(lines, guard_pos)
    guard_dir = lines[guard_pos[0]][guard_pos[1]]
    if guard_dir == '>':
        to_his_front = prev_pos[guard_dir][guard_pos[0]][guard_pos[1]+1:]
    elif guard_dir == '<':
        to_his_front = reversed(prev_pos[guard_dir][guard_pos[0]][:guard_pos[1]])
    elif guard_dir == 'v':
        to_his_front = [prev_pos[guard_dir][n][guard_pos[1]] for n in range(guard_pos[0], len(prev_pos[guard_dir]))] 
    elif guard_dir == '^':
        to_his_front = [prev_pos[guard_dir][n][guard_pos[1]] for n in reversed(range(guard_pos[0]))]
    to_his_front = ''.join(to_his_front)
    if 'X' in to_his_front.split('#')[0]:
        return True
    return False
def num_obstructions(lines):
    obs = 0
    for line in lines: 
        obs += line.count('#')
    return obs

def get_count(lines):
    ans = 0
    for line in lines: 
        ans += line.count('X')
    return ans

def walk(lines, prev_pos, add_stones=True):
    lines = copy.deepcopy(lines)
    prev_pos = copy.deepcopy(prev_pos)
    guard_pos = find_guard(lines)
    loops = []
    steps = 0 
    while guard_pos is not None:
        front_pos = get_front_pos(lines, guard_pos)
        had_to_turn = False
        while is_obstructed(lines, front_pos):
            had_to_turn = True
            lines = turn_guard(lines, guard_pos, prev_pos)
            front_pos = get_front_pos(lines, guard_pos)
            # __import__('pdb').set_trace()
        if had_to_turn:
            if add_stones:
                new_loop = would_loop(lines, prev_pos)
                if new_loop:
                    loops.append(new_loop)


        lines = move_guard(lines, prev_pos)
        steps += 1

        if add_stones:
            print(f'{steps = }')
            new_loop = would_loop(lines, prev_pos)
            if new_loop:
                loops.append(new_loop)
        else:
            if am_i_looping(lines, prev_pos):
                raise LoopingException()
        guard_pos = find_guard(lines)
    return lines, prev_pos, loops

def stat(lines):
    print('\n'.join([''.join(line) for line in lines]))


def main():
    lines = []
    with open('input') as fd:
    # with open('example') as fd:
        for line in fd:
            line = line.strip()
            lines.append(list(line))
    prev_pos = {
            '>': [list(line).copy() for line in lines.copy()],
            'v': [list(line).copy() for line in lines.copy()],
            '<': [list(line).copy() for line in lines.copy()],
            '^': [list(line).copy() for line in lines.copy()],
    }
    stat(lines)
    lines, prev_pos, loops = walk(lines, prev_pos)
    stat(lines)
    print(get_count(lines))
    print(f'loops: {loops}')
    print('5242?')
if __name__ == '__main__': 
    main()
