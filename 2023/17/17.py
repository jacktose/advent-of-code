#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/17
Day 17: Clumsy Crucible
"""

from dataclasses import dataclass
from itertools import pairwise
from math import inf
from typing import ClassVar, Sequence


def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data), '= 102?')
    
    #print('\npart 1:')
    #print(part_1(data))
    
    #print('\nexample 2:')
    #print(part_2(ex_data), '= _?')
    
    #print('\npart 2:')
    #print(part_2(data))

def get_input(file='./input'):
    with open(file, 'r') as f:
        #data = f.read().splitlines()
        data = {complex(r, c): int(v) for (r, row) in enumerate(f) for (c, v) in enumerate(row.rstrip())}
    return data

def part_1(data):
    '''Directing the crucible from the lava pool to the machine parts factory,
    but not moving more than three consecutive blocks in the same direction,
    what is the least heat loss it can incur?'''
    grid = Grid(data, start=(0+0j), end=None)
    return grid.recurse()

def part_2(data):
    '''assignment'''

count = 0

@dataclass
class Grid:
    values: dict[complex, int]
    start: complex = complex(0, 0)
    end: complex|None = None
    DIRS: ClassVar[Sequence[complex]] = ((-1+0j), (0+1j), (1+0j), (0-1j))  # N, E, S, W

    def __post_init__(self) -> None:
        #self.max_row: int = sum(1 for p in data if p.imag == 0) - 1
        #self.max_col: int = sum(1 for p in data if p.real == 0) - 1
        self.max_row: int = int(max(p.real for p in self.values if p.imag == 0))
        self.max_col: int = int(max(p.imag for p in self.values if p.real == 0))
        if self.end is None:
            self.end = complex(self.max_row, self.max_col)
        self.costs: dict[complex, int|float] = {v: inf for v in self.values.keys()}
        pass

    def in_bounds(self, point: complex) -> bool:
        return (0 <= point.real <= self.max_row) and (0 <= point.imag <= self.max_col)

    def possible_moves(self, path: list[complex], max_straight: int = 3) -> list[complex]:
        nogo = no_go_dirs(path, max_straight)
        poss = [path[-1] + dir for dir in self.DIRS if dir not in nogo]
        poss = [p for p in poss if self.in_bounds(p) and p not in path]
        return poss

    def recurse(self, path: list[complex]|None = None, cost: int = 0) -> int:
        global count
        count += 1
        if path is None:
            path = [self.start]
        if path[-1] == self.end:
            return cost + self.values[path[-1]]
        poss = self.possible_moves(path)
        if not poss:
            return inf
        costs = []
        for move in poss:
            new_path = path + [move]
            new_cost = self.recurse(new_path, cost + self.values[move])
            costs.append(new_cost)
        best = min(costs)
        return best
        #return min(self.recurse(path + [move], cost) for move in self.possible_moves(path))

def no_go_dirs(path: Sequence[complex], max_straight: int = 3) -> list[complex]:
    no_gos: list[complex] = []
    last_dirs = last_dirs_from_path(path, max_straight)
    try:
        no_gos.append(reverse(last_dirs[-1]))
    except IndexError:
        pass
    if (len(last_dirs) == max_straight
        and all(last_dirs[0] == d for d in last_dirs[1:])
       ):
        no_gos.append(last_dirs[0])
    return no_gos

def last_dirs_from_path(path: Sequence[complex], n: int = 3) -> list[complex]:
    return [p2 - p1 for p1, p2 in pairwise(path[-n-1:])]

def reverse(dir: complex) -> complex:
    return {
        (-1+0j): ( 1+0j),
        ( 0+1j): ( 0-1j),
        ( 1+0j): (-1+0j),
        ( 0-1j): ( 0+1j),
    }[dir]


if __name__ == '__main__':
    import sys
    sys.exit(main())

