"""
Classes & functions for representing and working with a 2D grid.
"""

from __future__ import annotations
from abc import ABC
from collections import deque
from collections.abc import Callable, Collection, Generator, Iterable, Mapping, Sequence
import enum
from functools import singledispatchmethod
from typing import NamedTuple, overload


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
    character = arrow

    @property
    def left(self) -> Direction:
        return {
            Direction.N: Direction.W,
            Direction.E: Direction.N,
            Direction.S: Direction.E,
            Direction.W: Direction.S,
        }[self]

    @property
    def right(self) -> Direction:
        return {
            Direction.N: Direction.E,
            Direction.E: Direction.S,
            Direction.S: Direction.W,
            Direction.W: Direction.N,
        }[self]

    @property
    def opposite(self) -> Direction:
        return {
            Direction.N: Direction.S,
            Direction.E: Direction.W,
            Direction.S: Direction.N,
            Direction.W: Direction.E,
        }[self]

    @property
    def perpendiculars(self) -> tuple[Direction, Direction]:
        return (self.left, self.right)    
    
    @property
    def unit_velocity(self) -> Velocity:
        return self.velocity(speed=1)

    def velocity(self, speed: int = 1) -> Velocity:
        return {
            Direction.N: Velocity(-speed, 0),
            Direction.W: Velocity(0, -speed),
            Direction.S: Velocity(speed, 0),
            Direction.E: Velocity(0, speed),
        }[self]
    
    def cross(self, other: Direction) -> int:
        '''Cross product of two direction vectors'''
        return self.unit_velocity.cross(other.unit_velocity)


class RCPair(NamedTuple):
    '''Abstract base class for (row, column) pair'''
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

    def __add__[T](self: T, other: RowAndCol) -> T:
        if isinstance(other, RCPair):
            return self.__class__(self.row + other.row, self.col + other.col)
        elif isinstance(other, tuple) and len(other) == 2:
            return self.__class__(self.row + other[0], self.col + other[1])
        else:
            raise TypeError

    def __sub__[T](self: T, other: RowAndCol) -> T:
        if isinstance(other, RCPair):
            return self.__class__(self.row - other.row, self.col - other.col)
        elif isinstance(other, tuple) and len(other) == 2:
            return self.__class__(self.row - other[0], self.col - other[1])
        else:
            raise TypeError


class Point(RCPair):
    '''A pair of coordinates, for access with point.row, point.col'''

    #def __add__(self, other: RowAndCol) -> Point:
    #    return Point(*super().__add__(other))
    
    @overload
    def __sub__(self, other: Point) -> Velocity: ...
    @overload
    def __sub__(self, other: Velocity) -> Point: ...
    @overload
    def __sub__(self, other: RowAndCol) -> Point: ...

    #@singledispatchmethod
    #def __sub__(self, other: Point) -> Velocity:
    #    return Velocity(*super().__sub__(other))
    #@__sub__.register
    #def __sub__velocity(self, other: Velocity) -> Point:
    #    return Point(*super().__sub__(other))
    #@__sub__.register
    #def __sub__rowandcol(self, other: RowAndCol) -> Point:
    #    return Point(*super().__sub__(other))

    def __sub__(self, other: Point|Velocity|RowAndCol) -> Velocity|Point:
        if isinstance(other, Point):
            return Velocity(*super().__sub__(other))
        elif isinstance(other, Velocity):
            return Point(*super().__sub__(other))
        else:
            return Point(*super().__sub__(other))
    

class Velocity(RCPair):
    '''A 2D velocity vector (in a cardinal direction)'''
    @property
    def dr(self): return self.row
    @property
    def dc(self): return self.col

    #def __add__(self, other: RCPair|tuple[int, int]) -> Velocity:
    #    return Velocity(*super().__add__(other))
    
    #def __sub__(self, other: RCPair|tuple[int, int]) -> Velocity:
    #    return Velocity(*super().__sub__(other))
    
    def __mul__(self, scalar: int) -> Velocity:
        return Velocity(self.row * scalar, self.col * scalar)
    
    @property
    def component_row(self):
        return Velocity(self.row, 0)
    @property
    def component_col(self):
        return Velocity(0, self.col)

    @property
    def direction(self) -> Direction:
        if self.dc == 0:
            if self.dr < 0: return Direction.N
            if self.dr > 0: return Direction.S
            if self.dr == 0: return Direction.NONE
        if self.dr == 0:
            if self.dc < 0: return Direction.W
            if self.dc > 0: return Direction.E
            if self.dc == 0: return Direction.NONE
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
        '''Cross product of two velocity vectors
        NB: Only for cardinal directions!'''
        return self.dr * other.dc - self.dc * other.dr

type RowAndCol = RCPair | tuple[int, int]

