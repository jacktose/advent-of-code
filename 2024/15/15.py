#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/15
Day 15: Warehouse Woes
"""

from __future__ import annotations
from collections.abc import Sequence

import sys 
import os
sys.path.append(os.path.abspath('../../util'))
from Grid import Direction, Grid, Grid_Sparse, Point


def main():
    ex_data_1 = get_input('./example1')
    ex_data_2 = get_input('./example2')
    ex_data_3 = get_input2('./example3')
    ex_data_2_2 = get_input2('./example2')
    data = get_input('./input')
    data2 = get_input2('./input')
    
    print('example 1.1:', part_1(ex_data_1), '= 2028?')
    print('\nexample 1.2:', part_1(ex_data_2), '= 10092?')
    print('\npart 1:', part_1(data))
    print('\nexample 2.1:', part_2(ex_data_3), f'= {105+207+306}?')
    print('\nexample 2.2:', part_2(ex_data_2_2), '= 9021?')
    print('\npart 2:', part_2(data2))

def get_input(file='./input'):
    with open(file, 'r') as f:
        [grid_str, moves_str] = f.read().split('\n\n')
        warehouse = Warehouse.from_string(grid_str)
        moves = tuple(Direction.from_arrow(char) for char in moves_str if char != '\n')
    return warehouse, moves
def get_input2(file='./input'):
    with open(file, 'r') as f:
        [grid_str, moves_str] = f.read().split('\n\n')
        warehouse = Warehouse_Big(grid_str)
        moves = tuple(Direction.from_arrow(char) for char in moves_str if char != '\n')
    return warehouse, moves

def part_1(data) -> int:
    '''Predict the motion of the robot and boxes in the warehouse.
    After the robot is finished moving, what is the sum of all boxes' GPS coordinates?'''
    wh, moves = data
    last_direction: Direction = Direction.E
    for move in moves:
        #wh.print()
        wh.rotate(move, last_direction)  # always move east
        last_direction = move
        robot = next(wh.find('@'))
        try:
            empty = wh[robot.row].index('.', robot.col+1)
            wall = wh[robot.row].index('#', robot.col+1)
        except ValueError:
            continue
        if wall < empty:
            continue
        wh[robot.row][robot.col:empty+1] = ['.'] + wh[robot.row][robot.col:empty]
    wh.rotate(Direction.E, last_direction)
    wh.print()
    return wh.gps_sum()

def part_2(data) -> int:
    '''Predict the motion of the robot and boxes in this new, scaled-up warehouse.
    What is the sum of all boxes' final GPS coordinates?'''
    wh, moves = data
    #print(wh, end='\n\n')
    for move in moves:
        wh.move_robot(move)
        #print(f'Move {move.arrow}:')
        #print(wh, end='\n\n')
    print(wh)
    return wh.gps_sum()

class Warehouse(Grid):
    '''Represent a warehouse as a mutable Grid, with extra methods for this puzzle.'''

    def _gps(self, point: Point) -> int:
        return 100*point.row + point.col

    def gps_sum(self) -> int:
        return sum(self._gps(point) for point in self.find('O'))

class Warehouse_Big(Grid_Sparse[str]):
    '''Represent a warehouse as a sparse grid, with extra methods for this puzzle.'''
    
    EMBIGGENER = {'#': '##', 'O': '[]', '.': '..', '@': '@.'}

    def __init__(self, string: str, **kwargs):
        embiggener_trans = str.maketrans(self.EMBIGGENER)
        return super().__init__(string.translate(embiggener_trans), bg_in='.', **kwargs)
    
    def _gps(self, point: Point) -> int:
        return 100*point.row + point.col
    
    def gps_sum(self, target: str = '[') -> int:
        return sum(self._gps(point) for point in self.find_all(target))
    
    @property
    def robot(self) -> Point:
        return self.find('@')
    
    def move_robot(self, direction: Direction) -> bool:
        '''Try to move robot one step in direction. Move boxes if any.
        Return T/F whether bot moved.'''
        robot: Point = self.robot
        step: Point = robot + direction.velocity()
        match self.get(step, '.'):
            case '#':  # wall
                return False
            case '.':  # empty
                pass
            case '['|']':  # box
                if not self.move_box(step, direction):
                    return False
            case _:
                raise ValueError
        self[step] = '@'
        del self[robot]
        return True
    
    def _get_box(self, location: Point) -> tuple[Point, Point]:
        match self.get(location, '.'):
            case '[':
                return (location, location + (0, 1))
            case ']':
                return (location - (0, 1), location)
            case other:
                raise ValueError(f'Not a box character: {location}: {other}')
    
    def _get_neighbors(self, locations: Sequence[Point], direction: Direction) -> tuple[Point, ...]:
        step = direction.velocity()
        return tuple(n for loc in locations if (n := loc+step) not in locations)

    def can_move_box(self, location: Point, direction: Direction) -> bool:
        box = self._get_box(location)
        #step = direction.velocity()
        neighbors = self._get_neighbors(box, direction)
        match tuple(self.get(n, '.') for n in neighbors):
            case ('.',) | ('.', '.'):
                return True
            case ('#',) | ('#', _) | (_, '#'):
                return False
            case ('[',) | (']',) | ('[', ']'):
                return self.can_move_box(neighbors[0], direction)
            case (']', '.'):
                return self.can_move_box(neighbors[0], direction)
            case ('.', '['):
                return self.can_move_box(neighbors[1], direction)
            case (']', '['):
                return all(self.can_move_box(box, direction) for box in neighbors)
            case _:
                raise ValueError
        
    def move_box(self, location: Point, direction: Direction) -> bool:
        '''Try to move box one step in direction. Move add'l boxes if any.
        Return T/F whether box moved.'''
        if not self.can_move_box(location, direction):
            return False
        box = self._get_box(location)
        # Move neighbors (recurse):
        for neigh in self._get_neighbors(box, direction):
            if self.get(neigh, '.') in '[]':
                self.move_box(neigh, direction)
        # Move self (finally!):
        if direction == Direction.E:
            box = tuple(reversed(box))
        step = direction.velocity()
        for point in box:
            self[point+step] = self[point]
            del self[point]
        return True
        
                
if __name__ == '__main__':
    import sys
    sys.exit(main())
