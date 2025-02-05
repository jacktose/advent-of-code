#!/usr/bin/env python3

"""
https://adventofcode.com/2022/day/6
Day 6: Tuning Trouble
"""

from collections import deque

def main():
    ex_data = get_ex_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    for ex_datum in ex_data:
        print(part_1(ex_datum[0]), f'= {ex_datum[1]}?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    for ex_datum in ex_data:
        print(part_2(ex_datum[0]), f'= {ex_datum[2]}?')
    
    print('\npart 2:')
    print(part_2(data))

    #breakpoint()

def get_ex_input(file='./example'):
    with open(file, 'r') as f:
        data = [line.split() for line in f]
    return data

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = f.read().rstrip()
    return data

def all_unique(seq):
    for i, elem in enumerate(seq):
        try:
            seq.index(elem, 0, i)
        except ValueError:
            continue
        return False
    else:
        return True

def part_1(data, window=4):
    '''How many characters need to be processed before
    the first start-of-packet marker is detected?'''
    buffer = deque((), maxlen=window)
    for i, char in enumerate(data):
        #print(i, char, buffer)
        if all_unique(buffer) and len(buffer) == window:
            return i
        else:
            buffer.append(char)
    else:
        raise ValueError('No marker found')

def part_2(data, window=14):
    '''How many characters need to be processed before
    the first start-of-message marker is detected?'''
    return part_1(data, window)


if __name__ == '__main__':
    import sys
    sys.exit(main())

