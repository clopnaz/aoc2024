#!/usr/bin/env python3
import itertools
import pathlib
import logging
logging.basicConfig(level=logging.DEBUG)

num_safe = 0 
with open('input') as fd:
    for line in fd:
        line = line.strip()
        all_vals = [int(a) for a in line.split()]
        remove_index = -1
        while remove_index <= len(all_vals):
            if remove_index == -1:
                vals = all_vals
            else:
                vals = all_vals[:remove_index] + all_vals[remove_index+1:]
            safe = True
            increasing = False
            decreasing = False
            for a, b in itertools.pairwise(vals):
                if a == b: 
                    safe = False
                    break
                if a - b < 0: 
                    decreasing = True
                    if increasing:
                        safe = False
                        break
                if a - b > 0: 
                    increasing = True
                    if decreasing:
                        safe = False
                        break
                if abs(a - b) > 3: 
                    safe = False
                    break
            if safe:
                num_safe += 1
                break
            else:
                remove_index += 1
            
print(num_safe)

