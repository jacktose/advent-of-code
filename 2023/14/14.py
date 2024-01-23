#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/14
Day 14: Parabolic Reflector Dish
"""

from functools import singledispatch
from typing import Sequence

def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data), '= 136?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 64?')
    
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = f.read().splitlines()
    return data

def part_1(data):
    '''Tilt the platform so that the rounded rocks all roll north.
    Afterward, what is the total load on the north support beams?'''
    return sum(load_e_row(row) for row in rotate_cw(tuple(data)))

@singledispatch
def rotate_cw(grid):
    raise TypeError('rotate_cw takes tuple or list')
@rotate_cw.register
def _(grid: tuple) -> tuple[str, ...]:
    return tuple(''.join(_) for _ in zip(*reversed(grid)))
@rotate_cw.register
def _(grid: list) -> list[list[str]]:
    return [list(_) for _ in zip(*reversed(grid))]

def load_e_grid(grid):
    return sum(load_e_row(row) for row in rotate_cw(grid))

def load_e_row(row: str) -> int:
    load = 0
    stones = 0
    for i, c in enumerate(row + '#', start=1):
        match c:
            case '.':
                continue
            case '#':
                load += sum(range(i-stones, i))
                stones = 0
            case 'O':
                stones += 1
    return load

def part_2(data: Sequence[Sequence[str]], cycles: int = 1_000_000_000) -> int:
    '''Run the spin cycle for 1000000000 cycles: North, West, South, East
    Afterward, what is the total load on the north support beams?'''
    grid: list[list[str]] = [list(row_str) for row_str in data]
    cache = {}
    i = 0; i_max = 4 * cycles
    while i < i_max:
        grid = rotate_cw(grid)
        tilt_e_grid(grid)  # in place
        grid_str = '\n'.join(''.join(row) for row in grid)
        if grid_str in cache:
            period = i - cache[grid_str]
            i = i_max - ((i_max - i) % period)
        else:
            cache[grid_str] = i
        i += 1
    return load_n_grid(grid)

def tilt_e_grid(grid: list[list[str]]) -> None:
    for row in grid:
        tilt_e(row)  # in place
    return None

def tilt_e(row: list[str]) -> None:
    target = len(row) - 1
    for i, c in etaremune(row):
        if c == 'O':
            row[i] = '.'
            row[target] = 'O'
            target -= 1
        elif c == '#':
            target = i - 1
    return None

def etaremune(sequence: Sequence):
    '''enumerate backward'''
    for n in reversed(range(len(sequence))):
        yield n, sequence[n]

def load_n_grid(grid) -> int:
    return sum(i * row.count('O') for (i, row) in enumerate(grid[::-1], start=1))
    

if __name__ == '__main__':
    import sys
    sys.exit(main())

