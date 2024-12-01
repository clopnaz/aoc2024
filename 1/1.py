#!/usr/bin/env python3

import pathlib
import logging
logging.basicConfig(level=logging.DEBUG)

list_one = []
list_two = []
with open('input.txt') as fd:
    for line in fd:
        line = line.strip()
        logging.debug('line: %s', line)
        list_one.append(int(line.split()[0]))
        list_two.append(int(line.split()[1]))
        logging.debug('%s, %s', list_one[-1], list_two[-1])

distance_sum = 0 
for item_one, item_two in zip(sorted(list_one), sorted(list_two)):
    distance_sum += abs(item_one - item_two)
print(distance_sum)


similarity_score = 0 
for item_one in list_one:
    occurrances = sum([1 for item_two in list_two if item_one == item_two])
    similarity_score += occurrances * item_one
print(similarity_score)
