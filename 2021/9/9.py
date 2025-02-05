#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/9
Day 9: Smoke Basin
"""

import sys
import math
from collections.abc import Generator, Iterable

def main():
    ex_data = get_input('./example.txt')
    data = get_input()
    
    print('example 1:')
    print(part_1(ex_data, debug=True), '= 15?')
    
    print('\npart 1:')
    print(part_1(data), '= 524?')
    
    print('\nexample 2:')
    print(part_2(ex_data, debug=True), '= 1134?')
    
    print('\npart 2:')
    print(part_2(data, debug=True), '= 1235430?')

def get_input(file='./input.txt') -> tuple[tuple[int, ...], ...]:
    with open(file, 'r') as f:
        data = tuple(tuple(int(n) for n in line) for line in f.read().splitlines())
    return data

def part_1(data: tuple[tuple[int, ...], ...], debug=False) -> int:
    '''What is the sum of the risk levels of all low points on your heightmap?'''
    floor = Map(data)
    if debug: print('low points:', list(floor.low_points()))
    return floor.risk()

def part_2(data: tuple[tuple[int, ...], ...], debug=False) -> int:
    '''What do you get if you multiply together the sizes of the three largest basins?'''
    floor = Map(data)
    if debug:
        basins = list(floor.basins())
        print('basin sizes:', basins)
        print('largest 3:', sorted(basins)[-3:])
    basins = floor.basins()
    return math.prod(sorted(basins)[-3:])

class Map:
    '''2D array of seafloor, with puzzling funcs'''
    def __init__(self, points: tuple[tuple[int, ...], ...]) -> None:
        self.points: tuple[tuple[int, ...], ...] = points  # 2D array as tuple of tuples of ints
        self.height: int = len(self.points)
        self.width: int = len(self.points[0])
    
    def low_points(self) -> Generator[tuple[int, int, int], None, None]:
        '''generator of low points on map'''
        for row in range(self.height):
            for col in range(self.width):
                if self._is_low_point(row, col):
                    yield (row, col, self.points[row][col])
    
    def _is_low_point(self, row: int, col: int, _=None) -> bool:
        '''is it lower than all 2–4 orthogonal neighbors?'''
        return all(self.points[row][col] < a[2] for a in self.adj(row, col))
    
    def adj(self, row: int, col: int, _=None) -> Generator[tuple[int, int, int], None, None]:
        '''generator of orthogonal neighbors'''
        for r, c in ((row-1, col),  # north
                     (row+1, col),  # south
                     (row, col-1),  # west
                     (row, col+1)): # east
            if (0 <= r < self.height) and (0 <= c < self.width):
                yield (r, c, self.points[r][c])
    
    def risk(self) -> int:
        '''The risk level of a low point is 1 plus its height.'''
        return sum(p[2]+1 for p in self.low_points())
    
    def basins(self) -> Generator[int, None, None]:
        '''generator of sizes of basins'''
        for low_point in self.low_points():
            yield self._basin_size(low_point)
    
    def _basin_size(self, initial_point: tuple[int, int, int]) -> int:
        '''given a (low?) point, count the points in its basin'''
        basin_maybe = {initial_point}
        basin_yes = set()
        while basin_maybe:
            p = basin_maybe.pop()
            if p[2] < 9:  # 9s are basin borders and not included
                basin_yes.add(p)
                basin_maybe.update(p for p in self.adj(*p) if p not in basin_yes)
        return len(basin_yes)


if __name__ == '__main__':
    sys.exit(main())

