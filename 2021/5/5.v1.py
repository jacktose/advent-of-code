#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/5
Day 5: Hydrothermal Venture
"""

import sys
import re
from collections import namedtuple, defaultdict
from functools import cached_property

PRINT_GRID = False

def main():
    data = get_input()
    print('part 1:')
    print(part_1(data, print_grid=PRINT_GRID))
    print('\npart 2:')
    print(part_2(data, print_grid=PRINT_GRID))

def get_input(file='./input.txt'):
    with open(file, 'r') as f:
        data = f.read().splitlines()
    return data

def part_1(data, print_grid=False):
    '''Rectalinear lines only'''
    lines = []
    for linestring in data:
        line = Line(linestring)
        if line.horizontal or line.vertical:
            lines.append(line)
    grid = Grid(lines)
    if print_grid: print(grid)
    return grid.intersections()

def part_2(data, print_grid=False):
    ''''''
    lines = [Line(linestring) for linestring in data]
    grid = Grid(lines)
    if print_grid: print(grid)
    return grid.intersections()


Point = namedtuple('Point', ['x', 'y'])

class Line:
    '''Two points of two dimensions'''
    def __init__(self, linestring):
        '''Construct from input data like "491,392 -> 34,392"'''
        self.x1, self.y1, self.x2, self.y2 = (int(n) for n in re.split(r'\D+', linestring))
    
    def __repr__(self):
        '''Line('491,392 -> 34,392')'''
        return f"Line('{self.__str__()}')"
    
    def __str__(self):
        '''491,392 -> 34,392'''
        return f'{self.x1},{self.y1} -> {self.x2},{self.y2}'
    
    @property
    def horizontal(self):
        return self.y1 == self.y2
    
    @property
    def vertical(self):
        return self.x1 == self.x2
    
    @property
    def diagonal(self):
        return not self.horizontal and not self.vertical
    
    @property
    def slope(self):
        if self.horizontal:
            return 0
        elif self.vertical:
            return None
        elif (self.x1 < self.x2) == (self.y1 < self.y2):
            return -1
        elif (self.x1 < self.x2) != (self.y1 < self.y2):
            return 1
    
    @property
    def left(self):
        return min(self.x1, self.x2)
    
    @property
    def right(self):
        return max(self.x1, self.x2)
    
    @property
    def top(self):
        return min(self.y1, self.y2)
    
    @property
    def bottom(self):
        return max(self.y1, self.y2)
    
    #@property
    @cached_property
    def points(self):
        if self.horizontal:
            return tuple((x,self.y1) for x in ri_range(self.x1, self.x2))
        elif self.vertical:
            return tuple((self.x1,y) for y in ri_range(self.y1, self.y2))
        else:
            return tuple(zip(
                ri_range(self.x1, self.x2),
                ri_range(self.y1, self.y2)
            ))


class Grid:
    ''''''
    def __init__(self, lines):
        # defaultdict is sparse (efficient), point value is effectively 0 until set
        # access with Grid.grid[x][y]
        self.grid = defaultdict(lambda: defaultdict(lambda: 0))
        for line in lines:
            for x, y in line.points:
                self.grid[x][y] += 1
        #breakpoint()
    
    def __str__(self):
        '''as in the example'''
        string = ''
        x_len, y_len = self.size
        # can't really use a comprehension because first order is columns
        for y in range(y_len):
            for x in range(x_len):
                #string += '.' if (self.grid[x][y] == 0) else self.grid[x][y], end=''
                match self.grid[x][y]:
                    case 0:
                        string += '.'
                    case 1:
                        string += '1'
                    case 2:
                        string += f'{c.bold}{c.blue}2{c.reset}'
                    case 3:
                        string += f'{c.bold}{c.green}3{c.reset}'
                    case 4:
                        string += f'{c.bold}{c.yellow}4{c.reset}'
                    case n if n > 4:
                        string += f'{c.bold}{c.red}{n}{c.reset}'
            string += '\n'
        return string.strip()
    
    @property
    def size(self):
        x_max = max(max(y.keys() for y in self.grid.values()))
        y_max = max(x for x in self.grid.keys())
        x_len, y_len = x_max+1, y_max+1
        return x_len, y_len
    
    def intersections(self):
        intersections = 0
        for col in self.grid.values():
            for n_lines in col.values():
                if n_lines > 1:
                    intersections += 1
        return intersections
    
    def points(self):
        return sum(len(col) for col in self.grid.values())


class c:
    '''
    Terminal color codes. Use like so:
    print(f'{c.red}warning!{c.reset}')
    '''
    reset =     '\033[0m'
    bold =      '\033[1m'
    underline = '\033[4m'
    red =       '\033[91m'
    green =     '\033[92m'
    yellow =    '\033[93m'
    blue =      '\033[94m'
    purple =    '\033[95m'
    cyan =      '\033[96m'


def ri_range(start, stop):
    '''Reversible, Inclusive range
    R: Make the range run backwards if it wants to!
    I: Go the extra step
    '''
    if stop >= start:
        return range(start, stop+1, 1)
    else:
        return range(start, stop-1, -1)


if __name__ == '__main__':
    sys.exit(main())

