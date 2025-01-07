#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/10
Day 10: Hoof It
"""

from __future__ import annotations
from collections.abc import Callable, Generator, Sequence


def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data), '= 36?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 81?')
    
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = Grid.from_string(f.read())
    return data

def part_1(data: Grid) -> int:
    '''What is the sum of the *scores* of all trailheads on your topographic map?'''
    return sum(score(data, trailhead) for trailhead in data.find(0))

def score(grid: Grid[int], trailhead: tuple[int, int]) -> int:
    return len(ends(grid, *trailhead))

def ends(grid: Grid[int], start_row: int, start_col: int) -> set[tuple[int, int]]:
    TARGET = 9
    here_val = grid[start_row][start_col]
    if here_val == TARGET:
        return {(start_row, start_col)}
    # TODO: Better way to recurse and combine sets?
    return set().union(*(
        ends(grid, *neighbor)
        for neighbor, value in grid.neighbors(start_row, start_col)
        if value == here_val+1
    ))

def part_2(data: Grid) -> int:
    '''What is the sum of the *ratings* of all trailheads?'''
    return sum(rating(data, *trailhead) for trailhead in data.find(0))

def rating(grid: Grid[int], start_row: int, start_col: int) -> int:
    here_val = grid[start_row][start_col]
    if here_val == 9:
        return 1
    return sum(rating(grid, *neighbor) for neighbor, value in grid.neighbors(start_row, start_col) if value == here_val+1)

class Grid[T](tuple[tuple[T, ...], ...]):
    '''Represent a 2D grid as a tuple of tuples.'''

    @staticmethod
    def from_string(string: str) -> Grid:
        return Grid.from_list(string.splitlines())
    
    @staticmethod
    def from_list(lst: Sequence[str], factory: Callable[[str], T] = int) -> Grid[T]:
        return Grid(tuple(tuple(factory(s) for s in row) for row in lst))
    
    def get_row(self, row_no: int) -> tuple[T, ...]:
        return self[row_no]
    
    def get_col(self, col_no: int) -> tuple[T, ...]:
        return tuple(row[col_no] for row in self)
    
    def get_value(self, row_no: int, col_no: int) -> T:
        if not self.in_bounds(row_no, col_no):
            raise IndexError
        return self[row_no][col_no]
    
    def in_bounds(self, row_no, col_no) -> bool:
        return row_no in range(len(self)) and col_no in range(len(self[0]))

    def find(self, target: T) -> Generator[tuple[int, int]]:
        for r, row in enumerate(self):
            for c, val in enumerate(row):
                if val == target:
                    yield (r, c)
    
    def neighbors(self, row: int, col: int) -> Generator[tuple[tuple[int, int], T]]:
        for d_row, d_col in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            if self.in_bounds(*(neighbor := (row+d_row, col+d_col))):
                yield neighbor, self.get_value(*neighbor)


if __name__ == '__main__':
    import sys
    sys.exit(main())

