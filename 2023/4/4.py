#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/4
Day 4: Scratchcards
"""

def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data), '= 13?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 30?')
    
    print('\npart 2:')
    print(part_2(data))

    #breakpoint()

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = f.read().splitlines()
    return data

def part_1(data):
    '''How many points are they worth in total?'''
    return sum(int(2 ** (num_winners(line) - 1)) for line in data)

def part_2(data):
    '''How many total scratchcards do you end up with?'''
    counts = [1] * len(data)
    for n, line in enumerate(data):
        for i in range(n+1, n+1+num_winners(line)):
            counts[i] += counts[n]
    return sum(counts)

def num_winners(card):
    '''How many numbers that we have are winning numbers?'''
    win, _, have = card.partition('|')
    win = set(win.split()[2:])  # remove Game ##:
    have = set(have.split())
    return len(win & have)  # set intersection


if __name__ == '__main__':
    import sys
    sys.exit(main())

