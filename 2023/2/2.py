#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/2
Day 2: Cube Conundrum
"""

import re
from math import prod

def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data), '= 8?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 2286?')
    
    print('\npart 2:')
    print(part_2(data))

    #breakpoint()

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = f.read().splitlines()
    return data

def part_1(data):
    '''Which games would have been possible if the bag contained
    only 12 red cubes, 13 green cubes, and 14 blue cubes?
    What is the sum of the IDs of the possible games?'''

    color_max = {'red': 12, 'green': 13, 'blue': 14}
    total = 0
    for line in data:
        #valid = True
        #game, results = line.split(':')
        #results = results.split(';')
        #for result in results:
        #    colors = result.split(',')
        #    for color in colors:
        #        num, name = color.split()
        #        if int(num) > max[name]:
        #            valid = False
        #if valid == True:
        #    total += int(game.split()[1])

        for result in re.findall(r' (\d+) (red|green|blue)', line):
            if int(result[0]) > color_max[result[1]]:
                break
        else:
            total += int(re.match(r'Game (\d+):', line)[1])
    return total

def part_2(data):
    '''For each game, find the minimum set of cubes that must have been present.
    What is the sum of the power of these sets?'''
    return sum(cube_power(re.findall(r' (\d+) (red|green|blue)', line)) for line in data)

def cube_power(game):
    color_min = {'red': 0, 'green': 0, 'blue': 0}
    for result in game:
        color_min[result[1]] = max(color_min[result[1]], int(result[0]))
    return prod(color_min.values())

if __name__ == '__main__':
    import sys
    sys.exit(main())
