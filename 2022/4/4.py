#!/usr/bin/env python3

"""
https://adventofcode.com/2022/day/4
Day 4: Camp Cleanup
"""

def main():
    ex_data = get_input('./example.txt')
    data = get_input('./input.txt')
    
    print('example 1:')
    print(part_1(ex_data), '= 2?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 4?')
    
    print('\npart 2:')
    print(part_2(data))

    #breakpoint()

def get_input(file='./input.txt'):
    with open(file, 'r') as f:
        data = [tuple(tuple(map(int, elf.split('-'))) for elf in
                tuple(pair.rstrip().split(','))) for pair in f]
    return data

def contain(pair):
    return (pair[0][0] <= pair[1][0] and pair[0][1] >= pair[1][1]
         or pair[0][0] >= pair[1][0] and pair[0][1] <= pair[1][1])

def overlap(pair):
    return pair[0][0] <= pair[1][1] and pair[0][1] >= pair[1][0]

def part_1(data):
    '''In how many assignment pairs does one range fully contain the other?'''
    return sum(contain(pair) for pair in data)

def part_2(data):
    '''assignment'''
    return sum(overlap(pair) for pair in data)


if __name__ == '__main__':
    import sys
    sys.exit(main())

