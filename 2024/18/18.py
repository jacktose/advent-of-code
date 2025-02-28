#!/usr/bin/env python3

"""
https://adventofcode.com/2024/day/18
Day 18: RAM Run
"""

from collections.abc import Sequence
#from time import time

import sys; import os; sys.path.append(os.path.abspath('../../util'))
from Grid import Grid_Sparse, Point

def main():
    ex_data = get_input('./example.txt')
    data =    get_input('./input.txt')
    
    print(  'example 1:', part_1(ex_data, max=6, bytes=12), '= 22?')
    print('\npart 1:',    part_1(data))  # 280
    print('\nexample 2:', part_2(ex_data, max=6, known_good=12), '= 6,1?')
    print('\npart 2:',    part_2(data))  # 28,56

def get_input(file='./input.txt') -> tuple[Point, ...]:
    with open(file, 'r') as f:
        data = tuple(Point(r, c)
                     for line in f
                     for c, r in [map(int, line.split(','))])
    return data

def part_1(data: Sequence[Point], max: int = 70, bytes: int = 1024) -> int:
    '''Simulate the first kilobyte (1024 bytes) falling onto your memory space.
    Afterward, what is the minimum number of steps needed to reach the exit?'''
    grid: Grid_Sparse[str] = Grid_Sparse({point: '#' for point in data[:bytes]},
                                         dimensions=(max+1, max+1))
    return len(grid.bfs((0, 0), (max, max))) - 1

def part_2(data: Sequence[Point], max: int = 70, known_good: int = 1024) -> str:
    '''What are the coordinates of the first byte that will
    prevent the exit from being reachable from your starting position?'''
    #t_start = time()
    grid: Grid_Sparse[str] = Grid_Sparse({point: '#' for point in data[:known_good]},
                                         dimensions=(max+1, max+1))
    path: set[Point] = set(grid.bfs(start:=(0, 0), end:=(max, max)))
    # TODO: Try binary search instead of linear
    for point in data[known_good:]:
        grid[point] = '#'
        if point not in path:  # can't be the blocker
            continue
        path = set(grid.bfs(start, end))
        if not path:
            #t_end = time(); print(t_end - t_start)
            return f'{point.col},{point.row}'
    else:  # Dropped all points and still have a path
        raise RuntimeError('Path is not blocked')


if __name__ == '__main__':
    import sys
    sys.exit(main())
