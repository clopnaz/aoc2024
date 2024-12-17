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


def path_locs(path):
    return [p[:2] for p in path]


class Machine:
    def __init__(self):
        self.registers = {"A": 0, "B": 0, "C": 0}
        self.instruction_pointer = 0
        self.program = []
        self.opcodes = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }
        self.output = []

    def reset(self): 
        self.registers = {"A": 0, "B": 0, "C": 0}
        self.instruction_pointer = 0
        self.output = []
    
    @property
    def done(self): 
        """ 
        if an output doesn't match, we're done
        if the length of the output is the same as the program, we're done
        """
        if len(self.output) == len(self.program):
            return True
        for out_no, out in enumerate(self.output): 
            if out != self.program[out_no]:
                return True
        return False
    
    @property
    def combo_operand(self):
        c = self.program[self.instruction_pointer+1]
        if 0 <= c <= 3:
            return c
        elif c == 4:
            return self.registers['A']
        elif c == 5:
            return self.registers['B']
        elif c == 6:
            return self.registers['C']
        else:
            assert c == 7, "WHAT"
            raise NotImplementedError()
    @property 
    def literal_operand(self):
        return self.program[self.instruction_pointer+1]

    def step(self):
        logging.debug(f'{self.instruction_pointer = } >= {len(self.program) = }')

        if self.instruction_pointer >= len(self.program):
            return False
        else:
            self.opcodes[self.program[self.instruction_pointer]]()
            return True

    def from_lines(self, lines):
        self.registers['A'] = int(lines[0].split(':')[1].strip())
        self.registers['B'] = int(lines[1].split(':')[1].strip())
        self.registers['C'] = int(lines[2].split(':')[1].strip())
        self.program = [int(n) for n in lines[4].split(':')[1].strip().split(',')]

    def adv(self):
        self.registers['A'] = int(self.registers['A'] / (2**(self.combo_operand)))
        self.instruction_pointer += 2


    def bxl(self):
        self.registers['B'] = self.registers['B'] ^ self.literal_operand
        self.instruction_pointer += 2
    
    def bst(self):
        self.registers['B'] = self.combo_operand % 8
        self.instruction_pointer += 2

    def jnz(self):
        if self.registers['A'] == 0: 
            logging.debug('no jump') 
            self.instruction_pointer += 2

        else:
            logging.debug('jump to %s', self.registers['A']) 
            self.instruction_pointer = self.literal_operand

    def bxc(self):
        self.registers['B'] = self.registers['B'] ^ self.registers['C']
        self.instruction_pointer += 2

    def out(self):
        self.output.append(self.combo_operand % 8)
        logging.debug(f'OUT({self.output[-1]}) {self.registers = }')
        self.instruction_pointer += 2

    def bdv(self):
        self.registers['B'] = int(self.registers['A'] / (2**(self.combo_operand)))
        self.instruction_pointer += 2

    def cdv(self):
        self.registers['C'] = int(self.registers['A'] / (2**(self.combo_operand)))
        self.instruction_pointer += 2

    def print(self):
        return ','.join([str(c) for c in self.output])
    
    def decode(self): 
        opcodes = {
            0: 'adv',
            1: 'bxl',
            2: 'bst',
            3: 'jnz',
            4: 'bxc',
            5: 'out',
            6: 'bdv',
            7: 'cdv',
        }
        output = []
        for ab in itertools.batched(self.program, 2): 
            output.append(opcodes[ab[0]])
            output.append(ab[1])
        return output


answer = (2,4,1,7,7,5,0,3,4,0,1,7,5,5,3,0)
def minimachine(A):
    B = 0
    C = 0 
    index = 0 
    while A!=0:
        B = A % 8
        B = B ^ 7 
        C = int(A / 2**B)
        A = int(A / 8) 
        B = B ^ C
        B = B ^ 7
        yield(B % 8) 

def minimachine_(A):
    B = 0
    C = 0 
    index = 0 
    while True:
        B = A % 8
        B = B ^ 7 
        C = int(A / 2**B)
        A = int(A / 8) 
        B = B ^ C
        B = B ^ 7
        out = B % 8
        __import__('pdb').set_trace()
        if int(out) == answer[index]:
            yield(B % 8) 
            index+=1
        else:
            break

@functools.cache
def minimachine2(A, B=0, C=0):
    if A==0: 
        return ()
    B = A % 8
    B = B ^ 7 
    C = int(A / 2**B)
    A = int(A / 8) 
    B = B ^ C
    B = B ^ 7
    return tuple((int(B%8),)) + minimachine2(A, B, C) 

# @functools.lru_cache(int(1e2))
def update_state(A, B, C): 
    B = A % 8
    B = B ^ 7 
    # C = A // 2**B
    C = A >> B
    A = A >> 3
    B = B ^ C
    B = B ^ 7
    return A,B,C


def minimachine3(A, B=0, C=0):
    index = 0 
    while True:
        A,B,C = update_state(A,B,C)
        out = B % 8
        if index < len(answer) and out == answer[index]:
            yield(out) 
            index+=1
        else:
            break
def update_state2(A,B,C):
    """
    B = A
    B = B ^ 7 
    C = int(A / 2**B)
    A = int(A / 8) 
    B = B ^ C
    B = B ^ 7
    print(B%8) 
    """
    """
    B = A ^ 7 
    C = A >> B
    A = A >> 3 
    B = (B ^ C) ^ 7
    print(B%8) 
    """
    B = ((A ^ 7) ^ (A >> (A ^ 7))) ^ 7
    A = A >> 3 
    print(B%8) 


def undo_state(A,output):
    A = A << 3 
    B = (A) ^ (A >> (A ^ 7))



if __name__ == "__main__":
    lines = []
    # for line_no, line in enumerate(open("example_2")):
    for line_no, line in enumerate(open("input")):
        line = line.strip()
        lines.append(line)
    m = Machine()
    m.from_lines(lines)
    print(m.decode())
    while m.step():
        pass
    print(m.print())

    # A = 0
    # while True:
    #     A += 1 
    #     m.reset()
    #     m.registers['A'] = A
    #     while m.step() and not m.done:
    #         pass
    #     if A % 10000 == 0:
    #         print(A)
    #         print(list(minimachine(A)))
    #         __import__('pdb').set_trace()
    #     if m.program == m.output:
    #         print(f'{A = }: {m.print()}') 
    #         __import__('pdb').set_trace()
    #         break
    # print(m.print())
    # A = int(35004600000000)
    i = 0
    longest = 0 

    while True:
        i+=1
        # I recognized the bit-shift operation (int(X/2^n) = X >> n)
        # way too late into the night. I was too tired for algebra, so I 
        # ran the following until I sucessively got a few more bytes 
        # of the solution, and then stuffed it into `A` to seed new guesses.
        A = 0b10010110010001110011011
        A = 0b101010010110010001110011011
        A += i << int.bit_length(A) 
        res = tuple(minimachine3(A))
        if len(res) > longest: 
            longest = len(res)
            print(f'new {longest = }: {A = }: {list(minimachine(A)) = }')
            print(f'{A = :>64b}')
        if res == answer:
            print('you did it') 
            __import__('pdb').set_trace()
        # if A % 100000000 == 0:
        #     print(f'{A = } {longest = }: {res = }')
        #     # print(f'{update_state.cache_info() = }')

    print(m.print())
