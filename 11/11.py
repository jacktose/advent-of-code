#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/11
Day 11: Dumbo Octopus
"""

import sys
import itertools
from collections.abc import Generator, Iterable
import blessings
t = blessings.Terminal()

def main():
    #print('example 0:')
    #demo_data = get_input('./demo')
    #print(part_1(demo_data, steps=2, debug=True), '= 9?\n')
    
    print('example 1:')
    ex_data = get_input('./example')
    print(part_1(ex_data, debug=False), '= 1656?')
    
    print('\npart 1:')
    data = get_input('./input')
    print(part_1(data))
    
    print('\nexample 2:')
    ex_data = get_input('./example')
    print(part_2(ex_data, debug=False), '= 195?')
    
    print('\npart 2:')
    data = get_input('./input')
    print(part_2(data))
    #breakpoint()

def get_input(file: str ='./input'):
    with open(file, 'r') as f:
        data: list[list[int]] = [[int(n) for n in line] for line in f.read().splitlines()]
    return data

def part_1(data: Iterable[Iterable[int]], steps: int = 100, debug=False):
    '''How many total flashes are there after 100 steps?'''
    octos: Octopodes = Octopodes(data)
    octos.step(100, debug=debug)
    return octos.flashes

def part_2(data: Iterable[Iterable[int]], debug=False):
    '''What is the first step during which all octopuses flash?'''
    octos: Octopodes = Octopodes(data)
    step, _ = octos.step(1_000_000, stop_when_synced=True, debug=debug)
    return step

class Octopodes:
    def __init__(self, grid: Iterable[Iterable[int]]) -> None:
        self.grid: list[list[int]] = grid
        self.height: int = len(self.grid)
        self.width: int = len(self.grid[0])
        self.flashes: int = 0
    
    def __repr__(self) -> str:
        return f'Octopodes({repr(self.grid)})'
    
    def __str__(self) -> str:
        out: str = ''
        for row in self.grid:
            for o in row:
                if o == 0:
                    out += t.blink(t.bold(str(o)))
                else:
                    out += str(o)
                out += ' '
            out = out.rstrip()
            out += '\n'
        return out.rstrip()
    
    def step(self, n: int = 1, stop_when_synced=False, debug=False) -> int:
        ''''''
        flashes: int = 0
        if debug:
            print('Before any steps:', self, '', sep='\n')
            input()
        
        for step in range(n):
            # First, the energy level of each octopus increases by 1:
            for row, col, _ in self.coords():
                self.grid[row][col] += 1
            
            # Then, any octopus with an energy level greater than 9 flashes:
            for row, col, energy in self.coords():
                if energy >= 10:
                    self.flash(row, col)
            
            # Finally, any octopus that flashed during this step has its energy level set to 0:
            for row, col, energy in self.coords():
                if energy < 0:
                    self.grid[row][col] = 0
                    flashes += 1
             
            if debug and (step+1 <= 10 or (step+1) % 10 == 0):
                print(f'After step {step+1}:', self, f'{self.flashes} flashes', '', sep='\n')
                input()
            
            if stop_when_synced and self.synced:
                if debug: print(self)
                break
        
        return step+1, flashes
    
    def coords(self) -> Generator[tuple[int, int, int], None, None]:
        for row in range(self.height):
            for col in range(self.width):
                yield row, col, self.grid[row][col]
    
    def neighbors(self, row: int, col: int) -> Generator[tuple[int, int], None, None]:
        '''All 9 grid neighbors, including input because it doesn't matter'''
        for r in (r for r in (row-1, row, row+1) if r >= 0 and r < self.height):
            for c in (c for c in (col-1, col, col+1) if c >= 0 and c < self.width):
                if r == row and c == col:
                    continue
                else:
                    yield (r, c)
    
    def flash(self, row: int, col: int) -> None:
        ''''''
        if self.grid[row][col] < 10:
            return
        self.flashes += 1
        # An octopus can only flash at most once per step:
        self.grid[row][col] = -1  # already flashed
        # This increases the energy level of all adjacent octopuses by 1, including octopuses that are diagonally adjacent:
        for nrow, ncol in self.neighbors(row, col):
            if self.grid[nrow][ncol] >= 0:  # hasn't already flashed
                self.grid[nrow][ncol] +=1
        # If this causes an octopus to have an energy level greater than 9, it also flashes:
        for nrow, ncol in self.neighbors(row, col):
            if self.grid[nrow][ncol] >= 10:
                self.flash(nrow, ncol)
                # This process continues as long as new octopuses keep having their energy level increased beyond 9.
    
    @property
    def synced(self) -> bool:
        '''Did all octopodes just flash?'''
        return all(o == 0 for o in itertools.chain.from_iterable(self.grid))


if __name__ == '__main__':
    sys.exit(main())

