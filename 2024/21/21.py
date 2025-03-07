#!/usr/bin/env python3

"""
https://adventofcode.com/2024/day/21
Day 21: Keypad Conundrum
"""

from functools import cache
from itertools import pairwise
from typing import Literal

import sys; import os
sys.path.append(os.path.abspath('../../util'))
from Grid import Point

def main():
    ex_data = get_input('./example.txt')
    data = get_input('./input.txt')
    
    print('example 1:', part_1(ex_data), '= 126384?',   '\n')
    print('part 1:',    part_1(data),                   '\n')  # 242484
    print('example 2:', part_2(ex_data), '= _?',        '\n')  # Example answer not given! (154115708116294)
    print('part 2:',    part_2(data),                   '\n')  # 294209504640384

def get_input(file='./input.txt'):
    with open(file, 'r') as f:
        data = f.read().splitlines()
    return data

KEYPADS: dict[str, dict[str, Point]] = {
    'num': {
        '7': Point(0, 0), '8': Point(0, 1), '9': Point(0, 2),
        '4': Point(1, 0), '5': Point(1, 1), '6': Point(1, 2),
        '1': Point(2, 0), '2': Point(2, 1), '3': Point(2, 2),
        ' ': Point(3, 0), '0': Point(3, 1), 'A': Point(3, 2),
    },
    'dir': {
        ' ': Point(0, 0), '^': Point(0, 1), 'A': Point(0, 2),
        '<': Point(1, 0), 'v': Point(1, 1), '>': Point(1, 2),
    }
}

def part_1(data: list[str]) -> int:
    '''Find the fewest number of button presses you'll need to perform
    in order to cause the robot in front of the door to type each code.
    What is the sum of the complexities of the five codes on your list?'''
    return sum(complexity(code) for code in data)

def part_2(data: list[str]) -> int:
    '''This time, many more robots are involved. In summary, there are the following keypads:
    - One directional keypad that you are using.
    - 25 directional keypads that robots are using.
    - One numeric keypad (on a door) that a robot is using.
    What is the sum of the complexities of the five codes on your list?'''
    return sum(complexity(code, depth=26) for code in data)

def complexity(code: str, depth: int = 3) -> int:
    '''Calculate the "complexity" by multiplying:
    - The length of the shortest sequence of button presses
    - The numeric part of the code'''
    return len_buttons(code, depth=depth) * int(code[:-1])

@cache
def len_buttons(code: str, keypad: Literal['num', 'dir'] = 'num', depth: int = 3) -> int:
    '''Count the final number of button presses after expanding through `depth` levels.'''
    if depth == 0:
        return len(code)
    global KEYPADS; kp = KEYPADS[keypad]
    total: int = 0
    for start_c, end_c in pairwise('A' + code):
        paths = find_paths(kp[start_c], kp[end_c], kp[' '])
        total += min(len_buttons(path+'A', keypad='dir', depth=depth-1) for path in paths)
    return total

#@cache
def find_paths(start: Point, end: Point, blank: Point) -> tuple[str, ...]:
    '''Find the 1 or 2 most efficient, legal paths
    from one point to another (avoiding the blank).'''
    vector = end - start
    h = abs(vector.cols) * ('<' if vector.cols < 0 else '>')
    v = abs(vector.rows) * ('^' if vector.rows < 0 else 'v')
    if not v:
        return (h,)
    elif not h:
        return (v,)
    elif start + vector.component_row == blank:
        return (h+v,)  # vert first would hit blank
    elif start + vector.component_col == blank:
        return (v+h,)  # horiz first would hit blank
    else:
        return (h+v, v+h)
        # NB: There are optimal orderings, so I wouldn't have to try both, which means
        # I wouldn't have to return a tuple, iterate, and take the min().
        # But I learned that from redditors in the solution thread, so it's not fair.
        # https://old.reddit.com/r/adventofcode/comments/1hj2odw/2024_day_21_solutions/mgzamhv/?context=99


if __name__ == '__main__':
    import sys
    sys.exit(main())
