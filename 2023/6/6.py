#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/6
Day 6: Wait For It
"""

from math import ceil, prod


def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data), '= 288?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 71503?')
    
    print('\npart 2:')
    print(part_2(data))

    #breakpoint()

def get_input(file='./input'):
    with open(file, 'r') as f:
        time, distance = f.read().splitlines()
    return (time.split()[1:], distance.split()[1:])

def part_1(data):
    '''Determine the number of ways you could beat the record in each race.
    What do you get if you multiply these numbers together?'''
    time, distance = (map(int, line) for line in data)
    return prod(ways_to_win(time, distance) for (time, distance) in zip(time, distance))

def part_2(data):
    '''How many ways can you beat the record in this one much longer race?'''
    time, distance = (int(''.join(line)) for line in data)
    return ways_to_win(time, distance)

def ways_to_win(time, distance):
    '''
    t_travel = t_race - t_button
    d_travel = t_travel * speed
    speed = t_button * (mm/ms^2)
    d_travel > d_record

    d_record < (t_travel * speed)
    d_record < (t_race - t_button) * (t_button)
    0 < -t_button^2 + t_race*t_button - d_record

    ( -b +/- sqrt(b^2 - 4ac) ) / 2a
    ( -t_race +/- sqrt(t_race^2 - 4*-1*-d_record) ) / 2*-1
    (  t_race +/- sqrt(t_race^2 - 4*d_record) ) / 2
    '''
    roots = quadratic(-1, time, -distance)
    limits = (int(roots[0]), int(ceil(roots[1])))
    return limits[1] - limits[0] - 1

def quadratic(a: float, b: float, c: float) -> tuple[float, float]:
    '''Find zeros of quadratic equation. Ignore possility of complex numbers.'''
    from math import sqrt
    discriminant = (b**2) - (4 * a * c)
    # Check here for negative
    left = -b / (2 * a)
    right = sqrt(abs(discriminant)) / (2 * a)
    return tuple(sorted((left - right, left + right)))


if __name__ == '__main__':
    import sys
    sys.exit(main())

