#!/usr/bin/env python
import pdb
import itertools
import functools
import pprint
import copy
import collections

lines = ()
# for line in open('example'):
# for line in open('example_2'):
# for line in open('input'):
# for line in open('input'):
for line in open('input2'):
# for line in open('input_fixed'):
    line = line.strip()
    lines = lines + (line,) 

# print('\n'.join(lines))


class Adder():
    def __init__(self, lines):
        self.inputs = {}
        lineiter = iter(lines)
        for line in lineiter:
            if not line:
                break
            line = line.split(':')
            self.inputs[line[0]] = bool(int(line[1]))

        self.program = {}
        for line in lineiter:
            line = line.strip()
            # print(line)
            line = line.split('->')
            line = [l.strip() for l in line]
            instruction = line[0].split()
            inp1 = instruction[0]
            inp2 = instruction[2]
            operator = instruction[1]
            output = line[1]

            progout = (inp1, inp2, operator)
            # print(progout)
            self.program[output] = progout
        self.orig_program = copy.deepcopy(self.program)
        self.orig_inputs = copy.deepcopy(self.inputs)
        # print(program)    

    def run(self):
        self.orig_program = copy.deepcopy(self.program)
        z_keys = [key for key in sorted(list(self.program.keys())) if key.startswith('z')]
        self.z_keys = z_keys

        n=0 
        while any([type(self.program[key]) != bool for key in self.z_keys]):
            n+=1
            for out_wire in self.program:
                self.program[out_wire] = self.calculate(self.program[out_wire])
            if n > 50:
                raise NotImplemented()
        
        # pprint.pprint(program)
        output = 0
        for key_no, key in enumerate(self.z_keys):
            # print(f'self.program[{key}] = {self.program[key]}')
            assert type(self.program[key]) == bool, f'{self.program}, {key}'
            # print(program[key])
            output += 2**key_no * self.program[key]
        return output

    def reset(self):
        self.program = copy.deepcopy(self.orig_program)

    def calculate(self, instruction):
        if type(instruction) == bool:
            return instruction
        instruction = list(instruction)
        a = self.substitute(instruction[0])
        b = self.substitute(instruction[1])
        operator = instruction[2]
        if type(a) == bool and type(b) == bool:
            if operator == 'AND':
                return a and b 
            elif operator == 'OR': 
                return a or b
            elif operator == 'XOR':
                return (a or b) and not (a and b)
        else:
            return instruction

    def substitute(self, key):
        if key in self.inputs:
            return self.inputs[key]
        elif key in self.program and type(self.program[key]) == bool:
            return self.program[key]
        return key

    def get_bad_wires(self):
        """ 
        check the sum at each position matches its inputs, for all combinations of input 
        I think I can get away with not knowing adder designs, if I run every possible input
        where only one bit is "on", then mark down which output bits are wrong and when.
        """
        saved_program  = copy.deepcopy(self.program)

        # (NOTE: last input bit is like x44, output is z45)
        bad_sum = collections.defaultdict(set)
        bad_carry = collections.defaultdict(set)

        # x only: output bits should match input bits. the 46 should be 0
        for n in range(1, 45):
            # self.reset()
            self.program = copy.deepcopy(saved_program)
            inpx = 2**n
            inpy = 0
            self.setinp(bin(inpx), bin(inpy))
            ans_z = self.run()
            ans_expected = inpx + inpy
            if ans_expected != ans_z:
                bin_x = f'{inpx:045b}'
                bin_y = f'{inpy:045b}'
                bin_z = f'{ans_z:045b}'
                bin_expected = f'{ans_expected:045b}'
                bin_no = 0 
                for bit_x, bit_z in zip(reversed(bin_x), reversed(bin_z)):
                    if bit_x != bit_z:
                        if bit_x == '1':
                            bad_sum[bin_no].add('x')
                        else:
                            bad_carry[bin_no].add('x')
                    bin_no += 1

        for n in range(1, 45):
            self.program = copy.deepcopy(saved_program)
            inpy = 2**n
            inpx = 0
            self.setinp(bin(inpx), bin(inpy))
            ans_z = self.run()
            ans_expected = inpx + inpy
            if ans_expected != ans_z:
                bin_x = f'{inpx:045b}'
                bin_y = f'{inpy:045b}'
                bin_z = f'{ans_z:045b}'
                bin_expected = f'{ans_expected:045b}'
                bin_no = 0 
                bin_no = 0 
                for bit_y, bit_z in zip(reversed(bin_y), reversed(bin_z)):
                    if bit_y != bit_z:
                        if bit_y == '1':
                            bad_sum[bin_no].add('y')
                        else:
                            bad_carry[bin_no].add('y')
                    bin_no += 1

        for n in range(1, 45):
            self.program = copy.deepcopy(saved_program)
            inpy = 2**n
            inpx = 2**n
            self.setinp(bin(inpx), bin(inpy))
            ans_z = self.run()
            ans_expected = inpx + inpy
            if ans_expected != ans_z:
                bin_x = f'{inpx:045b}'
                bin_y = f'{inpy:045b}'
                bin_z = f'{ans_z:045b}'
                bin_expected = f'{ans_expected:045b}'
                bin_no = 0 
                bin_no = 0 
                for bit_y, bit_z in zip(reversed(bin_y), reversed(bin_z)):
                    if bit_y != bit_z:
                        if bit_y == '1':
                            bad_sum[bin_no].add('y')
                        else:
                            bad_carry[bin_no].add('y')
                    bin_no += 1

        return bad_sum, bad_carry

    def setinp(self, valx, valy):
        assert valx.startswith('0b') 
        valx = valx[2:]
        assert valy.startswith('0b') 
        valy = valy[2:]

        valx = list(reversed(valx))
        valy = list(reversed(valy))
        self.inputs = {}
        for n in range(45):
            self.inputs[f'x{n:02}'] = False
        for n in range(45):
            self.inputs[f'y{n:02}'] = False
        for n, val in enumerate(valx):
            self.inputs[f'x{n:02}'] = bool(int(val))
        for n, val in enumerate(valy):
            self.inputs[f'y{n:02}'] = bool(int(val))
        return self.inputs

    def calculate_2(self, instruction):
        if type(instruction) == bool:
            return instruction
        elif type(instruction) == str:
            if instruction in self.program:
                return self.calculate_2(self.program[instruction]) # + (instruction,)
            else: 
                return instruction
        elif type(instruction) == tuple:
            a = self.calculate_2(instruction[0])
            b = self.calculate_2(instruction[1])
            operator = instruction[2]
            try:
                return tuple(sorted([a, b], key=depth)) + (operator,)
            except:
                pdb.set_trace()
        else:
            pdb.set_trace()

