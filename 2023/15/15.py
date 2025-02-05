#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/15
Day 15: Lens Library
"""

import re

def main():
    ex_data_1 = ['HASH']
    ex_data_2 = get_input('./example.txt')
    data = get_input('./input.txt')
    
    print('example 1.1:')
    print(part_1(ex_data_1), '= 52?')
    
    print('\nexample 1.2:')
    print(part_1(ex_data_2), '= 1320?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data_2), '= 145?')
    
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input.txt'):
    with open(file, 'r') as f:
        data = f.read().rstrip().split(',')
    return data

def part_1(data: list[str]) -> int:
    '''Run the HASH algorithm on each step in the initialization sequence.
    What is the sum of the results?'''
    return sum(hash(s) for s in data)

def part_2(data):
    '''Follow the initialization sequence.
    What is the focusing power of the resulting lens configuration?'''
    boxes: list[dict[str, int]] = [{} for _ in range(256)]
    for instruction in data:
        box, op, label, fl = hashmap(instruction)
        if op == '-':
            boxes[box].pop(label, None)
        elif op == '=':
            boxes[box][label] = fl
    return sum((box * slot * fl)
               for (box, lenses) in enumerate(boxes, start=1)
               for (slot, fl) in enumerate(lenses.values(), start=1))

def hash(string: str) -> int:
    '''Holiday ASCII String Helper algorithm'''
    ret = 0
    for c in string:
        ret += ord(c)
        ret *= 17
        ret %= 256
    return ret

def hashmap(string: str) -> tuple[int, str, str, int|None]:
    '''Holiday ASCII String Helper Manual Arrangement Procedure'''
    label, operation, focal_length = re.fullmatch(r'([a-z]+)([-=])(\d*)', string).groups()
    box = hash(label)
    focal_length = int(focal_length) if operation == '=' else None
    return box, operation, label, focal_length


if __name__ == '__main__':
    import sys
    sys.exit(main())

