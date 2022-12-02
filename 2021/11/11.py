#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/11
Day 11: Dumbo Octopus
"""

import sys
from collections.abc import Generator, Iterable
import blessings  # type: ignore
t = blessings.Terminal()

def main():
    #print('example 0:')
    #demo_data = get_input('./demo')
    #print(part_1(demo_data, steps=2, debug=True), '= 9?\n')
    
    print('example 1:')
    print(part_1('./example', debug=True), '= 1656?')
    
    print('\npart 1:')
    print(t.underline(str(part_1('./input'))), 'flashes')
    
    print('\nexample 2:')
    print(part_2('./example', debug=False), '= 195?')
    
    print('\npart 2:')
    print(t.underline(str(part_2('./input'))), 'steps to sync')
    #breakpoint()

def part_1(input_file: str = './input', steps: int = 100, debug=False):
    '''How many total flashes are there after 100 steps?'''
    data: Iterable[Iterable[int]] = get_input(input_file)
    octos: Octopodes = Octopodes(data)
    octos.step(100, debug=debug)
    return octos.flashes

def part_2(input_file: str = './input', debug=False):
    '''What is the first step during which all octopuses flash?'''
    data: Iterable[Iterable[int]] = get_input(input_file)
    octos: Octopodes = Octopodes(data)
    step, _ = octos.step(1_000_000, stop_when_synced=True, debug=debug)
    return step

def get_input(file: str ='./input'):
    with open(file, 'r') as f:
        data: list[list[int]] = [[int(n) for n in line] for line in f.read().splitlines()]
    return data

class Octopodes:
    '''A grid of dumbo “octopuses” and their flashy functions'''
    def __init__(self, grid: Iterable[Iterable[int]]) -> None:
        self.grid: list[list[int]] = [list(row) for row in grid]
        self.height: int = len(self.grid)
        self.width: int = len(self.grid[0])
        self.flashes: int = 0
    
    def __repr__(self) -> str:
        return f'Octopodes({repr(self.grid)})'
    
    def __str__(self) -> str:
        return '\n'.join(
            ' '.join(
                t.blink(t.bold(str(o))) if o == 0
                else str(o)
                for o in row
            ) for row in self.grid
        )
    
    def step(self, n: int = 1, stop_when_synced: bool = False, debug: bool = False) -> tuple[int, int]:
        '''Increment octopus energies and count flashes'''
        flashes: int = 0
        if debug:
            print('Before any steps:', self, sep='\n')
            debug = wait(debug)
        
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
                print(f'After step {step+1}:', self, f'{self.flashes} flashes', sep='\n')
                debug = wait(debug)
            
            if stop_when_synced and self.synced:
                if debug: print(self)
                break
        
        return step+1, flashes
    
    def coords(self) -> Generator[tuple[int, int, int], None, None]:
        '''Generate tuples of all coordinates in grid'''
        for row in range(self.height):
            for col in range(self.width):
                yield row, col, self.grid[row][col]
    
    def neighbors(self, row: int, col: int) -> Generator[tuple[int, int], None, None]:
        '''All 8 grid neighbors, excluding self and out-of-bounds'''
        for r in (r for r in (row-1, row, row+1) if r >= 0 and r < self.height):
            for c in (c for c in (col-1, col, col+1) if c >= 0 and c < self.width):
                if r == row and c == col:
                    continue
                else:
                    yield r, c
    
    def flash(self, row: int, col: int) -> None:
        '''Flash octopus at given coords, check neighbors and flash (recursively) as required'''
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
                # This process continues [recursively] as long as new octopuses keep having their energy level increased beyond 9.
    
    @property
    def synced(self) -> bool:
        '''Did all octopodes just flash?'''
        #return all(o == 0 for o in itertools.chain.from_iterable(self.grid))  # 800 nsec
        return all(all(o == 0 for o in row) for row in self.grid)  # 1000 nsec

def wait(debug: bool = True) -> bool:
    '''Wait for keyboard input. If Ctrl-C or Ctrl-D, turn off debug and continue.'''
    try:
        input()
    except (KeyboardInterrupt, EOFError):
        print()
        return False  # turn off debug
    return debug

if __name__ == '__main__':
    sys.exit(main())

