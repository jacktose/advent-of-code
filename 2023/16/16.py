#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/16
Day 16: The Floor Will Be Lava
"""

from __future__ import annotations
from collections import deque
from dataclasses import dataclass
import enum
import itertools
import os
from time import sleep
from typing import NamedTuple, Sequence

def main():
    ex_data = get_input('./example.txt')
    data = get_input('./input.txt')

    print('example 1:')
    print(part_1(ex_data, watch=True), '= 46?')

    print('\npart 1:')
    print(part_1(data))

    print('\nexample 2:')
    print(part_2(ex_data, watch=True, delay=0.01, inter_delay=0.2), '= 51?')

    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input.txt'):
    with open(file, 'r') as f:
        data = f.read().splitlines()
    return data

def part_1(data, watch: bool = False, delay: float = 0.05) -> int:
    '''With the beam starting in the top-left heading right,
    how many tiles end up being energized?'''
    return light_it_up(data, start=Beam(Point(0, 0), Velocity(0, 1)), watch=watch, delay=delay)

def part_2(data, watch: bool = False, delay: float = 0.05, inter_delay: float = 0) -> int:
    '''Find the initial beam configuration that energizes the largest number of tiles;
    how many tiles are energized in that configuration?'''
    n_rows = len(data)
    n_cols = len(data[0])
    return max(
        light_it_up(data, start=Beam(p, v), watch=watch,
                    delay=delay, inter_delay=inter_delay)
        for p, v in itertools.chain(
            ((Point(0,        c), Velocity( 1,  0)) for c in range(n_cols)),
            ((Point(n_rows-1, c), Velocity(-1,  0)) for c in range(n_cols)),
            ((Point(r,        0), Velocity( 0,  1)) for r in range(n_rows)),
            ((Point(r, n_cols-1), Velocity( 0, -1)) for r in range(n_rows)),
        )
    )

def light_it_up(data, start: Beam, watch: bool = False,
                delay: float = 0.05, inter_delay: float = 0) -> int:
    beams = deque([start])
    lit = [[Direction(0) for p in row] for row in data]
    if watch:
        display = Display(data)
        display.highlight = [beams[0].loc]
        sleep(inter_delay)
    else:
        display = None
    while beams:
        # Refresh display every cycle
        if display:
            display.print(lit, beams)
            sleep(delay)

        # Split/reflect all beams
        for _ in range(len(beams)):
            beam = beams.popleft()
            p = beam.loc
            # If already passed this tile in this direction:
            if beam.direction in lit[p.r][p.c]:
                continue  # ... let it die
            # Light this tile (record which in which directions we've passed)
            lit[p.r][p.c] |= beam.direction
            # Interact with tile
            tile = data[p.r][p.c]
            beams.extend(b for b in beam.reflected(tile) if b not in beams)

        # Move all beams
        for _ in range(len(beams)):
            beam = beams.popleft()
            beam.advance()
            if in_bounds(data, beam.loc):
                beams.append(beam)
                # Else let it die

    return sum(sum(tile != Direction.NONE for tile in row) for row in lit)

def in_bounds(data: Sequence[Sequence], point: Point) -> bool:
    return (0 <= point.r < len(data)) and (0 <= point.c < len(data[0]))

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

    @property
    def direction(self) -> Direction:
        match self.dr, self.dc:
            case -1, 0: return Direction.N
            case 0, -1: return Direction.W
            case 1, 0: return Direction.S
            case 0, 1: return Direction.E
        raise NotImplementedError('Cardinal directions only')

    def reflected(self, tile: str) -> Velocity:
        match tile:
            case '/':
                return Velocity(dr=-self.dc, dc=-self.dr)
            case '\\':
                return Velocity(dr=self.dc, dc=self.dr)
        raise ValueError

@dataclass
class Beam:
    loc: Point
    vel: Velocity

    def advance(self) -> Point:
        self.loc += self.vel
        return self.loc

    def reflected(self, tile: str) -> list[Beam]:
        match tile:
            case '.':
                return [self]
            case '/' | '\\':
                return [Beam(self.loc, self.vel.reflected(tile))]
            case '|' if self.vel.dc == 0:
                return [self]
            case '|':
                return [Beam(self.loc, self.vel.reflected(t)) for t in '/\\']
            case '-' if self.vel.dr == 0:
                return [self]
            case '-':
                return [Beam(self.loc, self.vel.reflected(t)) for t in '/\\']
        raise ValueError

    @property
    def character(self) -> str:
        match self.vel:
            case (0, 1): return '>'
            case (1, 0): return 'v'
            case (0, -1): return '<'
            case (-1, 0): return '^'
        raise RuntimeError(f'Unexpected velocity: {self.vel}')

    @property
    def direction(self) -> Direction:
        return self.vel.direction

class Display:
    def __init__(self, grid) -> None:
        self.grid = grid
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.highlight: Sequence[Point] = []
        term = os.get_terminal_size()
        if self.rows >= term.lines:
            print(f'Warning: grid len {self.rows} too tall for terminal {term.columns=} {term.lines=}')
        self._started = False

    def _prep(self) -> None:
        print(control.HIDE_CURSOR)
        print('\n' * (self.rows+1), end='')

    def _back_up(self) -> None:
        print(f'\x1b[{self.rows}F', end='')

    def print(self, lit, beams) -> None:
        if not self._started:
            self._prep()
            self._started = True
        self._back_up()
        beam_chars = {beam.loc: beam.character for beam in beams}
        for r, row in enumerate(self.grid):
            for c, tile in enumerate(row):
                if Point(r, c) in self.highlight:
                    print(style.BG.GREEN, end='')
                try:
                    print(style.BOLD, style.FG.YELLOW,
                        beam_chars[Point(r, c)],
                        style.RESET,
                        sep= '', end='')
                except KeyError:
                    print(style.BOLD + style.FG.YELLOW if lit[r][c] else '',
                        tile,
                        style.RESET,
                        sep= '', end='')
            print()
        print(n_lit(lit) + len(beams), '\r', sep='', end='')
        pass

def n_lit(lit) -> int:
    return sum(sum(d != Direction.NONE for d in row) for row in lit)


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

