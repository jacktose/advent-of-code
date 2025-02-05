#!/usr/bin/env python3

"""
https://adventofcode.com/2022/day/3
Day 3: Rucksack Reorganization
"""

def main():
    ex_data = get_input('./example.txt')
    data = get_input('./input.txt')
    
    print('example 1:')
    print(part_1(ex_data), '= 157?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 70?')
    
    print('\npart 2:')
    print(part_2(data))

    #breakpoint()

def get_input(file='./input.txt'):
    with open(file, 'r') as f:
        data = f.read().splitlines()
    return data

def priority(char):
    return ord(char) - 96 if char > 'Z' else ord(char) - 38

def part_1(data):
    '''Find the item type that appears in both compartments of each rucksack.
    What is the sum of the priorities of those item types?'''
    priority_sum = 0
    for sack in data:
        for char in sack:
            if char in sack[len(sack)//2:]:
                priority_sum += priority(char)
                break
        else:
            print('BAD SACK')
    return priority_sum

def part_2(data):
    '''Find the item type that corresponds to the badges of each three-Elf group.
    What is the sum of the priorities of those item types?'''
    return sum(priority(set.intersection(*group).pop()) for group in zip(*[map(set, data)]*3))


if __name__ == '__main__':
    import sys
    sys.exit(main())

