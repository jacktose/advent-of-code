#!/usr/bin/env python3

"""
https://adventofcode.com/2024/day/13
Day 13: Claw Contraption
"""

from __future__ import annotations
import re
from typing import NamedTuple

def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data), '= 480?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= _?')
    
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = tuple(Claw.from_string(s) for s in f.read().split('\n\n'))
    return data

def part_1(data) -> int:
    '''What is the fewest tokens you would have to spend to win all possible prizes?'''
    return sum(cost for claw in data if (cost := claw.cost()) is not None)

def part_2(data) -> int:
    '''Using the corrected prize coordinates, figure out how to win as many prizes as possible.
    What is the fewest tokens you would have to spend to win all possible prizes?'''
    return part_1(claw.boosted(10000000000000, 10000000000000) for claw in data)

class Claw(NamedTuple):
    a: Point
    b: Point
    prize: Point
    a_cost: int = 3
    b_cost: int = 1

    @staticmethod
    def from_string(string: str) -> Claw:
        ax, ay, bx, by, px, py = (int(n) for n in re.findall(r'[+-]?\d+', string))
        return Claw(Point(ax, ay), Point(bx, by), Point(px, py))
    
    def boosted(self, x_boost: int, y_boost: int) -> Claw:
        return Claw(self.a, self.b,
                    self.prize + Point(x_boost, y_boost),
                    self.a_cost, self.b_cost)
    
    def cost(self) -> int|None:
        '''Calculate the cost of a given solution (na, nb)'''
        if (solution := self.solution()) is None:
            return None
        na, nb = solution
        return (na * self.a_cost) + (nb * self.b_cost)

    def solution(self) -> tuple[int, int]|None:
        '''Find the number of presses of a, b to reach prize: p = na*a + nb*b'''
        # Find the intersection of a line with slope a through the origin, and a line with slope b through the prize
        # Algebraic!
        isec_x = self.a.x * (self.prize.y * self.b.x - self.prize.x * self.b.y) // (self.a.y * self.b.x - self.a.x * self.b.y)
        isec_y = self.a.y * isec_x // self.a.x  # or: y = Fraction(self.a.y, self.a.x) * x
        a_vec = Point(isec_x, isec_y)  # From origin to intersection along slope a
        b_vec = self.prize - a_vec  # From intersection to prize along slope b
        if 0 == (a_vec.x % self.a.x) == (a_vec.y % self.a.y) == (b_vec.x % self.b.x) == (b_vec.y % self.b.y):
            # Solution uses integer presses of a and b
            na = a_vec.x // self.a.x
            nb = b_vec.x // self.b.x
            return na, nb
        else:
            return None

class Point(complex):
    @property
    def x(self) -> int:
        return int(self.real)
    @property
    def y(self) -> int:
        return int(self.imag)

    def __add__(self, other: Point) -> Point:
        return Point(super().__add__(other))
    def __sub__(self, other: Point) -> Point:
        return Point(super().__sub__(other))
        

if __name__ == '__main__':
    import sys
    sys.exit(main())
