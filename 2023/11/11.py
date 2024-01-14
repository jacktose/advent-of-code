#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/11
Day 11: Cosmic Expansion
"""

from typing import Sequence

def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data), '= 374?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2.1:')
    print(part_2(ex_data, expansion=10), '= 1030?')
    print('\nexample 2.2:')
    print(part_2(ex_data, expansion=100), '= 8410?')
    
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = tuple(tuple(line) for line in f.read().splitlines())
    return data

def part_1(data: tuple[tuple[str, ...], ...], expansion: int = 2) -> int:
    '''Expand the universe, then find the length of the shortest path
    between every pair of galaxies. What is the sum of these lengths?'''
    return part_both(data, expansion=expansion)
    #sky = expand(data)
    ##pprint(sky)
    #galaxies = [(r, c)
    #            for (r, row)   in enumerate(sky)
    #            for (c, point) in enumerate(row)
    #            if point == '#']
    ##print(galaxies)
    #dist = 0
    #for i, g1 in enumerate(galaxies):
    #    for g2 in galaxies[i+1:]:
    #        dist += distance_simple(g1, g2)
    #return dist

#def distance_simple(p1, p2) -> int:
#    return (p2[0] - p1[0]) + abs(p2[1] - p1[1])

#def expand(sky: Sequence[Sequence[str]]) -> list[list[str]]:
#    empty_rows = ['#' not in row for row in sky]
#    cols = ((row[c] for row in sky) for c in range(len(sky[0])))
#    empty_cols = ['#' not in col for col in cols]
#    xsky = []
#    for r, row in enumerate(sky):
#        xsky.append([])
#        for c, point in enumerate(row):
#            xsky[-1].extend([point]*(2 if empty_cols[c] else 1))
#        if empty_rows[r]:
#            xsky.append(xsky[-1])
#    return xsky

def part_2(data: tuple[tuple[str, ...], ...], expansion: int = 1_000_000) -> int:
    '''Now, instead of the expansion you did before,
    make each empty row or column one million times larger.
    What is the sum of these lengths?'''
    return part_both(data, expansion=expansion)

#TODO: Make this a Sky object?
def part_both(data: tuple[tuple[str, ...], ...], expansion: int) -> int:
    empty_rows = ['#' not in row for row in data]
    cols = ((row[c] for row in data) for c in range(len(data[0])))
    empty_cols = ['#' not in col for col in cols]
    galaxies = [(r, c)
                for (r, row)   in enumerate(data)
                for (c, point) in enumerate(row)
                if point == '#']
    #print(galaxies)
    dist = 0
    for i, g1 in enumerate(galaxies):
        for g2 in galaxies[i+1:]:
            dist += distance(g1, g2, empty_rows, empty_cols, expansion)
    return dist

def distance(p1, p2, empty_rows, empty_cols, expansion) -> int:
    rs = sorted((p1[0], p2[0]))
    cs = sorted((p1[1], p2[1]))
    dist = (rs[1] - rs[0]) + (cs[1] - cs[0])
    dist += (expansion - 1) * sum(empty_rows[rs[0]:rs[1]])
    dist += (expansion - 1)* sum(empty_cols[cs[0]:cs[1]])
    return dist


if __name__ == '__main__':
    import sys
    sys.exit(main())

