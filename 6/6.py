#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/6
Day 6: Lanternfish
"""

import sys
from collections import Counter, deque

def main():
    test()
    data = get_input()
    print(part_1(data), 'lanternfish')
    print(part_2(data), 'lanternfish')

def get_input(file='./input'):
    with open(file, 'r') as f:
        # read every other character -> convert to int -> count frequency:
        # [::2] is sliiightly faster than .split(',')
        # (collections.Counter is the fastest way to count (see bottom))
        data = Counter((int(n) for n in f.read()[::2]))
    return data

def test():
    print('test:')
    test_data = Counter([3,4,3,1,2])  # from example
    for days, target in [(18, 26), (80, 5934), (256, 26984457539)]:
        fishies = propogate(test_data, days=days, output=days<20)
        print(f'{fishies} = {target}? {fishies == target}')

def part_1(data):
    '''How many lanternfish would there be after 80 days?'''
    print('\npart 1:')
    return propogate(data, days=80)

def part_2(data):
    '''How many lanternfish would there be after 256 days?'''
    print('\npart 2:')
    return propogate(data, days=256)

def propogate(cohort_count, days, output=False):
    '''How many lanterfish after `days` days?
    Don't model each fish. Rather, track sizes of age cohorts.
    Deque index is days to spawn. Value is qty in cohort.
    Rotate deque left to move all cohorts closer to 0. Looks like:
    example:   |0 1 2 3 4 5 6 7 8
    3 4 3 1 2  |  1 1 2 1
    2 3 2 0 1  |1 1 2 1
    1 2 1 6 0 8|1 2 1       1   1
    '''
    fishies = deque(cohort_count[cohort] for cohort in range(9))
    for d in range(days):
        # everyone gets closer to 0, but 0s wrap around to 8:
        fishies.rotate(-1)
        # and the 8s (yesterday's zeros) are also added to the 6s:
        fishies[6] += fishies [8]
        if output:
            #print(list(range(9)))
            print(list(fishies))
    return sum(fishies)


if __name__ == '__main__':
    sys.exit(main())



''' efficiency experiments:
    print(timeit(lambda: fishies1(data), number=100_000))
    print(timeit(lambda: fishies2(data), number=100_000))
    print(timeit(lambda: fishies3(data), number=100_000))

def fishies1(data):
    # 3.6s / 100k
    return {t: data.count(t) for t in range(1,9)}

def fishies2(data):
    # 2.9s / 100k
    fishies = {t:0 for t in range(1,9)}
    for t in data:
        fishies[t] += 1
    return fishies

def fishies3(data):
    # 1.5s / 100k
    c = Counter(data)
    #return c
    #return {t: c[t] for t in sorted(c)}
    return {t: c[t] for t in range(1,9)}
'''
