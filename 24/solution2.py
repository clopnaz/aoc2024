#!/usr/bin/env python3
import pdb
import copy

important_bits = [7, 13, 18, 26]
my_swaps = (
        # z07
        # ('tgj', 'kbk') # carrying from z06 fails
        # ('bjm', 'njc'), # 

        # z18
        ('z18', 'skf'), 
        # ('z18', 'rrq'), # causes bad deps on many z wires
        # ('z18', 'tgm'), # bit doesn't get better

        # z26
        ('nvr', 'wkr'),
        # z13
        ('hsw', 'z13'),
        # z07
        ('bjm', 'z07'), # option 1 
        # ('z08', 'z07'), # option 2

)

# my_swaps = ()
bool_table = {
    "AND": lambda x, y: x & y,
    "OR": lambda x, y: x | y,
    "XOR": lambda x, y: x ^ y,
}


def expand(expression):
    if type(expression) == str:
        if expression[0] in ("x", "y", "z"):
            return expression
        else:
            return expand(program[expression])
    else:
        return (expand(expression[0]), expand(expression[1]), expression[2])


def show(expression, level=0):
    indent = "  " * level
    print(f"{indent}{expression[2]}(")
    if type(expression[0]) == str:
        print(f"{indent}  {expression[0]}, ")
    else:
        print(f"{indent}(")
        show(expression[0], level=level + 1)
    if type(expression[1]) == str:
        print(f"{indent}  {expression[1]}")
    else:
        show(expression[1], level=level + 1)
    print(f"{indent})")


def solve(expanded_expression, xy):
    if type(expanded_expression) == str:
        if expanded_expression[0] in ("x", "y"):
            return xy[expanded_expression]
        else:
            raise NotImplementedError()
    else:
        s = lambda x: solve(x, xy)
        ans = (
            s(expanded_expression[0]),
            s(expanded_expression[1]),
            expanded_expression[2],
        )
        if type(ans[0]) == type(ans[1]) == bool:
            return bool_table[ans[2]](ans[0], ans[1])
        else:
            return ans


def create_xy_zero():
    for key in inputs:
        if key.startswith("x"):
            xy[key] = False
        elif key.startswith("y"):
            xy[key] = False
        else:
            raise NotImplementedError()
    return xy