adder = Adder(lines)
part_1_ans = adder.run()
print(f'{part_1_ans = }')
# inputs = setinp('0b0', '0b' + '1'*45)
# inputs = setinp('0b0', '0b1111111111111')
# inputs = setinp('0b' + '1'*45, '0b0')
# inputs = setinp('0b' + '1'*45, '0b' + '1'*45)
# pprint.pprint(inputs)
# print(inputs)

print('part 2')

# pdb.set_trace()


    
def depth(a):
    if type(a) == tuple:
        return 1 + max(depth(a[0]), depth(a[1]))
    else: 
        return 1



# for key in sorted(calculated.keys()):
#     print()
#     print(key)
#     pprint.pprint(calculated[key])
#     pdb.set_trace()

def num1():
    keys = sorted([key for key in inputs if key.startswith('x')])
    s = 0 
    for key_no, key in enumerate(keys):
        assert type(inputs[key]) == bool, f'{key = } {inputs[key] = }'
        if inputs[key]:
            s += 2**key_no 
    return s

def num2():
    keys = sorted([key for key in inputs if key.startswith('y')])
    s = 0 
    for key_no, key in enumerate(keys):
        assert type(inputs[key]) == bool, f'{key = } {inputs[key] = }'
        if inputs[key]:
            s += 2**key_no 
    return s

