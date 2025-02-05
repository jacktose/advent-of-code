#!/usr/bin/env python3

"""
https://adventofcode.com/2024/day/6
Day 6: Guard Gallivant
"""

from __future__ import annotations
from dataclasses import dataclass
import enum
import os
from time import sleep
from typing import NamedTuple, Sequence


def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data), '= 41?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data, watch=True), '= 6?')
    
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = f.read().splitlines()
    data = {Point(r=r, c=c): v for r, row in enumerate(data) for c, v in enumerate(row)}
    return data

def part_1(data: dict[Point, str]) -> int:
    '''How many distinct positions will the guard visit before leaving the mapped area?'''
    return len(visited(data))

def visited(data: dict[Point, str]) -> list[Point]:
    visited: list[Point] = []
    guard = find_guard(data)
    while guard.loc in data:
        if guard.loc not in visited:
            visited.append(guard.loc)
        if guard.ahead() not in data:
            # About to leave the grid
            break
        while data[guard.ahead()] == '#':
            guard.turn()
        guard.advance()
    return visited

def part_2(data: dict[Point, str], watch: bool = False):
    '''You need to get the guard stuck in a loop by adding a single new obstruction.
    How many different positions could you choose for this obstruction?'''
    # There's an analytical solution, but this works ...
    return sum(guard_loops(data, obstruction, watch=watch, delay=0.01) for obstruction in visited(data)[1:])

def find_guard(data: dict[Point, str]) -> Guard:
    '''Look through the grid for the starting location and direction of the guard'''
    for loc, char in data.items():
        if char in '^v<>':
            return Guard(loc, Velocity.from_char(char))
    else:
        raise ValueError('No guard, no guard, lala lala la la!')

def guard_loops(data: dict[Point, str], obstruction: Point,
               watch: bool = False, delay: float = 0.05, inter_delay: float = 0
               ) -> bool:
    guard = find_guard(data)
    if obstruction == guard.loc or data[obstruction] == '#':
        return False
    visited: dict[Point, Direction] = {loc: Direction(0) for loc in data}

    if watch:
        display = Display(data)
        display.highlight = [guard.loc]
        display.obstruction = obstruction
        sleep(inter_delay)
    else:
        display = None

    while guard.loc in data:
        # Refresh display every cycle
        if display:
            display.print(visited, guard)
            sleep(delay)
        # Have we looped?
        if guard.dir in visited[guard.loc]:
            if watch: print('LOOP!')
            return True
        # Record passing this location in this direction
        visited[guard.loc] |= guard.dir
        if guard.ahead() not in data:
            # About to leave grid
            break
        while data[guard.ahead()] == '#' or guard.ahead() == obstruction:
            guard.turn()
        guard.advance()
    return False


class classproperty:
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
    @classproperty
    def ALL(cls):
        return ~cls(0)  # type: ignore
    
    @staticmethod
    def from_vel(vel: Velocity) -> Direction:
        match vel.dr, vel.dc:
            case -1,  0: return Direction.N
            case  0, -1: return Direction.W
            case  1,  0: return Direction.S
            case  0,  1: return Direction.E
        raise NotImplementedError('Cardinal directions only')

    @staticmethod
    def from_char(char: str) -> Direction:
        match char:
            case '^': return Direction.N
            case '<': return Direction.W
            case 'v': return Direction.S
            case '>': return Direction.E
        raise ValueError(f'Unexpected char: {char}')


class Point(NamedTuple):
    r: int
    c: int

    def __add__(self, other: Point|Velocity|tuple[int, int]) -> Point:
        if isinstance(other, Point):
            return Point(self.r + other.r, self.c + other.c)
        elif isinstance(other, Velocity):
            return Point(self.r + other.dr, self.c + other.dc)
        elif isinstance(other, tuple) and len(other) == 2:
            return Point(self.r + other[0], self.c + other[1])
        else:
            raise TypeError


