#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/2

"""

import sys

def main():
    with open('./input.txt', 'r') as f:
        #data = f.read().splitlines()
        #data = [int(x) for x in f.readlines()]
        #data = [tuple(line.split()) for line in f.readlines()]
        data = [(a, int(b)) for a,b in (line.split() for line in f.readlines())]
    #breakpoint()
    x, y = part_1(data)
    print(f'{x =}\n{y =}\nproduct = {x*y}')
    x, y = part_2(data)
    print(f'{x =}\n{y =}\nproduct = {x*y}')

def part_1(data):
    x = 0
    y = 0
    for d in data:
        # could tighten this up: https://www.reddit.com/r/adventofcode/comments/r6zd93/2021_day_2_solutions/hmwbtbe/
        match d[0]:
            case 'forward':
                x += d[1]
            case 'down':
                y += d[1]
            case 'up':
                y -= d[1]
    return (x, y)

def part_2(data):
    aim = 0
    x = 0
    y = 0
    for d in data:
        match d[0]:
            case 'forward':
                x += d[1]
                y += aim * d[1]
            case 'down':
                aim += d[1]
            case 'up':
                aim -= d[1]
    return (x, y)

if __name__ == '__main__':
    sys.exit(main())

