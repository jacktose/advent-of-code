#!/usr/bin/env python3

"""
https://adventofcode.com/2024/day/10
Day 10: Hoof It
"""

from __future__ import annotations

import sys 
import os
sys.path.append(os.path.abspath('../../util'))
from Grid import Grid_Immutable as Grid


def main():
    ex_data = get_input('./example.txt')
    data = get_input('./input.txt')
    
    print('example 1:')
    print(part_1(ex_data), '= 36?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 81?')
    
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input.txt'):
    with open(file, 'r') as f:
        data = Grid(f.read(), int)
    return data

def part_1(data: Grid) -> int:
    '''What is the sum of the *scores* of all trailheads on your topographic map?'''
    return sum(score(data, trailhead) for trailhead in data.find_all(0))

def score(grid: Grid[int], trailhead: tuple[int, int]) -> int:
    return len(ends(grid, *trailhead))

def ends(grid: Grid[int], start_row: int, start_col: int) -> set[tuple[int, int]]:
    TARGET = 9
    here_val = grid[start_row][start_col]
    if here_val == TARGET:
        return {(start_row, start_col)}
    # TODO: Better way to recurse and combine sets?
    return set().union(*(
        ends(grid, *neighbor)
        for neighbor, value in grid.neighbors(start_row, start_col)
        if value == here_val+1
    ))

def part_2(data: Grid) -> int:
    '''What is the sum of the *ratings* of all trailheads?'''
    return sum(rating(data, *trailhead) for trailhead in data.find_all(0))

def rating(grid: Grid[int], start_row: int, start_col: int) -> int:
    here_val = grid[start_row][start_col]
    if here_val == 9:
        return 1
    return sum(rating(grid, *neighbor) for neighbor, value in grid.neighbors(start_row, start_col) if value == here_val+1)


if __name__ == '__main__':
    import sys
    sys.exit(main())