def wrongstr():
    """ indicate which part of the output is wrong for these inputs """
    bin_num1 = f'{num1():050b}'
    bin_num2 = f'{num2():050b}'
    bin_correct = f'{num1()+num2():050b}'
    bin_fake = f'{output:050b}'
    wstr = ''
    ones_str = ''
    tens_str = ''
    bit_no = 0 
    for cbit, fbit in zip(bin_correct, bin_fake):
        if cbit != fbit:
            wstr += 'x'
        else:
            wstr += ' '
        ones_str += str(bit_no % 10)
        tens_str += str(bit_no // 10)
        bit_no += 1
    ones_str = ''.join(reversed(ones_str))
    tens_str = ''.join(reversed(tens_str))
    print(bin_num1)
    print(bin_num2)
    print(bin_correct)
    print(bin_fake) 
    print(wstr)
    print(tens_str)
    print(ones_str)
# wrongstr()

# def instruction_keys(instruction):
#     keys = set()
#     for instr in [instruction[0], instruction[1]]:
#         if type(instr) == tuple:
#             keys.update(instruction_keys(instr))
#         else: 
#             keys.add(instr)
#     return keys

# for key_no, key in enumerate(calculated):
#     x[key_no] = f'x{key_no:02}'
#     y[key_no] = f'y{key_no:02}'
#     if key_no == 0:
#         self_bit[key_no] = (x[key_no], y[key_no], 'XOR') 
#         carry_bit[key_no] = (x[key_no], y[key_no], 'AND') 
#     else:
#         self_bit[key_no] = (carry_bit[key_no-1], (x[key_no], y[key_no], 'XOR'), 'XOR')
#         carry_bit[key_no] = ((x[key_no], y[key_no], 'AND'), ((x[key_no], y[key_no], 'XOR'), carry_bit[key_no-1], 'AND'), 'OR')
#     print()
#     # pprint.pprint(self_bit[key_no])
#     # print(self_bit[key_no])
#     # pprint.pprint(carry_bit[key_no])
#     # pprint.pprint(calculated[key])
#     # print(calculated[key])
#     pdb.set_trace()

n = 0
for wire_1, wire_2 in itertools.combinations(sorted(adder.program.keys()), 2):
    n+=1 
print(n)

adder.reset()
# orig_program = copy.deepcopy(adder.program)
# bad_wires = adder.get_bad_wires()
# print(bad_wires)
# adder.reset()
# wire_1 = 'njc'
# wire_2 = 'bjm'
# instruction_1 = adder.program[wire_1]
# instruction_2 = adder.program[wire_2]
# adder.program[wire_2] = instruction_1
# adder.program[wire_1] = instruction_2
# bad_wires = adder.get_bad_wires()
# print(bad_wires)
# exit()
# ans = adder.calculate_2(adder.program['z18'])
n = 0 
# len_1 = len(bad_wires[0])
# len_2 = len(bad_wires[1])
orig_bad_wires = adder.get_bad_wires()
pprint.pprint(orig_bad_wires)
# for wire_1, wire_2 in itertools.combinations(sorted(adder.program.keys()), 2):
#     # if not set(['njc', 'bjm']) == set([wire_1, wire_2]):
#     if not 'z18' in set([wire_1, wire_2]):
#         continue
#     print(f'{wire_1 =} {wire_2 = }')
#     test_adder = Adder(lines)
#     n += 1 
#     if n % 1000 == 0: 
#         print(f'{n = }')
#     # orig_bad_wires = test_adder.get_bad_wires()
#     test_adder.reset()
#     instruction_1 = test_adder.program[wire_1]
#     instruction_2 = test_adder.program[wire_2]
#     test_adder.program[wire_2] = instruction_1
#     test_adder.program[wire_1] = instruction_2
#     new_bad_wires = test_adder.get_bad_wires()
#     if len(new_bad_wires[0]) < 1:
#         pprint.pprint(new_bad_wires[0])
#         pdb.set_trace()
#         pass
#     # if len(bad_wires[0]) < len_1:
#     #     print(wire_1)
#     #     print(wire_2)
#     #     print(bad_wires)
#     #     pdb.set_trace()
#     #     pass


pdb.set_trace()
swaps = (
        ('njc', 'bjm'),
        ('wkr', 'nvr'),
        # ('qjc', 'z18'),
        ('rrq', 'z18'),
        ('hsw', 'z13'),
)

print('check') 
adder = Adder(lines)
swapped_cables = set()
for swap in swaps:
    swapped_cables.update(swap)
    a = adder.program[swap[0]] 
    b = adder.program[swap[1]]
    adder.program[swap[1]] = a
    adder.program[swap[0]] = b
pprint.pprint(adder.get_bad_wires())
print(','.join(sorted(swapped_cables)))



