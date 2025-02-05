#!/usr/bin/env python3

"""
https://adventofcode.com/2024/day/4
Day 4: Ceres Search
"""

from typing import NamedTuple

def main():
    ex_data = get_input('./example.txt')
    data = get_input('./input.txt')
    
    print('example 1:')
    print(part_1(ex_data), '= 18?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 9?')
    
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input.txt'):
    with open(file, 'r') as f:
        data = f.read().splitlines()
    return data

def part_1(data):
    '''Take a look at the little Elf's word search.
    How many times does XMAS appear?'''
    dirs = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    count = 0
    for row, letters in enumerate(data):
        for col, letter in enumerate(letters):
            if letter == 'X':
                for dir in dirs:
                    neighs = tuple(neighbors(data, (row,col), dir, length=3))
                    if ''.join(n[1] for n in neighs) == 'MAS':
                        count += 1
                        #display(data, ((row, col),) + tuple(n[0] for n in neighs))
                        #print((row, col), dir, '')
    return count

def neighbors(data, start, dir, length=3):
    loc = list(start)
    for _ in range(length):
        loc = vector_sum(loc, dir)
        if loc[0] < 0 or loc[1] < 0:
            return
        try:
            yield loc, data[loc[0]][loc[1]]
        except IndexError:
            return

def part_2(data):
    '''How many times does an X-MAS appear?'''
    count = 0
    for row, letters in enumerate(data):
        for col, letter in enumerate(letters):
            if letter == 'A':
                diags = tuple(diagonals(data, (row, col)))
                if all(''.join(loc[1] for loc in diag) in ('MS', 'SM') for diag in diags):
                    #display(data, ((row, col),) + tuple(loc[0] for diag in diags for loc in diag)); print()
                    count += 1
    return count

def diagonals(data, start):
    diags = (((-1, -1), (1, 1)), ((-1, 1), (1, -1)))
    for diag in diags:
        locs = []
        for delta in diag:
            loc = vector_sum(start, delta)
            if any(i < 0 for i in loc):
                continue
            try:
                locs.append((loc, data[loc[0]][loc[1]]))
            except IndexError:
                continue
        yield tuple(locs)

def vector_sum(a, b):
    return tuple(ai+bi for ai,bi in zip(a,b))


def display(data, highlight=None):
    if highlight is None: highlight = []
    for row, letters in enumerate(data):
        for col, letter in enumerate(letters):
            if (row, col) in highlight:
                print(style.BG.RED, style.FG.GREEN, style.BOLD, sep='', end='')
            print(data[row][col], style.RESET, sep='', end='')
        print()
    
class _fg(NamedTuple):
    BLACK =   '\x1b[30m'
    RED =     '\x1b[31m'
    GREEN =   '\x1b[32m'
    YELLOW =  '\x1b[33m'
    BLUE =    '\x1b[34m'
    MAGENTA = '\x1b[35m'
    CYAN =    '\x1b[36m'
    WHITE =   '\x1b[37m'

class _bg(NamedTuple):
    BLACK =   '\x1b[40m'
    RED =     '\x1b[41m'
    GREEN =   '\x1b[42m'
    YELLOW =  '\x1b[43m'
    BLUE =    '\x1b[44m'
    MAGENTA = '\x1b[45m'
    CYAN =    '\x1b[46m'
    WHITE =   '\x1b[47m'

class style(NamedTuple):
    RESET =         '\x1b[0m'
    BOLD =          '\x1b[1m'
    FAINT =         '\x1b[2m'
    ITALIC =        '\x1b[3m'
    UNDERLINED =    '\x1b[4m'
    INVERSE =       '\x1b[7m'
    STRIKETHROUGH = '\x1b[9m'
    FG = _fg
    BG = _bg

class control(NamedTuple):
    SHOW_CURSOR = '\x1b[?25h'
    HIDE_CURSOR = '\x1b[?25l'
    ERASE_CURSOR_TO_END = '\x1b[0J'
    ERASE_CURSOR_TO_START = '\x1b[1J'
    ERASE_SCREEN = '\x1b[2J'


if __name__ == '__main__':
    import sys
    sys.exit(main())

