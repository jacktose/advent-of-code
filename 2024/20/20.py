#!/usr/bin/env python3

"""
https://adventofcode.com/2024/day/20
Day 20: Race Condition
"""

from collections import Counter
from collections.abc import Iterable
from typing import NamedTuple

import sys; import os
sys.path.append(os.path.abspath('../../util'))
from Grid import Grid_Immutable, Point
from Util import find

def main():
    ex_data = get_input('./example.txt')
    data = get_input('./input.txt')
    
    print('example 1:', part_1(ex_data, min_ps=2, verbose=True), '= 44?')
    '''
    There are 14 cheats that save 2 picoseconds.
    There are 14 cheats that save 4 picoseconds.
    There are 2 cheats that save 6 picoseconds.
    There are 4 cheats that save 8 picoseconds.
    There are 2 cheats that save 10 picoseconds.
    There are 3 cheats that save 12 picoseconds.
    There is one cheat that saves 20 picoseconds.
    There is one cheat that saves 36 picoseconds.
    There is one cheat that saves 38 picoseconds.
    There is one cheat that saves 40 picoseconds.
    There is one cheat that saves 64 picoseconds.
    '''
    print('\npart 1:', part_1(data))  # 1438
    print('\nexample 2:', part_2(ex_data, min_ps=50, verbose=True), '= 285?')
    '''
    There are 32 cheats that save 50 picoseconds.
    There are 31 cheats that save 52 picoseconds.
    There are 29 cheats that save 54 picoseconds.
    There are 39 cheats that save 56 picoseconds.
    There are 25 cheats that save 58 picoseconds.
    There are 23 cheats that save 60 picoseconds.
    There are 20 cheats that save 62 picoseconds.
    There are 19 cheats that save 64 picoseconds.
    There are 12 cheats that save 66 picoseconds.
    There are 14 cheats that save 68 picoseconds.
    There are 12 cheats that save 70 picoseconds.
    There are 22 cheats that save 72 picoseconds.
    There are 4 cheats that save 74 picoseconds.
    There are 3 cheats that save 76 picoseconds.
    '''
    print('\npart 2:', part_2(data))  # 1026446

def get_input(file='./input.txt'):
    with open(file, 'r') as f:
        data = Grid_Immutable(f.read())
    return data

def part_1(data: Grid_Immutable, min_ps: int = 100, verbose: bool = False) -> int:
    '''How many cheats would save you at least 100 picoseconds?'''
    #return cheats_by_neighbor(data=data, cheat_ps=2, min_ps=min_ps, verbose=verbose)
    return cheats_by_path(data=data, cheat_ps=2, min_ps=min_ps, verbose=verbose)

def part_2(data: Grid_Immutable, min_ps: int = 100, verbose: bool = False) -> int:
    '''The latest version of the cheating rule permits
    a single cheat that instead lasts at most 20 picoseconds.
    How many cheats would save you at least 100 picoseconds?'''
    #return cheats_by_neighbor(data=data, cheat_ps=20, min_ps=min_ps, verbose=verbose)
    return cheats_by_path(data=data, cheat_ps=20, min_ps=min_ps, verbose=verbose)

class Cheat(NamedTuple):
    '''Each cheat has a distinct start position and end position;
    cheats are uniquely identified by their start position and end position.'''
    start: Point
    end: Point
    savings: int

def cheats_by_neighbor(data: Grid_Immutable, cheat_ps: int, min_ps: int = 100, verbose: bool = False) -> int:
    '''Iterate single points on path, iterate points in radius, check if in path.
    Faster for low cheat_ps (few neighbors), scales terribly (O(n^2)?) with high cheat_ps.'''
    path = data.bfs(data.find('S'), data.find('E'))
    cheats = []
    for i, start in enumerate(path[:-(min_ps+3)]):
        for dest, value in data.neighbors_in_taxi_radius(start, radius=cheat_ps):
            if (value != '#'
                and (j := find(path, dest, i+min_ps+2)) != -1
                and (savings := j - i - start.taxi_distance(dest)) >= min_ps):
                cheats.append(Cheat(start, dest, savings))
    if verbose:
        print(*describe(cheats), sep='\n')
    return len(cheats)

def cheats_by_path(data: Grid_Immutable, cheat_ps: int, min_ps: int = 100, verbose: bool = False) -> int:
    '''Iterate pairs of points on path, check distance.
    O(n^2) in grid size, but constant? linear? in cheat_ps.'''
    # TODO: Try optimizations - store path as sparse grid / dict of distances?
    # https://old.reddit.com/r/adventofcode/comments/1hicdtb/2024_day_20_solutions/m2y56t8/
    # https://topaz.github.io/paste/#XQAAAQBSAgAAAAAAAAAzHIoib6p4r/McpYgEEgWhHoa5LSRMkVi92ASWXgRJn/53WGzJcK4Rqxq0Qyar4BS5DQgYAN35Y8lJcqTY+yjGI8MFLEoYjkrWJOsXQQ76MnCrK/WCLaI4AeJ+YeerS9G3+hr3o9ifx4duubAP4Uk7sw2hyDhgCcbW0Kj9z7VbVmnYfwHz6XYc2QRIo37Uo15C8fWKXBhNKJs2HZ5bp42hQRrBbrt4W+sXf4DqcOSilRg2vmZ8y5kveBOUhixvHzC7WsdlMHWeWs6cY7TPAjPj8vhxVHH5JSlH3Twzs0Dc6xtNZOcdvYt/Vrd6WAJ7h3U9yacAfRUO0phuHaej8oocFxiTf6cp/kZqnE0goF1tuXyF2umof2jgL0oZb6XNcuXlnBs9D9CaTlsxHGvfWSqxAK7Ig5THSUVuZzHPsvHcj2gU2ly4sOehOnTAhoeSDS9UB0T0MvLB6pzIgTYP//TV5gs=
    path = data.bfs(data.find('S'), data.find('E'))
    cheats = []
    for i, start in enumerate(path[:-(min_ps+3)]):
        for j, dest in enumerate(path[i+min_ps+2:], i+min_ps+2):
            if ((dist := start.taxi_distance(dest)) <= cheat_ps
                and (savings := j - i - dist) >= min_ps):
                cheats.append(Cheat(start, dest, savings))
    if verbose:
        print(*describe(cheats), sep='\n')
    return len(cheats)

def describe(cheats: Iterable[Cheat]) -> list[str]:
    return [f'There are {n} cheats that save {ps} ps.' for ps, n in stats(cheats)]

def stats(cheats: Iterable[Cheat]) -> list[tuple[int, int]]:
    return sorted(Counter(cheat.savings for cheat in cheats).items())

if __name__ == '__main__':
    import sys
    sys.exit(main())
