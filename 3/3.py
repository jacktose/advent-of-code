#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/3

"""

import sys

def main():
    data = get_input()
    print('part 1:')
    print(part_1(data))
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = f.read().splitlines()
    # list of strings of digits -> list of tuples of ints:
    data = [tuple(int(digit) for digit in datum) for datum in data]
    return data

def part_1(data):
    #data = list(map(lambda d: tuple(map(int, d)), data))
    half = len(data) // 2
    columns = zip(*data)
    gamma_bits = ''.join('1' if sum(c)>half else '0' for c in columns)
    gamma = int(gamma_bits, 2)
    epsilon = (2 ** len(gamma_bits) - 1) - gamma
    print(f'{gamma = }\n{epsilon = }')
    power = gamma * epsilon
    return power

def part_2(data):
    oxy = decimalize(rating(data, criterion='MOST-COMMON'))
    co2 = decimalize(rating(data, criterion='LEAST-COMMON'))
    print(f'{oxy = }\n{co2 = }')
    return oxy * co2

def rating(data, criterion, index=0):
    '''recurse, recurse!'''
    if len(data) == 1:
        return data[0]
    elif len(data) == 0:
        raise ValueError('No data!')
    digit = crit_digit(data, criterion, index)
    filtered_data = [d for d in data if d[index] == digit]
    #print(f'filtered {len(data)} rows down to {len(filtered_data)} rows with {digit} in index {index}')
    return rating(filtered_data, criterion, index+1)

def crit_digit(data, criterion, index):
    '''This took way too much testing & truth-tabling!'''
    if criterion == 'MOST-COMMON':
        digit = 1 if 2 * sum((d[index] for d in data)) >= len(data) else 0
    elif criterion == 'LEAST-COMMON':
        digit = 1 if 2 * sum((d[index] for d in data)) < len(data) else 0
    else:
        raise ValueError(f'bad criterion: {criterion}')
    return digit

def decimalize(bin_iter):
    #print(f"{bin_iter} -> {int(''.join(map(str, bin_iter)), 2)}")
    return int(''.join(map(str, bin_iter)), 2)


if __name__ == '__main__':
    sys.exit(main())

