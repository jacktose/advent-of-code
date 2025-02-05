#!/usr/bin/env python3

"""
https://adventofcode.com/2024/day/15
Day 15: Warehouse Woes
"""

from __future__ import annotations
from collections.abc import Iterable
from typing import Any

import sys 
import os
sys.path.append(os.path.abspath('../../util'))
from Grid import Direction, Grid_Sparse, Point


def main():
    ex_data_1 = get_input('./example1.txt')
    ex_data_2 = get_input('./example2.txt')
    ex_data_3 = get_input('./example3.txt')
    data = get_input('./input.txt')
    
    print('example 1.1:', part_1(ex_data_1, verbose=True), '= 2028?')
    print('\nexample 1.2:', part_1(ex_data_2), '= 10092?')
    print('\npart 1:', part_1(data))

    print('\nexample 2.1:', part_2(ex_data_3, verbose=True), f'= {105+207+306}?')
    print('\nexample 2.2:', part_2(ex_data_2), '= 9021?')
    print('\npart 2:', part_2(data))

def get_input(file='./input.txt'):
    with open(file, 'r') as f:
        [grid_str, moves_str] = f.read().split('\n\n')
        moves = tuple(Direction.from_arrow(char) for char in moves_str if char != '\n')
    return grid_str, moves

def part_1(data, verbose: bool = False) -> int:
    '''Predict the motion of the robot and boxes in the warehouse.
    After the robot is finished moving, what is the sum of all boxes' GPS coordinates?'''
    grid_str, moves = data
    wh = Warehouse(grid_str, embiggener={})
    wh.do_moves(moves, verbose=verbose)
    return wh.gps_sum(target='O')

def part_2(data, verbose: bool = False) -> int:
    '''Predict the motion of the robot and boxes in this new, scaled-up warehouse.
    What is the sum of all boxes' final GPS coordinates?'''
    grid_str, moves = data
    wh = Warehouse(grid_str, embiggener = {'#': '##', 'O': '[]', '.': '..', '@': '@.'})
    wh.do_moves(moves, verbose=verbose)
    return wh.gps_sum(target='[')


class Warehouse(Grid_Sparse[str]):
    '''Represent a warehouse as a sparse grid, with extra methods for this puzzle.'''
    
    def __init__(self, string: str, embiggener: dict[str, str]|Any = {}, **kwargs):
        # Too complicated to fully type-hint embiggener. Let duck typing handle it.
        big_string = string.translate(str.maketrans(embiggener))
        super().__init__(big_string, bg_in='.', **kwargs)
        self.robot: Point = self.find('@')
    
    def do_moves(self, moves: Iterable[Direction], verbose: bool = False):
        '''Perform sequence of robot moves.'''
        vprint = print if verbose else lambda *args, **kwargs: None
        vprint('', self, '', sep='\n')
        for move in moves:
            self.move_robot(move)
            vprint(f'Move {move.arrow}:')
            vprint(self, end='\n\n')
        vprint(self)
    
    def move_robot(self, direction: Direction) -> bool:
        '''Try to move robot one step in direction. Move boxes if any.
        Return T/F whether bot moved.'''
        step: Point = self.robot + direction.velocity()
        match self.get(step, '.'):
            case '#':  # wall
                return False
            case '.':  # empty
                pass
            case 'O'|'['|']':  # box
                if not self.move_box(step, direction):
                    return False
            case other:
                raise ValueError(f'Invalid character: {step}: {other}')
        dest = {step: '@'}
        del self[self.robot]
        self.update(dest)
        self.robot = step
        return True
    
    def _get_box(self, location: Point) -> tuple[Point, ...]:
        '''Locations of all characters of box at this location.'''
        match self.get(location, '.'):
            case 'O': return (location,)
            case '[': return (location, location + (0, 1))
            case ']': return (location - (0, 1), location)
            case other:
                raise ValueError(f'Not a box character: {location}: {other}')
    
    def _get_neighbors(self, locations: Iterable[Point], direction: Direction) -> tuple[Point, ...]:
        '''All points adjacent to locations in direction.'''
        step = direction.velocity()
        return tuple(n for loc in locations if (n := loc+step) not in locations)

    def can_move_box(self, location: Point, direction: Direction) -> bool:
        '''Whether it's possible to move box at location in direction, and all affected boxes.'''
        box = self._get_box(location)
        neighbors = self._get_neighbors(box, direction)
        match tuple(self.get(n, '.') for n in neighbors):
            case ('.',) | ('.', '.'):  # empty
                return True
            case ('#',) | ('#', _) | (_, '#'):  # wall
                return False
            case ('O',) | ('[',) | (']',) | ('[', ']'):  # aligned box
                return self.can_move_box(neighbors[0], direction)
            case (']', '.'):  # single offset box
                return self.can_move_box(neighbors[0], direction)
            case ('.', '['):  # single offset box
                return self.can_move_box(neighbors[1], direction)
            case (']', '['):  # two offset boxen
                return all(self.can_move_box(box, direction) for box in neighbors)
            case other:
                raise ValueError(f'Invalid character(s): {neighbors}: {other}')
        
    def move_box(self, location: Point, direction: Direction) -> bool:
        '''Try to move box one step in direction. Move add'l boxes if any.
        Return T/F whether box moved.'''
        # Check if possible:
        if not self.can_move_box(location, direction):
            return False
        # Move neighbors (recurse):
        box = self._get_box(location)
        for neigh in self._get_neighbors(box, direction):
            if self.get(neigh, '.') in ('O', '[', ']'):
                self.move_box(neigh, direction)
        # Move self (finally!):
        step = direction.velocity()
        dest = {point+step: self[point] for point in box}
        for point in box:
            del self[point]
        self.update(dest)
        # It worked!
        return True

    def _gps(self, point: Point) -> int:
        '''The "GPS" coordinate of one point.'''
        return 100*point.row + point.col
    
    def gps_sum(self, target: str = 'O') -> int:
        '''The sum of "GPS" coordinates for all points matching target.'''
        return sum(self._gps(point) for point in self.find_all(target))
    
        
                
if __name__ == '__main__':
    import sys
    sys.exit(main())
