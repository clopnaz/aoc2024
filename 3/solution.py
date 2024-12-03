#!/usr/bin/env python3
import itertools
import pathlib
import logging
import re
logging.basicConfig(level=logging.DEBUG)

answer_1 = 0
with open('input') as fd:
    line = fd.read()
    matches = re.finditer(r'mul\((\d+),(\d+)\)', line)
    for match in matches:
        answer_1 +=  int(match.groups()[0]) * int(match.groups()[1])
    # split on don't() and then do() and then append rest
    more = True
    while more:
        [line, _, rest] = line.partition('don\'t()')
        [_, _, more] = rest.partition('do()') 
        line += more
        print(len(more))
    matches = re.finditer(r'mul\((\d+),(\d+)\)', line)
    for match in matches:
        answer_2 +=  int(match.groups()[0]) * int(match.groups()[1])
    matches = re.finditer(r'mul\((\d+),(\d+)\)', line)
    for match in matches:
        answer +=  int(match.groups()[0]) * int(match.groups()[1])
print(answer)
