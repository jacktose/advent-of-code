#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/14
Day 14: Restroom Redoubt
"""

from __future__ import annotations
from collections import Counter
from collections.abc import Sequence
from math import lcm, prod
import re
from statistics import mean, pstdev, pvariance
from typing import NamedTuple

import sys 
import os
sys.path.append(os.path.abspath('../../util'))
from Grid import RCPair

def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:', part_1(ex_data, RCPair(row=7, col=11)), '= 12?')
    print('\npart 1:', part_1(data))
    #print('\nexample 2:', part_2(ex_data, RCPair(row=7, col=11)), '= _?')
    print('\npart 2:', part_2(data))


def get_input(file='./input'):
    with open(file, 'r') as f:
        data = tuple((RCPair(pr, pc), RCPair(vr, vc)) for pc, pr, vc, vr in (
                      (int(n) for n in re.findall(r'-?\d+', line)) for line in f))
    return data

def part_1(data: Sequence[tuple[RCPair, RCPair]],
           size: RCPair = RCPair(row=103, col=101),
           n: int = 100) -> int:
    '''Predict the motion of the robots in your list
    within a space which is 101 tiles wide and 103 tiles tall.
    What will the safety factor be after exactly 100 seconds have elapsed?'''
    bots = move_all(data, size, n)
    #print_grid((rows, cols), locs, blank_middle=True)
    return safety_factor(bots, size)

def part_2(data: Sequence[tuple[RCPair, RCPair]],
           size: RCPair = RCPair(row=103, col=101)) -> int:
    '''What is the fewest number of seconds that must elapse
    for the robots to display a picture of a Christmas tree?'''
    # This is tricky! Xmas tree pattern is not specified.
    # Honestly, this is reverse-engineered from the answer, which I first got by looking
    # through the grids with the lowest safety factor.
    # There are three methods in here and I don't know which would generalize to other inputs.
    # 1. Zero (or least) overlaps: In my case, the grid with the tree has no robots sharing
    #    the same location. That implies something about the construction of the puzzle,
    #    which might make it general and fast, or might be cheating.
    n_robots = len(data)
    overlaps: list[tuple[int, int]] = []
    # 2. Lowest safety factor: Safety factor increases as robots are spread more evenly
    #    between quadrants. The grid with the tree seems like it would be more clumped.
    #    In my case, it is the 11th least safe. This is really a rough proxy for variance.
    safeties: list[tuple[int, float]] = []
    # 3. Lowest variance: The actual statistical measure of (population) variance.
    #    I'm calling the inverse clumpiness, and the tree pattern is the clumpiest.
    #    This is the most sophisticated method, and the most likely to be (fairly) general.
    variances: list[tuple[int, float]] = []
    for i in range(lcm(*size)):
        bots = move_all(data, size, i)  # Iteration from last locs is maybe faster, but not much.
        overlaps.append((i, n_robots - len(set(bots))))
        safeties.append((i, safety_factor(bots, size)))
        variances.append((i, pvariance(loc.row for loc in bots) + pvariance(loc.col for loc in bots)))
    
    # 1. Zero (or least) overlaps:
    least_overlappy = sorted(overlaps, key=lambda item: item[1])
    #for i, overlap in least_overlappy[:10]:
    #    if overlap > 0:
    #        break
    #    print_grid(size, move_all(data, size, i))
    #    print(i, 'no overlaps\n')

    # 2. Lowest safety factor:
    unsafest = sorted(safeties, key=lambda item: item[1])
    #for i, safety in unsafest[10:11]:
    #    print_grid(size, move_all(data, size, i))
    #    print(i, 'safety:', safety, '\n')

    # 3. Lowest variance:
    clumpiest = sorted(variances, key=lambda item: item[1])
    #for i, var in clumpiest[:1]:
    #    print_grid(size, move_all(data, size, i))
    #    print(i, 'variance:', var, '\n')
    # Trying to find a more rigorous way to detect an unusually clumpy grid (the tree):
    clumpy_mean = mean(variance for _, variance in clumpiest)
    clumpy_sd = pstdev(variance for _, variance in clumpiest)
    clumpy_sigma = [(variance - clumpy_mean) / clumpy_sd for _, variance in clumpiest]
    #print(f'{clumpy_mean=}, {clumpy_sd=}')
    #print('clumpiest:', *zip(clumpiest[:10], clumpy_sigma), sep='\n')

    return clumpiest[0][0]


def move_all(data: Sequence[tuple[RCPair, RCPair]],
            size: RCPair, n: int) -> list[RCPair]:
    '''Move from all points by respective velocities n times'''
    return [move(point, velocity, size, n) for (point, velocity) in data]

def move(start: RCPair, velocity: RCPair, size: RCPair, n: int) -> RCPair:
    '''Move from start by velocity n times'''
    return RCPair((start.row + n*velocity.row) % size.rows,
                  (start.col + n*velocity.col) % size.cols)

def quadrants(points: Sequence[RCPair], size: RCPair) -> Counter[int|None]:
    '''Sort all points into quadrants'''
    return Counter(quadrant(point, size) for point in points)

def quadrant(point: RCPair, size: RCPair) -> int|None:
    '''Return the quadrant of the point within the grid of given size'''
    if point.row not in range(size.rows) or point.col not in range(size.cols):
        raise ValueError('point not in grid')
    middle = RCPair(size.rows//2, size.cols//2)
    if point.row == middle.row or point.col == middle.col:
        return None
    match (point.row // middle.row, point.col // middle.col):
        case (0,   1|2): return 1  # top right
        case (0,   0  ): return 2  # top left
        case (1|2, 0  ): return 3  # bottom left
        case (1|2, 1|2): return 4  # bottom right
    raise ValueError('point not in any quadrant')

def safety_factor(bots: Sequence[RCPair], size: RCPair) -> int:
    '''Calculate the safety factor of all robots on the grid'''
    quads = quadrants(bots, size)
    return prod(v for k, v in quads.items() if k is not None)

def print_grid(size: RCPair, locs: Sequence[RCPair], blank_middle: bool = False) -> None:
    '''Print the grid with the locations of the robots'''
    middle = RCPair(size.rows//2, size.cols//2)
    counts = Counter(locs)
    for r in range(size.rows):
        for c in range(size.cols):
            if blank_middle and (r == middle.row or c == middle.col):
                print(' ', end='')
            elif (count := counts[RCPair(r, c)]) == 0:
                print('.', end='')
            else:
                print(count, end='')
        print()


if __name__ == '__main__':
    import sys
    sys.exit(main())