class _Grid[T](Sequence[Sequence[T]], ABC):
    def __init__[T_in](self,
                       grid: Iterable[Iterable[T_in]],
                       transformer: Callable[[T_in], T] = lambda x: x):
        ...
    
    height: int
    width: int

    def __str__(self) -> str:
        return '\n'.join(''.join(str(x) for x in row) for row in self)

    def string_with_numbers(self) -> str:
        head_rows = len(str(self.width))
        left_cols = len(str(self.height))
        output = [(' ',)*left_cols + line for line in zip(*[list(f'{n:{head_rows}}') for n in range(self.width)])]
        for r, row in enumerate(self):
            output.append([f'{r:{left_cols}}'] + list(row))
        return '\n'.join(''.join(str(x) for x in row) for row in output)

    def get_row(self, row_no: int) -> Sequence[T]|None:
        ...
    
    def get_col(self, col_no: int) -> Sequence[T]|None:
        ...
    
    def get_point(self, point: Point|RowAndCol) -> T|None:
        point = Point(*point)
        try:
            return self[point.row][point.col]
        except IndexError:
            return None

    @singledispatchmethod
    def get_value(self, point: Point|RowAndCol) -> T:
        return self.get_value(*point)
    @get_value.register
    def _(self, row: int, col: int):
        if not self.in_bounds(row, col):
            raise IndexError
        return self[row][col]

    @singledispatchmethod
    def in_bounds(self, point: Point|RowAndCol) -> bool:
        return self.in_bounds(*point)
    @in_bounds.register
    def _(self, row: int, col: int):
        return row in range(self.height) and col in range(self.width)

    def iter_all(self) -> Generator[tuple[Point, T]]:
        for r, row in enumerate(self):
            for c, val in enumerate(row):
                yield Point(r, c), val
    
    def find(self, target: T) -> Point:
        return next(self.find_all(target))

    def find_all(self, target: T) -> Generator[Point]:
        for point, val in self.iter_all():
            if val == target:
                yield point

    @singledispatchmethod
    def neighbors(self, point: Point|RowAndCol) -> Generator[tuple[Point, T]]:
        STEPS = (Velocity(-1, 0), Velocity(0, 1), Velocity(1, 0), Velocity(0, -1))
        for step in STEPS:
            if self.in_bounds(neighbor := Point(*point) + step):
                yield neighbor, self.get_value(neighbor)
    @neighbors.register
    def _(self, row: int, col: int):
        return self.neighbors(Point(row, col))

    @singledispatchmethod
    def contiguous(self, origin: Point|RowAndCol) -> tuple[Point, ...]:
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
    
    def bfs(self, start: RowAndCol, end: RowAndCol) -> tuple[Point, ...]:
        ...  # TODO: implement


class Grid_Mutable[T](list[list[T]], _Grid[T]):
    '''Represent a 2D grid as a list of lists'''

    @singledispatchmethod
    def __init__[T_in](self,
                       grid: Iterable[Iterable[T_in]],
                       transformer: Callable[[T_in], T] = lambda x: x):
        super().__init__([[transformer(x) for x in row] for row in grid])
    @__init__.register
    def __init__str(self, grid: str, **kwargs):
        return self.__init__(grid.splitlines(), **kwargs)

    @property
    def height(self) -> int:
        return len(self)
    @property
    def width(self) -> int:
        return len(self[0])
    
    def get_row(self, row_no: int) -> list[T]|None:
        try:
            return self[row_no]
        except IndexError:
            return None
    
    def set_row(self, row_no: int, contents: Sequence[T], start_col: int = 0) -> None:
        if not self.in_bounds(row_no, start_col) or not self.in_bounds(row_no, start_col+len(contents)-1):
            raise IndexError
        self[row_no][start_col:start_col+len(contents)-1] = list(contents)
    
    def get_col(self, col_no: int) -> list[T]|None:
        try:
            return [row[col_no] for row in self]
        except IndexError:
            return None
    
    def set_col(self, col_no: int, contents: Sequence[T], start_row: int = 0) -> None:
        if not self.in_bounds(start_row, col_no) or not self.in_bounds(start_row+len(contents)-1, col_no):
            raise IndexError
        for i, val in enumerate(contents):
            self[start_row+i][col_no] = val

    def set_point(self, point: Point|RowAndCol, value: T) -> None:
        point = Point(*point)
        self[point.row][point.col] = value
    
    @singledispatchmethod
    def rotate(self, degrees: int) -> None:
        match degrees:
            case 0:
                return
            case 90 | -270:
                self[:] = [list(row) for row in zip(*self[::-1])]
            case 180 | -180:
                self[:] = [list(row[::-1]) for row in self[::-1]]
            case 270 | -90:
                self[:] = [list(row) for row in zip(*self)][::-1]
            case other:
                raise NotImplementedError(f'Cannot rotate by {other} degrees.')
    @rotate.register
    def _(self, initial: Direction, final: Direction) -> None:
        if initial == final:  # cross product will be 0, same as 180
            return
        match initial.cross(final):
            case -1: return self.rotate(90)
            case  0: return self.rotate(180)
            case  1: return self.rotate(270)
        raise NotImplementedError(f'Cannot rotate; orthogonal only')
    

