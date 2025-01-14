"""
Classes & functions for representing and working with a 2D grid.
"""

from __future__ import annotations
from collections.abc import Callable, Generator, Mapping, Sequence
import enum
from functools import singledispatchmethod
from typing import NamedTuple


class _classproperty:
    def __init__(self, func):
        self._func = func
    def __get__(self, obj, owner):
        return self._func(owner)

class Direction(enum.Flag):
    NONE = 0
    N = enum.auto()
    W = enum.auto()
    S = enum.auto()
    E = enum.auto()
    @_classproperty
    def ALL(cls):
        return ~cls(0)  # type: ignore
    
    @staticmethod
    def from_arrow(arrow: str) -> Direction:
        return {
            '^': Direction.N,
            '<': Direction.W,
            'v': Direction.S,
            '>': Direction.E,
        }[arrow]
    
    @property
    def arrow(self) -> str:
        return {
            Direction.N: '^',
            Direction.W: '<',
            Direction.S: 'v',
            Direction.E: '>',
        }[self]
    
    def velocity(self, speed: int = 1) -> Velocity:
        return {
            Direction.N: Velocity(-speed, 0),
            Direction.W: Velocity(0, -speed),
            Direction.S: Velocity(speed, 0),
            Direction.E: Velocity(0, speed),
        }[self]
    
    def cross(self, other: Direction) -> int:
        return self.velocity(speed=1).cross(other.velocity(speed=1))


class RCPair(NamedTuple):
    '''A pair of coordinates, for access with point.row, point.col'''
    row: int
    col: int

    @property
    def r(self): return self.row
    @property
    def c(self): return self.col
    @property
    def rows(self): return self.row
    @property
    def cols(self): return self.col

    def __add__(self, other: RCPair|tuple[int, int]) -> RCPair:
        if isinstance(other, RCPair):
            return RCPair(self.row + other.row, self.col + other.col)
        elif isinstance(other, tuple) and len(other) == 2:
            return RCPair(self.row + other[0], self.col + other[1])
        else:
            raise TypeError

    def __sub__(self, other: RCPair|tuple[int, int]) -> RCPair:
        if isinstance(other, RCPair):
            return RCPair(self.row - other.row, self.col - other.col)
        elif isinstance(other, tuple) and len(other) == 2:
            return RCPair(self.row - other[0], self.col - other[1])
        else:
            raise TypeError


class Point(RCPair):

    def __add__(self, other: RCPair|tuple[int, int]) -> Point:
        return Point(*super().__add__(other))
    
    def __sub__(self, other: RCPair|tuple[int, int]) -> Point:
        return Point(*super().__sub__(other))
    

class Velocity(RCPair):
    @property
    def dr(self): return self.row
    @property
    def dc(self): return self.col

    def __add__(self, other: RCPair|tuple[int, int]) -> Velocity:
        return Velocity(*super().__add__(other))
    
    def __sub__(self, other: RCPair|tuple[int, int]) -> Velocity:
        return Velocity(*super().__sub__(other))
    
    def __mul__(self, scalar: int) -> Velocity:
        return Velocity(self.row * scalar, self.col * scalar)
    
    @property
    def direction(self) -> Direction:
        if self.dc == 0:
            if self.dr < 0: return Direction.N
            if self.dr > 0: return Direction.S
        if self.dr == 0:
            if self.dc < 0: return Direction.W
            if self.dc > 0: return Direction.E
        raise NotImplementedError('Cardinal directions only')
        #match self.dr, self.dc:
        #    case -1,  0: return Direction.N
        #    case  0, -1: return Direction.W
        #    case  1,  0: return Direction.S
        #    case  0,  1: return Direction.E
        #raise NotImplementedError('Cardinal directions only')
        #try:
        #    return {
        #        (-1,  0): Direction.N,
        #        ( 0, -1): Direction.W,
        #        ( 1,  0): Direction.S,
        #        ( 0,  1): Direction.E,
        #    }[self]
        #except KeyError:
        #    raise NotImplementedError('Cardinal directions only')

    def cross(self, other: Velocity) -> int:
        return self.dr * other.dc - self.dc * other.dr


