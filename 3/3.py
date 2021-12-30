#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/2

"""

import sys

def main():
    with open('./input', 'r') as f:
        #data = f.read().splitlines()
        #data = [int(x) for x in f.readlines()]
        #data = [tuple(line.split()) for line in f.readlines()]
        data = [(int(digit) for digit in datum) for datum in f.read().splitlines()]
    #breakpoint()
    print(part_1(data))

def part_1(data):
    half = len(data) // 2
    columns = zip(*data)
    gamma_bits = ''.join('1' if sum(c)>half else '0' for c in columns)
    gamma = int(gamma_bits, 2)
    epsilon = (2 ** len(gamma_bits) - 1) - gamma
    print(f'{gamma =}\n{epsilon =}')
    power = gamma * epsilon
    return power


if __name__ == '__main__':
    sys.exit(main())

