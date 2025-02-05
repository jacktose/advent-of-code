#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/10
Day 10: Syntax Scoring
"""

import sys
from collections import deque
from functools import reduce
from typing import Any
from collections.abc import Generator, Reversible

def main():
    print('example:')
    ex_data: list[str] = get_input('./example.txt')
    e1, e2 = part_both(ex_data, debug=True)
    print('example 1:')
    print(e1, '= 26397?')
    print('example 2:')
    print(e2, '= 288957?')
    #breakpoint()
    
    print('\nmain:')
    data: list[str] = get_input('./input.txt')
    p1, p2 = part_both(data)
    print('part 1:')
    print(p1)
    print('part 2:')
    print(p2)
    #breakpoint()

def get_input(file: str = './input.txt') -> list[str]:
    with open(file, 'r') as f:
        data = f.read().splitlines()
    return data

def part_both(data: list[str], debug=False) -> tuple[int, int]:
    '''
    1: What is the total syntax error score for those errors?
    2: Find the completion string for each incomplete line,
    score the completion strings, and sort the scores.
    What is the middle score?
    '''
    score1: int = 0
    scores2: set[int] = set()
    for line in data:
        stack: deque = deque()
        for char in line:
            if debug: print(char, end='')
            if char in '([{<':
                stack.append(char)
            elif char in ')]}>':
                last = stack.pop()
                if char != closer_of[last]:
                    if debug: print(' corrupt')
                    score1 += points_corrupt[char]
                    break  # next line
        else:
            if debug: print(' incomplete ', end='')
            score = score_incomplete(stack)
            if debug: print(score)
            scores2.add(score)
    #score2 = statistics.median(scores2)
    score2 = sorted(scores2)[len(scores2) // 2]
    return score1, score2

closer_of: dict[str, str] = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}
points_corrupt: dict[Any, int] = {
    None: 0,
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
points_incomplete: dict[str, int] = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

def score_incomplete(stack: Reversible[str]) -> int:
    closers: Generator[str, None, None] = (closer_of[c] for c in reversed(stack))
    #return reduce(lambda tot, pts: (tot*5) + pts, (values[char] for char in (closer_of(c) for c in stack[::-1])))
    closer_pts: Generator[int, None, None] = (points_incomplete[c] for c in closers)
    scorer = lambda tot, pts: (tot*5) + pts
    score: int = reduce(scorer, closer_pts)
    return score


if __name__ == '__main__':
    sys.exit(main())

