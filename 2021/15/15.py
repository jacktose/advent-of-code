#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/15
Day 15: Chiton
"""

import sys
from functools import cache
import blessings
t = blessings.Terminal()

def main():
    myex_data = ((0, 1, 5),
                 (5, 1, 5),
                 (9, 1, 9))
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 0:')
    print(part_1(myex_data), '= 12?')
    
    print('example 1:')
    print(part_1(ex_data), '= 40?')
    
    #print('\npart 1:')
    #print(part_1(data))
    
    #print('\nexample 2:')
    #print(part_2(ex_data))
    
    #print('\npart 2:')
    #print(part_2(data))
    #breakpoint()

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = tuple(tuple(int(n) for n in line.rstrip()) for line in f)
    return data

def part_1(data):
    '''What is the lowest total risk of any path from the top left to the bottom right?'''
    print(grid_str(data, fancy=True))
    start = (0, 0)
    end = (len(data)-1, len(data[0])-1)
    #breakpoint()
    return min_path_risk(data, seen=(start,), end=end)

def part_2(data):
    '''assignment'''

@cache
def min_path_risk(data, seen, end):
    paths = []
    for nei in neighbors(data, seen[-1]):
        if nei == end:
            #breakpoint()
            return sum(data[row][col] for row, col in seen[1:]+(nei,))
        if nei not in seen:
            paths.append(min_path_risk(data, seen+(nei,), end))
    #breakpoint()
    try:
        return min(paths)
    except (ValueError, TypeError):
        return None

def neighbors(data, point):
    row, col = point
    for r, c in (row+1, col), (row, col+1), (row-1, col), (row, col-1):
        if 0 <= r < len(data) and 0 <= c < len(data[0]):
            yield r, c

def grid_str(data, fancy=False):
    if not fancy:
        return '\n'.join(''.join(str(n) for n in row) for row in data)
    n_rows, n_cols = len(data), len(data[0])  # assume at least a rectangle
    max_rows, max_cols = n_rows-1, n_cols-1
    data_strs = [[''] * n_cols for row in range(n_rows)]
    for row, row_data in enumerate(data):
        for col, n in enumerate(row_data):
            match (row, col, n):
                case 0, 0, _:
                    f = lambda _: t.green(str(_))
                case r, c, _ if r == max_rows and c == max_cols:
                    f = lambda _: t.red(str(_))
                case _, _, _:
                    f = str
            data_strs[row][col] = f(n)
    return '\n'.join(''.join(row) for row in data_strs)


if __name__ == '__main__':
    sys.exit(main())

