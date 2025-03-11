#!/usr/bin/env python3

"""
https://adventofcode.com/2024/day/23
Day 23: LAN Party
"""

from collections import defaultdict
from collections.abc import Collection, Mapping, Set
from itertools import combinations

def main():
    ex_data = get_input('./example.txt')
    data = get_input('./input.txt')
    
    print('example 1:', part_1(ex_data), '= 7?', '\n')
    print('part 1:',    part_1(data),            '\n')  # 1485
    print('example 2:', part_2(ex_data), '= co,de,ka,ta?', '\n')
    print('part 2:',    part_2(data),                      '\n')  # cc,dz,ea,hj,if,it,kf,qo,sk,ug,ut,uv,wh

def get_input(file='./input.txt') -> dict[str, Set[str]]:
    with open(file, 'r') as f:
        data: tuple[tuple[str, str], ...] = tuple((line[0:2], line[3:5]) for line in f)
        graph = defaultdict(set)
        for a, b in data:
            graph[a].add(b)
            graph[b].add(a)
    return {k: frozenset(v) for k, v in graph.items()}

def part_1(graph: Mapping[str, Collection[str]]) -> int:
    '''Find all the sets of three inter-connected computers.
    How many contain at least one computer with a name that starts with t?'''
    triads: set[frozenset[str]] = set()
    for comp, neighbors in graph.items():
        if comp[0] != 't':
            continue
        for a, b in combinations(neighbors, 2):
            if b in graph[a]:
                triads.add(frozenset({comp, a, b}))
    #print(*triads, sep='\n')
    return len(triads)

def part_2(graph: Mapping[str, Set[str]]) -> str:
    '''The LAN party is the largest set of computers that are all connected to each other.
    The password to get into the LAN party is the name of every computer at the LAN party,
    sorted alphabetically, then joined together with commas.
    What is the password to get into the LAN party?'''
    next_rank = {frozenset({k}) for k in graph.keys()}    
    while next_rank:
        print(f'{len(next(iter(next_rank)))}: {len(next_rank)}')
        last_rank = next_rank
        next_rank = set()
        for mesh in last_rank:
            for computer, neighbors in graph.items():
                if neighbors >= mesh:
                    next_rank.add(mesh | {computer})
    lan = last_rank.pop()
    return ','.join(sorted(lan))


if __name__ == '__main__':
    import sys
    sys.exit(main())