class Grid[T](list[list[T]]):
    '''Represent a 2D grid as a list of lists'''

    @classmethod
    def from_string(cls, string: str, transformer: Callable[[str], T]|None = None) -> Grid[T]:
        return cls.from_list(string.splitlines(), transformer)
    
    @classmethod
    def from_list(cls, sequence: Sequence[str], transformer: Callable[[str], T]|None = None) -> Grid[T]:
        if transformer is None:
            return cls([[s for s in row] for row in sequence])
        else:
            return cls([[transformer(s) for s in row] for row in sequence])
    
    @property
    def heigth(self) -> int:
        return len(self)
    @property
    def width(self) -> int:
        return len(self[0])
    
    def get_row(self, row_no: int) -> list[T]:
        return self[row_no]
    
    def set_row(self, row_no: int, contents: Sequence[T], start_col: int = 0) -> None:
        if not self.in_bounds(row_no, start_col) or not self.in_bounds(row_no, start_col+len(contents)-1):
            raise IndexError
        self[row_no][start_col:start_col+len(contents)-1] = list(contents)
    
    def get_col(self, col_no: int) -> list[T]:
        return [row[col_no] for row in self]
    
    def set_col(self, col_no: int, contents: Sequence[T], start_row: int = 0) -> None:
        if not self.in_bounds(start_row, col_no) or not self.in_bounds(start_row+len(contents)-1, col_no):
            raise IndexError
        for i, val in enumerate(contents):
            self[start_row+i][col_no] = val
    
    @singledispatchmethod
    def get_value(self, point: tuple[int, int]) -> T:
        return self.get_value(*point)
    @get_value.register
    def _(self, point: Point|RCPair):
        return self.get_value(*point)
    @get_value.register
    def _(self, row: int, col: int):
        if not self.in_bounds(row, col):
            raise IndexError
        return self[row][col]
    
    @singledispatchmethod
    def in_bounds(self, point: tuple[int, int]) -> bool:
        return self.in_bounds(*point)
    @in_bounds.register
    def _(self, point: Point|RCPair):
        return self.in_bounds(*point)
    @in_bounds.register
    def _(self, row: int, col: int):
        return row in range(len(self)) and col in range(len(self[0]))

    def iter_all(self) -> Generator[tuple[Point, T]]:
        for r, row in enumerate(self):
            for c, val in enumerate(row):
                yield Point(r, c), val
    
    def find(self, target: T) -> Generator[Point]:
        for point, val in self.iter_all():
            if val == target:
                yield point
    
    @singledispatchmethod
    def neighbors(self, *args) -> Generator[tuple[Point, T]]:
        raise TypeError
    @neighbors.register
    def _(self, point: Point):
        for velocity in (Velocity(-1, 0), Velocity(0, 1), Velocity(1, 0), Velocity(0, -1)):
            if self.in_bounds(neighbor := point + velocity):
                yield neighbor, self.get_value(neighbor)
    @neighbors.register
    def _(self, row: int, col: int):
        return self.neighbors(Point(row, col))
    
    @singledispatchmethod
    def contiguous(self, *args) -> tuple[Point, ...]:
        raise TypeError
    @contiguous.register
    def _(self, origin: Point):
        value = self.get_value(origin)
        members = set()
        stack = [origin]
        while stack:
            if (point := stack.pop()) in members:
                continue
            members.add(point)
            stack.extend(neigh_pt for neigh_pt, neigh_val in self.neighbors(*point)
                         if neigh_val == value and neigh_pt not in members)
        return tuple(sorted(members))
    @contiguous.register
    def _(self, row: int, col:int):
        return self.contiguous(Point(row, col))
    
    def rotate(self, initial: Direction, final: Direction) -> None:
        if initial == final:
            return
        match initial.cross(final):
            case -1:  # 90 degrees clockwise
                self[:] = [list(row) for row in zip(*self[::-1])]
            case  0:  # 180 degrees
                self[:] = [list(row[::-1]) for row in self[::-1]]
            case  1:  # 270 degrees clockwise
                self[:] = [list(row) for row in zip(*self)][::-1]
    
    def print(self) -> None:
        for row in self:
            print(''.join(str(x) for x in row))
        

class Grid_Immutable[T](tuple[tuple[T, ...], ...]):
    '''Represent a 2D grid as a tuple of tuples.'''

    @staticmethod
    def from_string(string: str) -> Grid_Immutable[T]:
        return Grid_Immutable.from_list(string.splitlines())
    
    @staticmethod
    def from_list(sequence: Sequence[str], transformer: Callable[[str], T] = lambda x: x) -> Grid_Immutable[T]:
        return Grid_Immutable(tuple(tuple(transformer(s) for s in row) for row in sequence))
    
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

#@dataclass
class Grid_Sparse[T](dict[Point, T]):
    '''Represent a 2D grid as a dictionary of points to values.'''
    #dimensions: RCPair|None
    #bg_out: str

    # input as mapping of points to values
    @singledispatchmethod
    def __init__[T_in](self,
                 grid: Mapping[Point|tuple[int, int], T_in],
                 dimensions: RCPair|tuple[int, int]|None = None,
                 transformer: Callable[[T_in], T] = lambda x: x,
                 bg_in: T|None = None,
                 bg_out: T|str = '.',
                 **kwargs) -> None:
        super().__init__({Point(*k): tv for k, v in grid.items()
                          if bg_in not in (v, tv := transformer(v))},
                         **kwargs)
        
        self.dimensions: RCPair|None = RCPair(*dimensions) if isinstance(dimensions, tuple) else dimensions
        self.bg_out: str = str(bg_out)
    
    # input as list of strings or list of lists
    @__init__.register
    def __init_seq(self, grid: Sequence, **kwargs):
        grid_dict = {Point(r, c): s for r, row in enumerate(grid) for c, s in enumerate(row)}
        return Grid_Sparse.__init__(self, grid_dict, **kwargs)
    
    # input as single string
    @__init__.register
    def __init_str(self, grid: str, **kwargs):
        return Grid_Sparse.__init_seq(self, grid.splitlines(), **kwargs)

    def __str__(self) -> str:
        return '\n'.join(
            ''.join(
                str(self.get(Point(i, j), self.bg_out))
                for j in range(self._dimensions_auto.col))
            for i in range(self._dimensions_auto.row)
        )
    
    @property
    def _dimensions_auto(self) -> RCPair:
        if self.dimensions is None:
            return RCPair(max(point.row for point in self)+1, max(point.col for point in self)+1)
        else:
            return self.dimensions
    
    def in_bounds(self, point: Point) -> bool:
        if self.dimensions is None:
            return True
        return point.row in range(self.dimensions.row) and point.col in range(self.dimensions.col)
    
    def find(self, target: T) -> Point:
        return next(self.find_all(target))

    def find_all(self, target: T) -> Generator[Point]:
        for point, val in self.items():
            if val == target:
                yield point