def create_xy(x=0, y=0):
    xy = {}
    for key_no in range(45):
        xy[f"x{key_no:02}"] = bool((x // 2**key_no) % 2)
        xy[f"y{key_no:02}"] = bool((y // 2**key_no) % 2)
    return xy


def get_expression_variables(expression):
    if isinstance(expression, str | bool):
        return (expression,)
    return get_expression_variables(expression[0]) + get_expression_variables(
        expression[1]
    )


inputs = {}
program = {}
with open("input") as fd:
    for line in fd:
        line = line.strip()
        if not line:
            break
        line = line.replace(":", "").split()
        inputs[line[0]] = bool(line[1])

    for line in fd:
        line = line.strip()
        line = line.replace(" ->", "")
        line = line.split()
        program[line[3]] = (line[0], line[2], line[1])

# do the swaps
for swap in my_swaps:
    hold_1 = program[swap[0]]
    hold_2 = program[swap[1]]
    program[swap[0]] = hold_2
    program[swap[1]] = hold_1
expanded_program = {}
for key in program:
    expanded_program[key] = expand(program[key])

z_keys = list((f"z{n:02}" for n in range(46)))


bad_bits = set()
# check sum / carry
for bit_no in range(45):
    z_key = z_keys[bit_no]
    # x
    xy = create_xy(2**bit_no, 0)
    if not solve(expanded_program[z_key], xy):
        bad_bits.add(bit_no)
    # y
    xy = create_xy(0, 2**bit_no)
    if not solve(expanded_program[z_key], xy):
        bad_bits.add(bit_no)
    # x and y (carry case #1)
    xy = create_xy(2**bit_no, 2**bit_no)
    if solve(expanded_program[z_key], xy):
        bad_bits.add(bit_no)
print(f'{bad_bits = }')

def bit_is_bad(bit_no):
    # try carry and sum 
    error_codes = []
    this_bit = 2**bit_no
    less_bit = 2**(bit_no-1)
    xy = create_xy(this_bit, 0)
    if not solve(expanded_program[z_keys[bit_no]], xy):
        error_codes.append(0)
    xy = create_xy(this_bit, this_bit)
    if solve(expanded_program[z_keys[bit_no]], xy):
        error_codes.append(1)
    if bit_no == 0:
        # there's no lesser bit to carry from
        return error_codes
    xy = create_xy(less_bit, less_bit)
    if not solve(expanded_program[z_keys[bit_no]], xy):
        error_codes.append(2)
    xy = create_xy(less_bit + this_bit, less_bit + this_bit)
    if not solve(expanded_program[z_keys[bit_no]], xy):
        error_codes.append(3)
    xy = create_xy(less_bit, less_bit + this_bit)
    if solve(expanded_program[z_keys[bit_no]], xy):
        error_codes.append(4)
    xy = create_xy(less_bit + this_bit, less_bit)
    if solve(expanded_program[z_keys[bit_no]], xy):
        error_codes.append(5)
    return error_codes

# the set of variables every wire depends on
variables = {
    wire: get_expression_variables(expression)
    for wire, expression in expanded_program.items()
}
# create a set of variables that z wires already depend on
# TODO: expand the program with wire names first. 
def get_all_deps(expression):
    if type(expression) == str:
        if expression[0] in ('x', 'y'):
            return (expression,)
        elif expression[0] == 'z':
            return get_all_deps(program[expression])
        else: 
            return (expression,) +  get_all_deps(program[expression])
    else:
        return get_all_deps(expression[0]) + get_all_deps(expression[1])

def get_all_wire_deps(expression): 
    if type(expression) == str:
        if expression[0] in ('x', 'y'):
            return (expression,)
        else: 
            return (expression,) +  get_all_wire_deps(program[expression])
    else:
        return (expression[0], expression[1], ) + get_all_wire_deps(expression[0]) + get_all_wire_deps(expression[1])

all_deps = {key : get_all_deps(key) for key in program}

all_wire_deps = {}
for key in program:
    all_wire_deps[key] = [d for d in get_all_wire_deps(key) if d[0] not in ('x', 'y')]


expected_deps = {}
for z_key_no in range(len(z_keys)):
    z_key = z_keys[z_key_no]
    expected_deps[z_key] = ()
    if z_key == 'z45':
        z_key_no -= 1
    for xy_key_no in range(z_key_no+1):
        expected_deps[z_key] += (f'x{xy_key_no:02}',)
        expected_deps[z_key] += (f'y{xy_key_no:02}',)

deps = {}
for key in program:
    deps[key] = tuple(dep for dep in get_all_deps(key) if dep[0] in ('x', 'y'))
for key, expression in expanded_program.items():
    if not key.startswith('z'):
        continue
    if set(deps[key]) != set(expected_deps[key]):
        print(f'{key} has bad dependencies!')
        for key2 in program:
            if set(deps[key2]) == set(expected_deps[key]):
                print(f'{key2} might be a better match')
for bit_no in range(2,44):
    if bit_is_bad(bit_no): 
        print(f'{bit_no = } is bad')
assert not bit_is_bad(18)
# assert bit_is_bad(7)
for bad_bit in bad_bits:
    z_key = z_keys[bad_bit]
    current_wires = set([d for d in all_wire_deps[z_key] if d[0] not in ('x', 'y')])
    # get a list of wires that *could* be part of this z wire
    expected_dep_set = set(expected_deps[z_key])
    if bad_bit == 7:

        # brute force, I guess
        possible_wires = set([d for d in all_wire_deps if d[0] not in ('x', 'y')])
    else:
        possible_wires = set([wire for wire, deplist in deps.items() if set(deplist) <= expected_dep_set])
    print(f'{bad_bit = }:  {len(current_wires) = }  {len(possible_wires) = }')
    pdb.set_trace()
    for swap_key_1 in possible_wires:
        for swap_key_2 in current_wires:
            swap_expression_1 = program[swap_key_1]
            swap_expression_2 = program[swap_key_2]
            program[swap_key_2] = swap_expression_1
            program[swap_key_1] = swap_expression_2
            try:
                expanded_program = {key : expand(expression) for key,expression in program.items()}
                if not bit_is_bad(bad_bit):
                    print(f'{bad_bit = } got better with {swap_key_1 = } and {swap_key_2 = }')
            except RecursionError:
                pass
            program[swap_key_1] = swap_expression_1
            program[swap_key_2] = swap_expression_2



answer = sorted([s for swap in my_swaps for s in swap])
print(','.join(answer))

