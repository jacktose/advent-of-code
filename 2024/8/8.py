#!/usr/bin/env python3

"""
https://adventofcode.com/2024/day/8
Day 8: Resonant Collinearity
"""

from __future__ import annotations
from collections.abc import Sequence
#from operator import add, sub
from typing import NamedTuple


def main():
    ex_data = get_input('./example.txt')
    data = get_input('./input.txt')
    
    print('example 1:')
    print(part_1(ex_data), '= 14?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 34?')
    
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input.txt'):
    with open(file, 'r') as f:
        data = f.read().splitlines()
    return data

def part_1(data: Sequence[Sequence[str]]) -> int:
    '''How many unique locations within the bounds of the map contain an antinode?'''
    antennae = find_antennae(data)
    antinodes: set[Point] = set()
    for points in antennae.values():
        for i, p1 in enumerate(points):
            for p2 in points[i+1:]:
                dist = p2 - p1
                for p in (p1-dist, p2+dist):
                    if p.r in range(len(data)) and p.c in range(len(data[0])):
                        antinodes.add(p)
    return len(antinodes)

def part_2(data: Sequence[Sequence[str]]) -> int:
    '''Calculate the impact of the signal using this updated model.
    How many unique locations within the bounds of the map contain an antinode?'''
    antennae = find_antennae(data)
    antinodes: set[Point] = set()
    # Try a closure(?) for checking bounds more efficiently(?):
    in_bounds = lambda p, r_bounds=range(len(data)), c_bounds=range(len(data[0])): p.r in r_bounds and p.c in c_bounds
    for points in antennae.values():
        for i, p1 in enumerate(points):
            for p2 in points[i+1:]:
                dist = p2 - p1
                antinode = p1
                while in_bounds(antinode):
                    antinodes.add(antinode)
                    antinode -= dist
                antinode = p2
                while in_bounds(antinode):
                    antinodes.add(antinode)
                    antinode += dist
                ## DRYer but less readable:
                #for antinode, op in ((p1, sub), (p2, add)):
                #    while in_bounds(antinode):
                #        antinodes.add(antinode)
                #        antinode = op(antinode, dist)
    return len(antinodes)

def find_antennae(grid: Sequence[Sequence[str]]) -> dict[str, list[Point]]:
    '''Look through grid and create dict of Points for each frequency'''
    antennae = {}
    for r, row in enumerate(grid):
        for c, freq in enumerate(row):
            if freq != '.':
                antennae.setdefault(freq, []).append(Point(r, c))
    return antennae


class Point(NamedTuple):
    r: int
    c: int

    def __add__(self, other: Point|tuple[int, int]) -> Point:
        if isinstance(other, Point):
            return Point(self.r + other.r, self.c + other.c)
        elif isinstance(other, tuple) and len(other) == 2:
            return Point(self.r + other[0], self.c + other[1])
        else:
            raise TypeError

    def __sub__(self, other: Point|tuple[int, int]) -> Point:
        if isinstance(other, Point):
            return Point(self.r - other.r, self.c - other.c)
        elif isinstance(other, tuple) and len(other) == 2:
            return Point(self.r - other[0], self.c - other[1])
        else:
            raise TypeError


if __name__ == '__main__':
    import sys
    sys.exit(main())
