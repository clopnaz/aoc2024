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
    elif x >= len(lines):
        return False
    elif y >= len(lines[x]):
        return False
    return True






class Maze:
    def __init__(self, lines, turn_cost=1000, move_cost=1):
        self.winners = []
        self.turn_cost = turn_cost
        self.move_cost = move_cost
        self.visited = {}
        self.paths = []
        self.lines = lines
        for row_no, row in enumerate(self.lines):
            for col_no, char in enumerate(row):
                if char == "E":
                    self.exit = (row_no, col_no)
                elif char == "S":
                    self.deer = (row_no, col_no, ">", 0)
        # init the search
        path = []
        path.append(self.deer)
        self.paths.append(path)
        self.visit(path) 
        self.dead_paths = []

    def check_visit(self, step): 
        if step[:3] not in self.visited: 
            return True
        elif self.visited[step[:3]] >= step[3]:
            return True
        else:
            return False


    def visit(self, steps): 
        for step in steps: 
            assert step[2] in dirs, f"visit({steps = })"
            if step[:3] in self.visited:
                assert self.visited[step[:3]] >= step[3]
                self.visited[step[:3]] = step[3]
            self.visited[step[:3]] = step[3]
    def turn_toward(self, curr_loc, dest_dir):
        """returns the least steps to turn toward an exit given
        a deer location/direction (location_x, location_y, direction_symbol)
        """
        curr_score = curr_loc[3]
        curr_dir = curr_loc[2]
        def gen_path(dirs):
            path = []
            score = curr_score
            for direction in dirs:
                score += self.turn_cost
                loc = (curr_loc[0], curr_loc[1], direction, score)
                path.append(loc) 
            return path
        if curr_dir == dest_dir: 
            return []
        elif dest_dir == '>' and curr_dir == '<': 
            path = gen_path(['v', '>']) 
        elif dest_dir == '<' and curr_dir == '>': 
            path = gen_path(['v', '<']) 
        elif dest_dir == 'v' and curr_dir == '^': 
            path = gen_path(['>', 'v']) 
        elif dest_dir == '^' and curr_dir == 'v': 
            path = gen_path(['>', '^']) 
        else: 
            path = gen_path([dest_dir])
        assert path[-1][2] == dest_dir, f"{path = }, {curr_dir = } {dest_dir = }"
        return path

    def exit_dirs(self, loc):
        exits = []
        for direction_symb in dirs:
            direction = dirs[direction_symb]
            potential_exit = (loc[0] + direction[0], loc[1] + direction[1])
            if self.loc_is_space(potential_exit):
                exits.append(direction_symb)
        return exits

    def loc_is_inside(self, loc):
        if loc[0] < 0:
            return False
        elif loc[1] < 0:
            return False
        elif loc[0] >= len(self.lines):
            return False
        elif loc[1] >= len(self.lines[loc[0]]):
            return False
        else:
            return True

    def loc_is_space(self, loc): 
        if self.loc_is_inside(loc) and self.lines[loc[0]][loc[1]] != "#":
            return True


    def step_path(self, path_no): 
        """ step the path or add a high score b.c. it's a deadend """ 
        path = self.paths[path_no]
        # step forward
        last_step = path[-1]
        new_step = (
                last_step[0] + dirs[last_step[2]][0],
                last_step[1] + dirs[last_step[2]][1],
                last_step[2],
                last_step[3] + self.move_cost,
        ) 
        if self.loc_is_space(new_step): 
            if self.check_visit(new_step): 
                self.visit([new_step]) 
                path.append(new_step)
            else:
                logging.debug("path %s is bad", path) 
                self.dead_paths.append(self.paths.pop(path_no))
        else:
            logging.debug("path %s hit dead end", path) 
            if last_step[:2] != self.exit:
                self.dead_paths.append(self.paths.pop(path_no))
            else:
                self.winners.append(self.paths.pop(path_no))

    def add_paths(self, path_no): 
        """ if deer can turn, add new paths """
        last_step = self.paths[path_no][-1]
        for exit_dir in self.exit_dirs(last_step):
            if exit_dir == last_step[2]:
                continue
            new_path = self.paths[path_no][:]
            turn_steps = self.turn_toward(last_step, exit_dir)
            if len(turn_steps) == 2:
                continue
            new_path.extend(turn_steps)
            if self.check_visit(new_path[-1]):
                self.paths.append(new_path)
                self.visit(turn_steps) 


    def path_score(self, path_no): 
        return self.paths[path_no][-1][3]

    def best_path_no(self):
        best_no = 0
        best_score = self.path_score(best_no) 
        for path_no in range(len(self.paths)):
            path_score = self.path_score(path_no)
            if path_score < best_score: 
                best_no = path_no
                best_score = path_score
        return best_no


    def search(self):
        path_no = self.best_path_no()
        self.add_paths(path_no)
        self.step_path(path_no) 

    def dbg_paths(self):
        logging.debug("best (%s): %s", self.best_path_no(), self.paths[self.best_path_no()])
    def score(self):
        return self.paths[self.best_path_no()][-1]

    def check(self): 
        for path_no, path in enumerate(self.paths): 
            endpoint = path[-1]
            if self.exit[0] == endpoint[0] and self.exit[1] == endpoint[1]:
                # that was all that was needed for part 1 
                if m.best_path_no == path_no:
                    return True
                else: 
                    return False
        return False

    def draw_path(self, path): 
        field = ''
        visited = {(l[0], l[1]) : l[2] for l in path}
        for row_no, row in enumerate(self.lines):
            for col_no, col in enumerate(row):
                if (row_no, col_no) in visited:
                    field += visited[row_no, col_no]
                else:
                    field += col
            field +=  '\n'
        print(field)            

def path_locs(path):
    return [p[:2] for p in path]

if __name__ == "__main__":
    lines = []
    for line_no, line in enumerate(open('input')):
    # for line_no, line in enumerate(open("example_1")):
        # for line_no, line in enumerate(open('example_2')):
        # for line_no, line in enumerate(open('example_3')):
        line = line.strip()
        lines.append(line)

    m = Maze(lines)
    logging.debug(f"{m.deer = }")
    logging.debug(f"{m.exit_dirs(m.deer) = }")
    m.dbg_paths()
    n = 0 
    while m.paths and not m.check():
        n+= 1
        m.dbg_paths()
        m.search()
    best_paths = []
    best_locs = set()
    for path in m.winners:
        if path[-1][:2] == m.exit and path[-1][3] == 108504:
            best_paths.append(path)
            best_locs.update([p[:2] for p in path])
    print(len(best_locs)) 

    __import__('pdb').set_trace()
