#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/13
Day 13: Point of Incidence
"""

from itertools import pairwise


def main():
    ex_data = get_input('./example.txt')
    data = get_input('./input.txt')
    
    print('example 1:')
    print(part_1(ex_data, debug=True), '= 405?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data, debug=True), '= 400?')
    
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input.txt'):
    with open(file, 'r') as f:
        data = tuple(tuple(p.splitlines()) for p in f.read().split('\n\n'))
    return data

def part_1(data, smudge_target=0, debug=False):
    '''Find the line of reflection in each of the patterns in your notes.
    What number do you get after summarizing all of your notes?'''
    tops = []; lefts = []
    for i, pattern in enumerate(data):
        if debug: print(f'{i}:')
        if top := find_mirror(pattern, smudge_target=0):
            if debug: print_w_horiz(pattern, top)
            tops.append(top)
        elif left := find_mirror(transpose(pattern), smudge_target=0):
            if debug: print_w_vert(pattern, left)
            lefts.append(left)
        else:
            breakpoint()
        if debug: print()
    return (100 * sum(tops)) + sum(lefts)

def part_2(data, debug=False):
    '''In each pattern, fix the smudge and find the different line of reflection.
    What number do you get after summarizing the new
    reflection line in each pattern in your notes?'''
    return part_1(data, smudge_target=1, debug=debug)

def transpose(grid):
    return tuple(''.join(c) for c in zip(*grid))

def find_mirror(pattern, smudge_target=1):
    for i, j in pairwise(range(len(pattern))):
        smudged = 0
        a = i+1; b = j-1
        while (smudged <= smudge_target
               and (a := a-1) >= 0
               and (b := b+1) < len(pattern)):
            smudged += differences(pattern[a], pattern[b])
        if smudged == smudge_target:
            return i + 1
    return None

def differences(line1, line2) -> int:
    return sum(x != y for (x, y) in zip(line1, line2))

def print_w_horiz(pattern, mirror):
    start = max(0, (2 * mirror) - len(pattern)) + 1
    end = min(len(pattern), (2 * mirror))
    for i, line in enumerate(pattern, start=1):
        color = reset = '\x1b[0m'
        if i == start:        char = ('┌', '┐')
        elif start < i < end: char = ('│', '│')
        elif i == end:        char = ('└', '┘')
        else:                 char = (' ', ' '); color = '\x1b[2m';
        print(f"{color}{i:>2}{char[0]}{line}{char[1]}{i:<2}{reset}")
        if i == mirror:
            print('  ├' + '┈'*len(line) + '┤ ')

def print_w_vert(pattern, mirror):
    width = len(pattern[0])
    start = max(0, (2 * mirror) - width)
    end = min(width, (2 * mirror))

    ones = ''.join(str(n%10) for n in range(1, width+1))
    ones = add_mirror_and_dim(ones, start, mirror, end, ' ')
    if width > 9:
        tens = ' '*9 + ''.join(str(n//10) for n in range(10, width+1))
        tens = add_mirror_and_dim(tens, start, mirror, end, ' ')
    else:
        tens = None
    top = (' ' * (start)
         + '┌' + '─' * (mirror - start - 1)
         + '┬' + '─' * (end - mirror - 1)
         + '┐' + ' ' * (width - end))
    bottom = top.translate(str.maketrans( '┌┬┐', '└┴┘'))

    if tens: print(tens)
    print(ones)
    print(top)
    for line in pattern:
        print(add_mirror_and_dim(line, start, mirror, end, '┊'))
    print(bottom)
    print(ones)
    if tens: print(tens)

def add_mirror_and_dim(string, start, mirror, end, m_char):
    dim = '\x1b[2m'
    reset = '\x1b[0m'
    return (
        dim + string[:start] + reset
        + string[start:mirror]
        + m_char
        + string[mirror:end]
        + dim + string[end:] + reset
    )


if __name__ == '__main__':
    import sys
    sys.exit(main())

