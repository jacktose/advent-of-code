#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/9
Day 9: Smoke Basin
"""

import sys

def main():
    ex_data = get_input('./example')
    data = get_input()

    print('example 1:')
    print(part_1(ex_data, debug=True))

    print('\npart 1:')
    print(part_1(data))

    #print('\nexample 2:')
    #print(part_2(ex_data, debug=True))

    #print('\npart 2:')
    #print(part_2(data))
    #breakpoint()

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = tuple(tuple(int(n) for n in line) for line in f.read().splitlines())
    return data

def part_1(data, debug=False):
    '''What is the sum of the risk levels of all low points on your heightmap?'''
    floor = Map(data)
    if debug: print(list(floor.low_points()))
    return floor.risk()

class Map:
    ''''''
    def __init__(self, points):
        self.points = points  # 2D array as tuple of tuples of ints
        self.height = len(self.points)
        self.width = len(self.points[0])
    
    def low_points(self):
        '''generator of low points on map'''
        for row in range(self.height):
            for col in range(self.width):
                if self._is_low_point(row, col):
                    yield ((row, col), self.points[row][col])
    
    def _is_low_point(self, row, col):
        p = self.points[row][col]
        if (
                (row == 0             or p < self.points[row-1][col])  # north
            and (row == self.height-1 or p < self.points[row+1][col])  # south
            and (col == 0             or p < self.points[row][col-1])  # west
            and (col == self.width-1  or p < self.points[row][col+1])  # east
        ):
            return True
    
    def risk(self):
        '''The risk level of a low point is 1 plus its height.'''
        return sum(p[1]+1 for p in self.low_points())


if __name__ == '__main__':
    sys.exit(main())

