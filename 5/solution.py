#!/usr/bin/env python3
import itertools
import pathlib
import logging
import re
logging.basicConfig(level=logging.DEBUG)

with open('input') as fd:
# with open('example') as fd:
    lines = fd.read().splitlines()

ans = 0 
ans2 = 0 
rules = []
for line_no, line in enumerate(lines):
    line = line.strip()
    if '|' in line: 
        line = line.split('|') 
        rules.append(re.compile(f'(?P<one>{line[1]},)(?P<two>(:?\\d\\d,)*)(?P<three>{line[0]},)'))
    elif ',' in line:
        orig_nums = [int(num) for num in line.split(',')]
        line = line + ','
        def check_match(line, rules):
            # print(line)
            failing_rules = []
            for rule in rules:
                # print(rule)
                rematch = rule.search(line)
                if rematch is not None:
                    failing_rules.append(rule)
            # print(failing_rules)
            return failing_rules
        failing_rules = check_match(line, rules)
        if not failing_rules: 
            print('pass')
            nums = line.split(',')[:-1]
            ans += int(nums[len(nums)//2])
        if failing_rules:
            if line_no == 1182:
                __import__('pdb').set_trace()
            # print(line)
            def fix_line(line, rules):
                for rule in rules: 
                    if rule.search(line) is not None:
                        # __import__('pdb').set_trace()
                        line = rule.sub(r'\g<three>\g<one>\g<two>', line)
                return line
            wrong = 0 
            while failing_rules:
                line = fix_line(line, failing_rules)
                failing_rules = check_match(line, rules) 
                wrong += 1
            assert not check_match(line, rules) 
            nums = line.split(',')[:-1]
            new_nums = [int(num) for num in nums] 
            if len(nums) != len(orig_nums):
                __import__('pdb').set_trace()
            ans2 += int(nums[len(nums)//2])


    
print(ans)
print(ans2)

