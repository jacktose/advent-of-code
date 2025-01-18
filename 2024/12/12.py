#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/12
Day 12: Garden Groups
"""

from collections.abc import Collection, Generator
from itertools import pairwise
from typing import Any

import sys 
import os
sys.path.append(os.path.abspath('../../util'))
from Grid import Grid_Immutable as Grid


def main():
    ex_data_1 = get_input('./example1')
    ex_data_2 = get_input('./example2')
    ex_data_3 = get_input('./example3')
    ex_data_4 = get_input('./example4')
    ex_data_5 = get_input('./example5')
    data = get_input('./input')
    
    print('example 1-1:')
    print(part_1(ex_data_1), '= 140?')
    print('example 1-2:')
    print(part_1(ex_data_2), '= 772?')
    print('example 1-3:')
    print(part_1(ex_data_3), '= 1930?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2-1:')
    print(part_2(ex_data_1), '= 80?')
    print('example 2-2:')
    print(part_2(ex_data_2), '= 436?')
    print('example 2-3:')
    print(part_2(ex_data_3), '= 1206?')
    print('example 2-4:')
    print(part_2(ex_data_4), '= 236?')
    print('example 2-5:')
    print(part_2(ex_data_5), '= 368?')
    
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input'):
    with open(file, 'r') as f:
        data: Grid[str] = Grid(f.read())
    return data

def part_1(data: Grid[Any]) -> int:
    '''What is the total price of fencing all regions on your map?
    price = area * perimiter'''
    return sum(len(region) * perimiter(region) for region in get_regions(data))

def part_2(data: Grid[Any]):
    '''What is the new total price of fencing all regions on your map?
    price = area * sides'''
    return sum(len(region) * sides(region) for region in get_regions(data))

def get_regions(data: Grid[Any]) -> Generator[Collection[tuple[int, int]]]:
    assigned = set()
    for point, _ in data.iter_all():
        if point in assigned:
            continue
        region = data.contiguous(*point)
        assigned.update(region)
        yield region

def neighbors(point: tuple[int, int]) -> Generator[tuple[int, int]]:
    '''Generate all possible (rectalinear) neighbors of a point.'''
    row, col = point
    for d_row, d_col in ((-1, 0), (0, 1), (1, 0), (0, -1)):
        yield row+d_row, col+d_col

def perimiter(region: Collection[tuple[int, int]]) -> int:
    '''Calculate the perimiter of a region.'''
    return sum(1 for point in region for neighbor in neighbors(point) if neighbor not in region)

def sides(region: Collection[tuple[int, int]]) -> int:
    '''Calculate the number of sides of a region.'''
    # Find points that have borders above, below, left, and right
    #above = []; below = []; left = []; right = []
    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
    borders = {d: [] for d in directions}
    for point in region:
        for (d_row, d_col), members in borders.items():
            if (point[0] + d_row, point[1] + d_col) not in region:
                members.append(point)

    # Sort the lists of border points and count runs of contiguous border points, i.e. sides
    sides = 4  # There's at least one in each direction. Then find any more:
    for (d_row, d_col), members in borders.items():
        if d_row == 0:  # left & right neighbors, i.e. vertical borders
            # Rotate points so we can treat them all the same:
            members = [(c, r) for (r, c) in members]
        members.sort()  # sort by row, then column
        for (r1, c1), (r2, c2) in pairwise(members):
            if r1 != r2 or c2 - c1 != 1:
                sides += 1
    return sides


if __name__ == '__main__':
    import sys
    sys.exit(main())
