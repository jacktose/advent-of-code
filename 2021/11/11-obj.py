#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/11
Day 11: Dumbo Octopus
"""

import sys
from collections.abc import Generator, Sequence
import blessings  # type: ignore
t = blessings.Terminal()

def main():
    #print('example 0:')
    #demo_data = get_input('./demo')
    #print(part_1(demo_data, steps=2, debug=True), '= 9?\n')
    
    print('example 1:')
    print(part_1('./example.txt', debug=True), '= 1656?')
    
    print('\npart 1:')
    print(t.underline(str(part_1('./input.txt'))), 'flashes')
    
    print('\nexample 2:')
    print(part_2('./example.txt', debug=False), '= 195?')
    
    print('\npart 2:')
    print(t.underline(str(part_2('./input.txt'))), 'steps to sync')
    #breakpoint()

def part_1(input_file: str = './input.txt', steps: int = 100, debug=False):
    '''How many total flashes are there after 100 steps?'''
    data: Sequence[Sequence[int]] = get_input(input_file)
    octos: Octopodes = Octopodes(data)
    flashes: int = octos.step(100, debug=debug)
    return flashes

def part_2(input_file: str = './input.txt', debug=False):
    '''What is the first step during which all octopuses flash?'''
    data: Sequence[Sequence[int]] = get_input(input_file)
    octos: Octopodes = Octopodes(data)
    step, _ = octos.step(1_000_000, stop_when_synced=True, debug=debug)
    return step

def get_input(file: str ='./input.txt'):
    with open(file, 'r') as f:
        data: list[list[int]] = [[int(n) for n in line] for line in f.read().splitlines()]
    return data

class Octopus:
    def __init__(self, row: int, col: int, energy: int, parent: 'Octopodes') -> None:
        self.row: int = row
        self.col: int = col
        self.energy: int = energy
        self.parent: 'Octopodes' = parent
        self.flashed: bool = False
    
    def __repr__(self) -> str:
        return f'Octopus({self.row}, {self.col}, {self.energy})'
    
    def flash(self):
        '''Flash, check neighbors and flash (recursively) as required'''
        if self.energy < 10 or self.flashed:
            return
        # An octopus can only flash at most once per step:
        self.flashed = True
        #self.energy = -1  # already flashed
        # This increases the energy level of all adjacent octopuses by 1, including octopuses that are diagonally adjacent:
        for neighbor in self.neighbors():
            if not neighbor.flashed:
                neighbor.energy +=1
        # If this causes an octopus to have an energy level greater than 9, it also flashes:
        for neighbor in self.neighbors():
            if neighbor.energy >= 10:
                neighbor.flash()
                # This process continues [recursively] as long as new octopuses keep having their energy level increased beyond 9.
    
    def neighbors(self) -> Generator['Octopus', None, None]:
        '''All 8 grid neighbors, excluding self and out-of-bounds'''
        for r in (r for r in (self.row-1, self.row, self.row+1) if r >= 0 and r < self.parent.height):
            for c in (c for c in (self.col-1, self.col, self.col+1) if c >= 0 and c < self.parent.width):
                if r == self.row and c == self.col:
                    continue
                else:
                    yield self.parent.grid[r][c]

class Octopodes:
    '''A grid of dumbo “octopuses” and their flashy functions'''
    grid: list[list['Octopus']]
    def __init__(self, grid: Sequence[Sequence[int]]) -> None:
        self.grid: list[list['Octopus']] = [
            [Octopus(row_n, col_n, energy, self) for col_n, energy in enumerate(row)]
            for row_n, row in enumerate(grid)
        ]
        self.height: int = len(self.grid)
        self.width: int = len(self.grid[0])
        #self.flashes_tot: int = 0
    
    def __repr__(self) -> str:
        return f'Octopodes({repr(self.grid)})'
    
    def __str__(self) -> str:
        return '\n'.join(
            ' '.join(
                t.blink(t.bold(str(o.energy))) if o.energy == 0
                else str(o.energy)
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
            for octopus in self.all_octos():
                octopus.flashed = False
                octopus.energy += 1
            
            # Then, any octopus with an energy level greater than 9 flashes:
            for octopus in self.all_octos():
                if octopus.energy >= 10:
                    octopus.flash()
            
            # Finally, any octopus that flashed during this step has its energy level set to 0:
            for octopus in self.all_octos():
                if octopus.energy < 0 or octopus.flashed:
                    octopus.energy = 0
                    flashes += 1
                    #self.flashes_tot += 1
             
            if debug and (step+1 <= 10 or (step+1) % 10 == 0):
                print(f'After step {step+1}:', self, f'{flashes} flashes', sep='\n')
                debug = wait(debug)
            
            if stop_when_synced and self.synced:
                print(f'After step {step+1}:', self, f'{flashes} flashes', sep='\n')
                break
        
        return step+1, flashes
    
    def all_octos(self) -> Generator['Octopus', None, None]:
        '''Generate tuples of all coordinates in grid'''
        for row in self.grid:
            for o in row:
                yield o
    
    @property
    def synced(self) -> bool:
        '''Did all octopodes just flash?'''
        #return all(o.flashed for o in itertools.chain.from_iterable(self.grid))  # 800 nsec
        return all(all(o.flashed for o in row) for row in self.grid)  # 1000 nsec

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

