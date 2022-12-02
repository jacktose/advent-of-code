#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/12
Day 12: Passage Pathing
"""

import sys
from collections import defaultdict

def main():
    ex1_data = get_input('./ex1')
    ex2_data = get_input('./ex2')
    ex3_data = get_input('./ex3')
    data = get_input('./input')
    
    print('example 1.1:')
    print(part_both(ex1_data, revisit=False, debug=True), '= 10?')
    
    print('\nexample 1.2:')
    print(part_both(ex2_data, revisit=False, debug=True), '= 19?')
    
    print('\nexample 1.3:')
    print(part_both(ex3_data, revisit=False, debug=False), '= 226?')
    
    print('\npart 1:')
    print(part_both(data, revisit=False), 'paths')
    
    print('\nexample 2.1:')
    print(part_both(ex1_data, revisit=True, debug=True), '= 36?')
    
    print('\nexample 2.2:')
    print(part_both(ex2_data, revisit=True, debug=False), '= 103?')
    
    print('\nexample 2.3:')
    print(part_both(ex3_data, revisit=True, debug=False), '= 3509?')
    
    print('\npart 2:')
    print(part_both(data, revisit=True), 'paths')
    #breakpoint()

def get_input(file='./input'):
    caves = defaultdict(set)
    with open(file, 'r') as f:
        # get pairs defining connected caves:
        for a, z in (line.split('-') for line in f.read().splitlines()):
            # make dict of caves: neighbors:
            caves[a].add(z)
            caves[z].add(a)
    return caves

def part_both(caves, revisit=False, debug=False):
    '''For part 2, just start with revisit=True'''
    paths = find_paths(caves, path=['start'], revisit=revisit)
    if debug: print('\n'.join(','.join(path) for path in paths))
    return len(paths)

def find_paths(caves, path, revisit):
    '''How many paths through this cave system are there that visit small caves at most once?
    Or one small cave twice, if we start with revisit=True?'''
    if path[-1] == 'end':
        return [path]
    paths = []
    for neighbor in caves[path[-1]]:
        if neighbor == 'start':
            continue
        elif neighbor.isupper() or neighbor not in path:
            # recurse, recurse!
            paths += find_paths(caves, path+[neighbor], revisit)
        elif revisit:
            # two hops this time
            paths += find_paths(caves, path+[neighbor], revisit=False)
    return paths


if __name__ == '__main__':
    sys.exit(main())

