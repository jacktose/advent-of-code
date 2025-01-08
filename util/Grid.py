"""
Classes & functions for representing and working with a 2D grid.
"""

from __future__ import annotations
from collections.abc import Callable, Generator, Sequence


class Grid[T](tuple[tuple[T, ...], ...]):
    '''Represent a 2D grid as a tuple of tuples.'''

    @staticmethod
    def from_string(string: str) -> Grid:
        return Grid.from_list(string.splitlines())
    
    @staticmethod
    def from_list(sequence: Sequence[str], transformer: Callable[[str], T] = lambda x: x) -> Grid[T]:
        return Grid(tuple(tuple(transformer(s) for s in row) for row in sequence))
    
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

    def iter_all(self) -> Generator[tuple[tuple[int, int], T]]:
        for r, row in enumerate(self):
            for c, val in enumerate(row):
                yield (r, c), val
    
    def find(self, target: T) -> Generator[tuple[int, int]]:
        for point, val in self.iter_all():
            if val == target:
                yield point
    
    def neighbors(self, row: int, col: int) -> Generator[tuple[tuple[int, int], T]]:
        for d_row, d_col in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            if self.in_bounds(*(neighbor := (row+d_row, col+d_col))):
                yield neighbor, self.get_value(*neighbor)
    
    def contiguous(self, row: int, col:int) -> tuple[tuple[int, int], ...]:
        value = self.get_value(row, col)
        members = set()
        stack = [(row, col)]
        while stack:
            if (point := stack.pop()) in members:
                continue
            members.add(point)
            stack.extend(neigh_pt for neigh_pt, neigh_val in self.neighbors(*point)
                         if neigh_val == value and neigh_pt not in members)
        return tuple(sorted(members))