class Velocity(NamedTuple):
    dr: int
    dc: int

    @staticmethod
    def from_char(char: str) -> Velocity:
        match char:
            case '^': return Velocity(dr=-1, dc= 0)
            case 'v': return Velocity(dr= 1, dc= 0) 
            case '>': return Velocity(dr= 0, dc= 1) 
            case '<': return Velocity(dr= 0, dc=-1)
        raise ValueError(f'Unexpected char: {char}')

    @staticmethod
    def from_dir(dir: Direction) -> Velocity:
        match dir:
            case Direction.N: return Velocity(dr=-1, dc= 0)
            case Direction.S: return Velocity(dr= 1, dc= 0) 
            case Direction.E: return Velocity(dr= 0, dc= 1) 
            case Direction.W: return Velocity(dr= 0, dc=-1)
        raise ValueError(f'Invalid Direction: {dir}')

    @property
    def direction(self) -> Direction:
        return Direction.from_vel(self)

    def turned(self) -> Velocity:
        return Velocity(dr=self.dc, dc=-self.dr)


@dataclass
class Guard:
    loc: Point
    vel: Velocity

    def ahead(self) -> Point:
        return self.loc + self.vel

    def advance(self) -> Point:
        self.loc += self.vel
        return self.loc

    def turn(self) -> None:
        self.vel = self.vel.turned()

    @property
    def char(self) -> str:
        match self.vel:
            case (0,  1): return '>'
            case (1,  0): return 'v'
            case (0, -1): return '<'
            case (-1, 0): return '^'
        raise RuntimeError(f'Unexpected velocity: {self.vel}')

    @property
    def dir(self) -> Direction:
        return self.vel.direction


class Display:
    def __init__(self, grid) -> None:
        self.grid: dict[Point, str] = grid
        self.rows: int = sum(p[1] == 0 for p in self.grid)
        self.cols: int = sum(p[0] == 0 for p in self.grid)
        self.highlight: Sequence[Point] = []
        self.obstruction: Point|None = None
        term = os.get_terminal_size()
        if self.rows >= term.lines:
            print(f'Warning: grid len {self.rows} too tall for terminal {term.columns=} {term.lines=}')
        self._started: bool = False

    def _prep(self) -> None:
        print(control.HIDE_CURSOR, end='')
        print('\n' * (self.rows+1), end='')

    def _back_up(self) -> None:
        print(f'\x1b[{self.rows}F', end='')

    def print(self, visited, guard) -> None:
        if not self._started:
            self._prep()
            self._started = True
        self._back_up()
        for r in range(self.rows):
            for c in range(self.cols):
                p = Point(r, c)
                if p in self.highlight:
                    print(style.BG.GREEN, end='')
                if p == guard.loc:
                    print(style.BOLD, style.FG.YELLOW,
                        guard.char,
                        style.RESET,
                        sep= '', end='')
                elif p == self.obstruction:
                    print(style.BOLD, style.FG.RED,
                        'O',
                        style.RESET,
                        sep= '', end='')
                else:
                    print(style.BOLD + style.FG.YELLOW if visited[p] else '',
                        self.grid[p],
                        style.RESET,
                        sep= '', end='')
            print()  # End of row

class _fg(NamedTuple):
    BLACK =   '\x1b[30m'
    RED =     '\x1b[31m'
    GREEN =   '\x1b[32m'
    YELLOW =  '\x1b[33m'
    BLUE =    '\x1b[34m'
    MAGENTA = '\x1b[35m'
    CYAN =    '\x1b[36m'
    WHITE =   '\x1b[37m'

class _bg(NamedTuple):
    BLACK =   '\x1b[40m'
    RED =     '\x1b[41m'
    GREEN =   '\x1b[42m'
    YELLOW =  '\x1b[43m'
    BLUE =    '\x1b[44m'
    MAGENTA = '\x1b[45m'
    CYAN =    '\x1b[46m'
    WHITE =   '\x1b[47m'

class style(NamedTuple):
    RESET =         '\x1b[0m'
    BOLD =          '\x1b[1m'
    FAINT =         '\x1b[2m'
    ITALIC =        '\x1b[3m'
    UNDERLINED =    '\x1b[4m'
    INVERSE =       '\x1b[7m'
    STRIKETHROUGH = '\x1b[9m'
    FG = _fg
    BG = _bg

class control(NamedTuple):
    SHOW_CURSOR = '\x1b[?25h'
    HIDE_CURSOR = '\x1b[?25l'
    ERASE_CURSOR_TO_END = '\x1b[0J'
    ERASE_CURSOR_TO_START = '\x1b[1J'
    ERASE_SCREEN = '\x1b[2J'


if __name__ == '__main__':
    import sys
    sys.exit(main())
