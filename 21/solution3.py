import itertools
import functools
import heapq


numpad_tuple = (("7", "8", "9"), ("4", "5", "6"), ("1", "2", "3"), (None, "0", "A"))
dpad_tuple = ((None, "^", "A"), ("<", "v", ">"))
numpad = {(row_no, col_no): col for row_no, row in enumerate(numpad_tuple) for col_no, col in enumerate(row)}
inumpad = {val: key for key,val in numpad.items()}
numpad.update(inumpad)
dpad = {(row_no, col_no): col for row_no, row in enumerate(dpad_tuple) for col_no, col in enumerate(row)}
idpad = {val: key for key,val in dpad.items()}
dpad.update(idpad)

def valid_index(x, y, pad):
    if (x,y) in pad: 
        if pad[x,y] is not None:
            return True
    return False

def displacement(button1, button2, pad=dpad):
    a = pad[button1]
    b = pad[button2]
    return (b[0] - a[0], b[1] - a[1])

def disp2arrows(disp):
    arrows = ''
    if disp[0] < 0:
        arrows += '^' * -disp[0]
    else:
        arrows += 'v' * disp[0]
    if disp[1] < 0:
        arrows += '<' * -disp[1]
    else:
        arrows += '>' * disp[1]
    return arrows

up = (-1, 0)
down = (1, 0)
left = (0, -1)
right = (0, 1)
# dirs = (up, down, left, right)
dirs = {"^": up, "v": down, "<": left, ">": right}
inv_dirs = {value: key for key,value in dirs.items()}

@functools.cache
def nextmoves(curr_pos, padname):
    if padname=='dpad':
        pad = dpad
    elif padname=='numpad':
        pad = numpad
    else:
        raise NotImplementedError()
    moves = ()
    for dx, arrow in inv_dirs.items():
        new_pos = (curr_pos[0]+dx[0], curr_pos[1]+dx[1])
        if valid_index(new_pos[0], new_pos[1], pad):
            moves += ((new_pos, arrow),)
    return moves


@functools.cache
def shortest_presses(pair, pad_no=2, not_first_pad=False):
    if not_first_pad: 
        pad = dpad
        padname = 'dpad'
    else:
        pad = numpad
        padname = 'numpad'
    moves = [('', pair[0])]
    while not any((move[1]==pair[1] for move in moves)):
        moves = [(c+new_c, pad[new_p]) for c, b in moves for new_p, new_c in nextmoves(pad[b], padname)]
    moves_options = tuple([move + 'A' for move, pos in moves if pos==pair[1]])
    if pad_no:
        presses_options = []
        for moves_option in moves_options:
            moves_option = 'A' + moves_option 
            presses = ''
            for pair in itertools.pairwise(moves_option):
                presses += shortest_presses(pair, pad_no=pad_no-1, not_first_pad=True)
            presses_options.append(presses)
        return sorted(presses_options, key=len)[0]
    else:
        return sorted(moves_options, key=len)[0]

    
@functools.cache
def shortest_length(pair, pad_no=2, not_first_pad=False):
    if not_first_pad: 
        pad = dpad
        padname = 'dpad'
    else:
        pad = numpad
        padname = 'numpad'
    moves = [('', pair[0])]
    while not any((move[1]==pair[1] for move in moves)):
        moves = [(c+new_c, pad[new_p]) for c, b in moves for new_p, new_c in nextmoves(pad[b], padname)]
    moves_options = tuple([move + 'A' for move, pos in moves if pos==pair[1]])
    if pad_no:
        lengths = []
        for moves_option in moves_options:
            moves_option = 'A' + moves_option 
            length = 0 
            for pair in itertools.pairwise(moves_option):
                length += shortest_length(pair, pad_no=pad_no-1, not_first_pad=True)
            lengths.append(length)
        return min(lengths)
    else:
        return len(sorted(moves_options, key=len)[0])



if __name__ == '__main__':
    # combos = open('example').read().splitlines()
    combos = open('input').read().splitlines()
    ans_1 = 0
    ans_2 = 0
    for combo in combos:
        presses = ''
        num_presses_check = 0 
        num_presses_25 = 0 
        for pair in itertools.pairwise('A' + combo):
            presses += shortest_presses(pair)
            num_presses_check += shortest_length(pair) 
            num_presses_25 += shortest_length(pair, pad_no=25) 

        assert len(presses) == num_presses_check
        ans_1 += len(presses) * int(combo[:3])
        ans_2 += num_presses_25 * int(combo[:3])
        print(f'{combo}: {len(presses) = } {int(combo[1:3]) = } {num_presses_25 = }')
    print(f'{ans_1 = }')
    print(f'{ans_2 = }')
