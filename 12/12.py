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
    
    print('example 1:')
    print(part_1(ex1_data, debug=True), '= 10?')
    
    print('example 2:')
    print(part_1(ex2_data, debug=True), '= 19?')
    
    print('example 3:')
    print(part_1(ex3_data, debug=False), '= 226?')
    
    print('\npart 1:')
    print(part_1(data), 'paths')
    
    #print('\nexample 2:')
    #print(part_2(ex_data))
    
    #print('\npart 2:')
    #print(part_2(data))
    #breakpoint()

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = [tuple(line.split('-')) for line in f.read().splitlines()]
    return data

def part_1(data, debug=False):
    '''How many paths through this cave system are there that visit small caves at most once?'''
    cave_set = set()
    for d in data:
        cave_set.update(d)
    caves = {}
    for cave in cave_set:
        caves[cave] = {c2 for c1, c2 in data if c1 == cave}
        caves[cave].update(c1 for c1, c2 in data if c2 == cave)
    paths = find_paths(caves, path=['start'])
    if debug:
        for path in paths:
            print(','.join(path))
    return len(paths)

def find_paths(caves, path=['start']):
    if path[-1] == 'end':
        return [path]
    paths = []
    for neighbor in caves[path[-1]]:
        if neighbor.isupper() or neighbor not in path:
            paths.extend(find_paths(caves, path+[neighbor]))
    return paths



def part_2(data):
    '''assignment'''


if __name__ == '__main__':
    sys.exit(main())

