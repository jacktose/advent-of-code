#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/1
Day 1: Calorie Counting
"""


def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data), '= 24000?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 45000?')
    
    print('\npart 2:')
    print(part_2(data))

    #breakpoint()

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = f.read().splitlines()
    return data

def part_1(data):
    '''Find the Elf carrying the most Calories.
    How many total Calories is that Elf carrying?'''
    this = 0
    most = 0
    for line in data:
        match line:
            case '':
                most = max(most, this)
                #print(f'{this} ({most})')
                this = 0
            case calories:
                this += int(calories)
    return most

def part_2(data):
    '''Find the top three Elves carrying the most Calories.
    How many Calories are those Elves carrying in total?'''
    elves = [0]
    for line in data:
        match line:
            case '':
                elves.append(0)
            case calories:
                elves[-1] += int(calories)
    elves.sort(reverse=True)
    #print(elves[0:3])
    return sum(elves[0:3])


import sys
if __name__ == '__main__':
    sys.exit(main())

