#!/usr/bin/env python3
import pdb

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

# the set of variables every wire depends on
variables = {
    wire: get_expression_variables(expression)
    for wire, expression in expanded_program.items()
}
# create a set of variables that z wires already depend on
# TODO: expand the program with wire names first. 
z_dependencies = set()
for z_key in z_keys:
    z_dependencies.update(variables[z_key])


for bad_bit in bad_bits:
    # get all the variables the bad bit depends on
    bad_expression = expanded_program[z_keys[bad_bit]]
    bad_wire_variables = get_expression_variables(expanded_program[z_keys[bad_bit]])
    # get every expression that depends on those variables
    possible_swap_wires = []
    for wire, wire_variables in variables.items():
        if set(bad_wire_variables) <= set(wire_variables):
            possible_swap_wires.append(wire)
    # don't swap with other z wires
    possible_swap_wires = [
        wire for wire in possible_swap_wires if not wire.startswith("z")
    ]
    # don't swap with other wires z wires depend on
    possible_swap_wires = [
        wire for wire in possible_swap_wires if wire not in z_dependencies
    ]

pdb.set_trace()