class Grid(Grid_Mutable):
    # Alias to Grid_Mutable
    ...


class Grid_Immutable[T](tuple[tuple[T, ...], ...], _Grid):
    '''Represent a 2D grid as a tuple of tuples.'''

    def __new__[T_in](cls,
                       grid: Iterable[Iterable[T_in]]|str,
                       transformer: Callable[[T_in], T] = lambda x: x):
        if isinstance(grid, str):
            grid = grid.splitlines()
        return super().__new__(cls, (tuple(transformer(x) for x in row) for row in grid))

    def __init__(self, _grid, _transformer=None):
        self.height: int = len(self)
        self.width: int = len(self[0])
        self.dimensions = RCPair(self.height, self.width)

    def get_row(self, row_no: int) -> tuple[T, ...]|None:
        try:
            return self[row_no]
        except IndexError:
            return None
    
    def get_col(self, col_no: int) -> tuple[T, ...]|None:
        try:
            return tuple(row[col_no] for row in self)
        except IndexError:
            return None


class Grid_Sparse[T](dict[Point, T]):
    '''Represent a 2D grid as a dictionary of points to values.'''

    # input as mapping of points to values
    @singledispatchmethod
    def __init__[T_in](self,
                 grid: Mapping[RowAndCol, T_in],
                 dimensions: RowAndCol|None = None,
                 transformer: Callable[[T_in], T] = lambda x: x,
                 bg_in: T|None = None,
                 bg_out: T|str = '.',
                 **kwargs) -> None:
        super().__init__({Point(*k): tv for k, v in grid.items()
                          if bg_in not in (v, tv := transformer(v))},
                         **kwargs)
        
        self.dimensions: RCPair|None = RCPair(*dimensions) if isinstance(dimensions, tuple) else None
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
        if isinstance(self.dimensions, RCPair):
            return self.dimensions
        else:
            return RCPair(max(point.row for point in self)+1, max(point.col for point in self)+1)
    
    def in_bounds(self, point: Point) -> bool:
        if self.dimensions is None:
            return True
        return point.row in range(self.dimensions.row) and point.col in range(self.dimensions.col)

    @singledispatchmethod
    def neighbors(self, point: Point|RowAndCol) -> Generator[tuple[Point, T]]:
        STEPS = (Velocity(-1, 0), Velocity(0, 1), Velocity(1, 0), Velocity(0, -1))
        for step in STEPS:
            if self.in_bounds(neighbor := Point(*point) + step):
                yield neighbor, self.get(neighbor, self.bg_out)
    @neighbors.register
    def _(self, row: int, col: int):
        return self.neighbors(Point(row, col))
    
    def find(self, target: T) -> Point:
        return next(self.find_all(target))

    def find_all(self, target: T) -> Generator[Point]:
        for point, val in self.items():
            if val == target:
                yield point

    def bfs(self, start: RowAndCol, end: RowAndCol, invalid: Collection[T] = set('#')) -> tuple[Point, ...]:
        '''Breadth-first search. Returns path from start to end,
        avoiding locations with invalid values (e.g. walls).
        If no path, returns empty tuple.'''
        start = Point(*start)
        end = Point(*end)
        invalid = set(invalid)

        def backtrack(prevs: Mapping[Point, Point|None], end: Point) -> tuple[Point, ...]:
            path = [end]
            while (prev := prevs[path[-1]]) is not None:
                path.append(prev)
            return tuple(reversed(path))

        todo = [start]
        prev: dict[Point, Point|None] = {start: None}
        for here in todo:
            for neighbor, value in self.neighbors(here):
                if neighbor in prev or value in invalid:
                    continue
                prev[neighbor] = here
                if neighbor == end:
                    return tuple(backtrack(prev, end))
                todo.append(neighbor)
        else:  # Can't reach end from start
            return ()





if __name__ == '__main__':
    print('test Grid creation:')
    for data in ([['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i']],
                 ['ijk', 'lmn', 'opq'],
                 'rst\nuvw\nxyz'):
        grid = Grid_Mutable(data)
        print(grid, end='\n\n')
    
    print('test neighbors:')
    print(tuple(grid.neighbors(Point(0,0))))
    print(tuple(grid.neighbors(Point(1,1))))