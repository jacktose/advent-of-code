#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/12
Day 12: Passage Pathing
"""

import sys

def main():
    ex1_data = get_input('./ex1')
    ex2_data = get_input('./ex2')
    ex3_data = get_input('./ex3')
    data = get_input('./input')
    
    print('example 1.1:')
    print(part_1(ex1_data, debug=True), '= 10?')
    
    print('\nexample 1.2:')
    print(part_1(ex2_data, debug=True), '= 19?')
    
    print('\nexample 1.3:')
    print(part_1(ex3_data, debug=False), '= 226?')
    
    print('\npart 1:')
    print(part_1(data), 'paths')
    
    print('\nexample 2.1:')
    print(part_2(ex1_data, debug=True), '= 36?')
    
    print('\nexample 2.2:')
    print(part_2(ex2_data, debug=False), '= 103?')
    
    print('\nexample 2.3:')
    print(part_2(ex3_data, debug=False), '= 3509?')
    
    print('\npart 2:')
    print(part_2(data), 'paths')
    #breakpoint()

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = [tuple(line.split('-')) for line in f.read().splitlines()]
    return data

def part_1(data, debug=False):
    '''How many paths through this cave system are there that visit small caves at most once?'''
    caves = caves_from_paths(data)
    paths = find_paths_1(caves, path=['start'])
    if debug: print_paths(paths)
    return len(paths)

def part_2(data, debug=False):
    '''a single small cave can be visited at most twice, and the remaining small caves can be visited at most once'''
    caves = caves_from_paths(data)
    paths = find_paths_2(caves, path=['start'])
    if debug: print_paths(paths)
    return len(paths)

def caves_from_paths(paths):
    '''Take tuples defining paths, make dict of caves: neighbors'''
    caves = {}
    for cave in set.union(*(set(p) for p in paths)):
        caves[cave] = {c2 for c1, c2 in paths if c1 == cave}
        caves[cave].update(c1 for c1, c2 in paths if c2 == cave)
    return caves

def find_paths_1(caves, path=['start']):
    if path[-1] == 'end':
        return [path]
    paths = []
    for neighbor in caves[path[-1]]:
        if neighbor.isupper() or neighbor not in path:
            paths.extend(find_paths_1(caves, path+[neighbor]))
    return paths

def find_paths_2(caves, path=['start']):
    if path[-1] == 'end':
        return [path]
    paths = []
    for neighbor in caves[path[-1]]:
        if (
            neighbor.isupper()
            or neighbor not in path
            or (neighbor != 'start'
                and not has_double_small(path))
        ):
            paths.extend(find_paths_2(caves, path+[neighbor]))
    return paths

def has_double_small(path):
    '''Have we already visited some small cave twice?'''
    for i, c in enumerate(path):
        if c.islower() and c in path[i+1:]:
            return True
    else:
        return False

def print_paths(paths):
    '''Output like in examples'''
    print('\n'.join(
        ','.join(path) for path in paths
    ))


if __name__ == '__main__':
    sys.exit(main())

