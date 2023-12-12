#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/5
Day 5: If You Give A Seed A Fertilizer
"""

from typing import NamedTuple

def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data), '= 35?')
    
    print('\npart 1:')
    print(part_1(data))
    
    #print('\nexample 2:')
    #print(part_2(ex_data), '= _?')
    
    #print('\npart 2:')
    #print(part_2(data))

    #breakpoint()

def get_input(file='./input'):
    maps = []
    with open(file, 'r') as f:
        seeds = [int(n) for n in f.readline().split()[1:]]
        for line in f:
            if line == '\n':  # blank
                pass
            elif line.endswith(':\n'):  # map name
                #print(line[:-5])
                maps.append([])
            else:  # mapping
                maps[-1].append(tuple(int(n) for n in line.split()))
    return seeds, maps

class Mapping(NamedTuple):
    dst_start: int
    src_start: int
    length: int

    def matches(self, input):
        return input in range(self.src_start, self.src_start + self.length)
    def convert(self, input):
        if not self.matches(input):
            return None
        return self.dst_start + input - self.src_start

class Map():
    def __init__(self, mappings):
        self.mappings = mappings
    def convert(self, n):
        for mapping in self.mappings:
            if mapping.matches(n):
                return mapping.convert(n)
        else:
            return n


def part_1(data):
    '''Convert each seed number through other categories
    until you can find its corresponding location number.
    What is the lowest location number that corresponds to any of the initial seed numbers?'''
    seeds, maps = data
    for i, map in enumerate(maps):
        maps[i] = Map([Mapping(*m) for m in map])
    locations = []
    for seed in seeds:
        locations.append(int(seed))
        for map in maps:
            locations[-1] = map.convert(locations[-1])
    return min(locations)

def part_2(data):
    '''assignment'''


if __name__ == '__main__':
    import sys
    sys.exit(main())

