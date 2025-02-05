#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/14
Day 14: Parabolic Reflector Dish
"""

from typing import Sequence

def main():
    ex_data = get_input('./example.txt')
    data = get_input('./input.txt')
    
    print('example 1:')
    print(part_1(ex_data), '= 136?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 64?')
    
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input.txt'):
    with open(file, 'r') as f:
        data = f.read().splitlines()
    return data

def part_1(data):
    '''Tilt the platform so that the rounded rocks all roll north.
    Afterward, what is the total load on the north support beams?'''
    return sum(load_e_row(row) for row in rotate_cw(tuple(data)))

def rotate_cw(grid: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(''.join(_) for _ in zip(*reversed(grid)))

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
    grid = Grid(data)
    cache = {}
    i = 0; i_max = 4 * cycles
    while i < i_max:
        grid.rotate_cw()
        grid.tilt_e()
        if (grid_str := str(grid)) in cache:
            period = i - cache[grid_str]
            remaining = i_max - i
            i = i_max - (remaining % period)
        else:
            cache[grid_str] = i
        i += 1
    return grid.load_n

class Grid:
    def __init__(self, grid: Sequence[Sequence[str]]):
        self._grid: list[list[str]] = [list(row) for row in grid]
    def __str__(self) -> str:
        return '\n'.join(''.join(row) for row in self._grid)

    def rotate_cw(self) -> None:
        self._grid = [list(_) for _ in zip(*reversed(self._grid))]

    @property
    def load_n(self) -> int:
        return sum(i * row.count('O') for (i, row) in enumerate(self._grid[::-1], start=1))

    def tilt_e(self) -> None:
        for row in self._grid:
            target = len(row) - 1
            for i, c in etaremune(row):
                if c == 'O':
                    row[i] = '.'
                    row[target] = 'O'
                    target -= 1
                elif c == '#':
                    target = i - 1

def etaremune(sequence: Sequence):
    '''enumerate backward'''
    for n in reversed(range(len(sequence))):
        yield n, sequence[n]
    

if __name__ == '__main__':
    import sys
    sys.exit(main())

