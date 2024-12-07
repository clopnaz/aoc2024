#!/usr/bin/env python3
import itertools
import pathlib
import logging
import re
import copy
import graphlib
import functools

logging.basicConfig(level=logging.DEBUG)

up = (-1, 0)
down = (1, 0)
left = (0, -1)
right = (0, 1)


def find_guard(lines):
    locs = tuple(
        (line_no, column_no, what_is_there)
        for line_no, line in enumerate(lines)
        for column_no, what_is_there in enumerate(line)
        if what_is_there in "<>v^"
    )
    assert len(locs) == 1
    return locs[0] 

def turned_guard(guard_dir):
    if guard_dir == '>':
        return 'v'
    elif guard_dir == '<':
        return '^'
    elif guard_dir == 'v':
        return '<'
    elif guard_dir == '^':
        return '>'

class LoopException(Exception):
    pass

class ExitException(Exception):
    pass

class World:
    def __init__(self, lines):
        self.lines = lines
        self.graph = graphlib.TopologicalSorter()
        # self.connections = {}
        # for stone_loc in self.stone_locs:
        #     self.connections[stone_loc] = self.get_connections(stone_loc)
        self.visited = set()
        self.guard_loc = find_guard(self.lines)
        self.visited.add(self.guard_loc)
        self.extra_stone = ()
        self.guard_loc_orig = self.guard_loc
        self.new_stone_results = dict()

    def __hash__(self):
        return hash((self.extra_stone, self.lines))

    def guard_dx(self):
        if self.guard_loc[2] == '>':
            dx = (0, 1)
        elif self.guard_loc[2] == '<':
            dx = (0, -1)
        elif self.guard_loc[2] == 'v':
            dx = (1, 0)
        elif self.guard_loc[2] == '^':
            dx = (-1, 0)
        return dx


    def front_of_guard(self):
        guard_loc = self.guard_loc
        guard_dx = self.guard_dx()
        try:
            xy = (guard_loc[0] + guard_dx[0], guard_loc[1] + guard_dx[1])
        except:
            __import__('pdb').set_trace()
        if self.extra_stone == xy:
            thing_in_front = '#'
        elif self.valid_index(row=xy[0], col=xy[1]):
            thing_in_front = self[xy[0], xy[1]]
        else:
            thing_in_front = 'exit'

        front_of_guard = (xy[0], xy[1], thing_in_front)
        return front_of_guard

    def step_guard(self):
        front_of_guard = self.front_of_guard()
        if front_of_guard[2] == '#':
            # turn the guard
            self.guard_loc = (self.guard_loc[0], self.guard_loc[1], turned_guard(self.guard_loc[2]))
            if self.guard_loc not in self.visited:
                self.visited.add(self.guard_loc)
            else:
                raise LoopException()
        elif front_of_guard[2] == 'exit':
            raise ExitException()
        else:
            self.guard_loc = (front_of_guard[0], front_of_guard[1], self.guard_loc[2])
            if self.guard_loc not in self.visited:
                self.visited.add(self.guard_loc)
            else:
                raise LoopException()
            self.visited.add(self.guard_loc)

    @property
    def stone_locs(self):
        x_max, y_max = self.shape
        return tuple(
            (x, y)
            for x in range(x_max)
            for y in range(y_max)
            if self.lines[x][y] == "#"
        )

    def __getitem__(self, slices):
        slice_rows = slices[0]
        slice_cols = slices[1]
        if isinstance(slice_rows, slice):
            return tuple(line[slice_cols] for line in self.lines[slice_rows])
        elif isinstance(slice_cols, slice):
            return tuple(self.lines[slice_rows][slice_cols])
        else:
            return self.lines[slice_rows][slice_cols]

    def valid_index(self, row=0, col=0):
        if row < 0:
            return False
        elif col < 0:
            return False
        elif row >= self.shape[0]:
            return False
        elif col >= self.shape[1]:
            return False
        else:
            return True

    def get_connections(self, stone_loc):
        """
        returns 4 connections, one for each direction the guard can approach the stone from
        the direction is like a long knight's move from the stone
        """
        connections = {}
        # from below
        row = stone_loc[0] + 1
        if self.valid_index(row=row):
            path = self[row, stone_loc[1] :]
            if "#" in path:
                connections["^"] = (row, path.index("#") + stone_loc[1], ">")
            else:
                connections["^"] = "exit"
        # from above
        row = stone_loc[0] - 1
        if self.valid_index(row=row):
            path = tuple(reversed(self[row, : stone_loc[1]]))
            if "#" in path:
                index = path.index("#")
                connections["v"] = (row, stone_loc[1] - index - 1, "<")
            else:
                connections["v"] = "exit"
        # from left
        col = stone_loc[1] - 1
        if self.valid_index(col=col):
            path = tuple(self[stone_loc[0] :, col])
            if "#" in path:
                index = path.index("#")
                connections[">"] = (stone_loc[0] + index, col, "v")
            else:
                connections[">"] = "exit"
        # from right
        col = stone_loc[1] + 1
        if self.valid_index(col=col):
            path = tuple(reversed(self[: stone_loc[0], col]))
            if "#" in path:
                index = path.index("#")
                connections["<"] = (stone_loc[0] - index - 1, col, "^")
            else:
                connections["<"] = "exit"
        for key in connections:
            if connections[key] == "exit":
                continue
            try:
                assert self[connections[key]] == "#"
            except:
                __import__("pdb").set_trace()
        return connections

    @property
    def shape(self):
        assert all((len(line) == len(self.lines[0]) for line in self.lines))
        return (len(self.lines), len(self.lines[0]))

    def build_graph(self):
        for stone in self.lines:
            pass

    def __str__(self):
        line_one = " " * 5 + "".join(str(num // 100) for num in range(self.shape[1]))
        line_two = " " * 5 + "".join(
            str(num % 100 // 10) for num in range(self.shape[1])
        )
        line_three = " " * 5 + "".join(str(num % 10) for num in range(self.shape[1]))
        return "\n".join(
            [line_one, line_two, line_three]
            + [
                f"{line_no:03d}: " + "".join(line)
                for line_no, line in enumerate(self.lines)
            ]
        )

    def __repr__(self):
        return "\n" + self.__str__()

    def unique_locations(self):
        return set(((visited[0], visited[1]) for visited in self.visited))

    def num_unique_locations(self):
        return len(self.unique_locations())

    def get_connection_from_2_loc(self, stone_loc, guard_loc):
        if stone_loc in self.stone_locs:
            return self.connections(guard_loc[2])
        else:
            raise Exception()

        assert(self.valid_index(row=stone_loc[0]))
        assert(self.valid_index(col=stone_loc[1]))
        assert(self.valid_index(row=guard_loc[0]))
        assert(self.valid_index(col=guard_loc[1]))
        dx = (stone_loc[0] - guard_loc[0], stone_loc[1] - guard_loc[1])
        assert(abs(dx[0])==1 ^ abs(dx[1])==1)
        if dx[0] < 0:
            guard_direction = 'v'
        elif dx[0] > 0:
            guard_direction = '^'
        
    def run(self):
        while True:
            try:
                self.step_guard()
            except ExitException:
                break

    def check_add_stone_loops(self):
        front_of_guard = self.front_of_guard()
        if front_of_guard[:2]  == self.guard_loc_orig[:2]:
            # can't put a stone where the guard started
            return False
        elif front_of_guard[2] == 'exit':
            return False
        else: 
            try:
                stone_check_id = front_of_guard[:2]
            except:
                __import__('pdb').set_trace()
            # if ((stone_check_id not in self.new_stone_results) or 
            #     (False and stone_check_id in self.new_stone_results and not self.new_stone_results[stone_check_id])):
            if stone_check_id not in self.new_stone_results:
                if stone_check_id in self.visited:
                    __import__('pdb').set_trace()
                new_world = World(self.lines)
                new_world.extra_stone = stone_check_id
                try:
                    new_world.run()
                    self.new_stone_results[stone_check_id] = False
                except LoopException: 
                    self.new_stone_results[stone_check_id] = True
                    print(self.num_looping_new_stones())
             
    def num_looping_new_stones(self):
        return len(set(key for key in self.new_stone_results if self.new_stone_results[key]))

    def run_2(self):
        steps = 0 
        while True:
            self.check_add_stone_loops()
            try:
                self.step_guard()
            except ExitException:
                break
            steps += 1
            print(f'{steps = }')



lines = tuple(tuple(line.strip()) for line in open('input'))
# lines = tuple(tuple(line.strip()) for line in open("example"))
world = World(lines)
world.run_2()
print(f"{world.num_looping_new_stones() = }")
__import__("pdb").set_trace()
print(f"{world = }")
print(f"{world.shape = }")
print(f"{world.stone_locs = }")
print(f"{world[0:2, :] = }")
print(f"{world.connections = }")
print(f"{world.num_unique_locations() = }")
