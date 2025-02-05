#!/usr/bin/env python3

"""
https://adventofcode.com/2022/day/2
Day 2: Rock Paper Scissors
"""

def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data), '= 15?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 12?')
    
    print('\npart 2:')
    print(part_2(data))

    #breakpoint()

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = f.read().splitlines()
    return data

def part_1(data):
    '''What would your total score be if everything
    goes exactly according to your strategy guide?'''

    score = {
        'A X': 3 + 1,
        'A Y': 6 + 2,
        'A Z': 0 + 3,
        'B X': 0 + 1,
        'B Y': 3 + 2,
        'B Z': 6 + 3,
        'C X': 6 + 1,
        'C Y': 0 + 2,
        'C Z': 3 + 3,
    }
    #return functools.reduce((lambda total, game: total + score[game]), data, 0)
    return sum(score[game] for game in data)

def part_2(data):
    '''Following the Elf's instructions for the second column,
    what would your total score be if everything
    goes exactly according to your strategy guide?'''

    score = {
        'A X': 0 + 3,
        'A Y': 3 + 1,
        'A Z': 6 + 2,
        'B X': 0 + 1,
        'B Y': 3 + 2,
        'B Z': 6 + 3,
        'C X': 0 + 2,
        'C Y': 3 + 3,
        'C Z': 6 + 1,
    }
    #return functools.reduce((lambda total, game: total + score[game]), data, 0)
    return sum(score[game] for game in data)

if __name__ == '__main__':
    import sys
    sys.exit(main())

