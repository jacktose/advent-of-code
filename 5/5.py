#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/5
Day 5: Hydrothermal Venture
"""

import sys
import re
from collections import defaultdict

def main():
    data = get_input()
    print('part 1:')
    print(part_1(data))
    #print('\npart 2:')
    #print(part_2(data))

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = f.read().splitlines()
    return data

def part_1(data):
    '''Rectalinear lines only'''
    lines = []
    for linestring in data:
        line = Line(linestring)
        if line.horizontal or line.vertical:
            lines.append(line)
    grid = Grid(lines)
    print(grid)
    return grid.intersections()

def part_2(data):
    ''''''
    lines = [Line(linestring) for linestring in data]
    x_max = max(line.right for line in lines)
    y_max = max(line.bottom for line in lines)
    print(f'{x_max=}, {y_max=}')
    
    return intersections(grid)


class Line:
    '''Two points of two dimensions'''
    def __init__(self, linestring):
        '''Construct from input data like "491,392 -> 34,392"'''
        self.x1, self.y1, self.x2, self.y2 = (int(n) for n in re.split(r'\D+', linestring))
    
    def __repr__(self):
        '''491,392 -> 34,392'''
        return f"Line('{self.x1},{self.y1} -> {self.x2},{self.y2}')"
    
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
    
    def contains(self, x, y):
        '''ASSUME RECTALINEAR'''
        if self.horizontal:
            return y == self.y1 and x >= self.left and x <= self.right
        elif self.vertical:
            return x == self.x1 and y >= self.top and y <= self.bottom
        else:
            raise NotImplementedError('can only do rectalinear for now')


class Grid:
    ''''''
    def __init__(self, lines):
        self.grid = defaultdict(lambda: defaultdict(lambda: 0))
        for line in lines:
            if line.horizontal:
                for x in range(line.left, line.right+1):
                    self.grid[x][line.y1] += 1
            elif line.vertical:
                for y in range(line.top, line.bottom+1):
                    self.grid[line.x1][y] += 1
            else:
                raise NotImplementedError('can only do rectalinear for now')
    
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
    
    def __str__(self):
        '''as in the example'''
        string = ''
        x_len, y_len = self.size()
        # can't really use a comprehension because first order is columns
        for x in range(x_len):
            for y in range(y_len):
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
                        string += f'{c.bold}{c.red}5{c.reset}'
            string += '\n'
        return string.strip()


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


if __name__ == '__main__':
    sys.exit(main())

