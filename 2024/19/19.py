#!/usr/bin/env python3

"""
https://adventofcode.com/2024/day/19
Day 19: Linen Layout
"""

from functools import cache
#import time

def main():
    ex_data = get_input('./example.txt')
    data = get_input('./input.txt')
    
    print('example 1:', part_1(ex_data), '= 6?')
    #start = time.time()
    print('\npart 1:', part_1(data))  # 300
    #end = time.time(); print(end - start)
    print('\nexample 2:', part_2(ex_data), '= 16?')
    print('\npart 2:', part_2(data))  # 624802218898092

def get_input(file='./input.txt') -> tuple[tuple, tuple]:
    with open(file, 'r') as f:
        patterns, designs = f.read().split('\n\n')
    patterns = patterns.split(', ')
    designs = designs.splitlines()
    return tuple(patterns), tuple(designs)

def part_1(data) -> int:
    '''How many designs are possible?'''
    patterns, designs = data
    patterns = sorted(patterns, key=len, reverse=True)  # Try from longest to shortest
    # TODO: More preprocessing patterns?
    #       Does it help to remove long patterns that comprise shorter patterns?
    #       Or are they effectively just precomputed cache?

    # re.fullmatch() is too slow for this. Needs caching on subproblems to speed backtracking.
    @cache
    def match(design: str) -> bool:
        if design == '':
            return True
        for pattern in patterns:
            if design.startswith(pattern):
                if match(design[len(pattern):]):
                    return True
                # else continue (backtrack)
        else:
            return False

    return sum(1 for design in designs if match(design))
    #answer: int = 0
    #for i, design in enumerate(designs):
    #    print(i, design, sep='\t', end='\t')
    #    if match(design):
    #        answer += 1
    #        print('✅')
    #    else:
    #        print('❌')
    #return answer

def part_2(data) -> int:
    '''Add up the number of different ways you could make each design'''
    patterns, designs = data

    @cache
    def ways(design: str) -> int:
        if design == '':
            return 1
        count = 0
        for pattern in patterns:
            if design.startswith(pattern):
                count += ways(design[len(pattern):])
        return count

    return sum(map(ways, designs))


if __name__ == '__main__':
    import sys
    sys.exit(main())
