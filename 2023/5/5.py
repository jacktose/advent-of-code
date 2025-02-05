#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/5
Day 5: If You Give A Seed A Fertilizer
"""

from dataclasses import dataclass

def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data), '= 35?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 46?')
    
    print('\npart 2:')
    print(part_2(data))

    #breakpoint()

def get_input(file='./input'):
    with open(file, 'r') as f:
        data_seeds, *data_maps = f.read().strip().split('\n\n')
    seeds = [int(n) for n in data_seeds.split(':')[1].split()]
    maps = [tuple(tuple(int(n) for n in mapping.split()) for mapping in m.split('\n')[1:]) for m in data_maps]
    return seeds, maps

def part_1(data):
    '''Convert each seed number through other categories
    until you can find its corresponding location number.
    What is the lowest location number that corresponds to any of the initial seed numbers?'''
    seeds, maps = data
    maps = [Map([Mapping(*mapping_tup) for mapping_tup in map_tup]) for map_tup in maps]
    locations = []
    for seed in seeds:
        locations.append(int(seed))
        for map in maps:
            locations[-1] = map.convert(locations[-1])
    return min(locations)

def part_2(data):
    '''The seeds: line actually describes ranges of seed numbers.
    What is the lowest location number that corresponds to any of the initial seed numbers?'''
    seeds, maps = data
    seeds = [range(start, start+len) for start, len in zip(seeds[::2], seeds[1::2])]
    maps = [Map([Mapping(mapping_tup[1], mapping_tup[0], mapping_tup[2]) for mapping_tup in map_tup]) for map_tup in maps[::-1]]
    allmap = maps[0]
    for map in maps[1:]:
        allmap = allmap.merge_in(map)
    #seeds
    for mapping in allmap.mappings:
        for seed_range in seeds:
            if seed_range.start in mapping.dst:
                return seed_range.start - mapping.delta
            if mapping.dst.start in seed_range:
                return mapping.src.start
    else:
        return False


@dataclass
class Mapping:
    dst_start: int
    src_start: int
    length: int

    def __post_init__(self):
        self.dst = range(self.dst_start, self.dst_start + self.length)
        self.src = range(self.src_start, self.src_start + self.length)
        self.delta = self.dst_start - self.src_start

    def __contains__(self, item):
        return item in self.src
    
    #def __str__(self):
    #    return f'[{self.src.start}, {self.src.stop})  {"+" if self.delta >= 0 else ""}{self.delta}'
    
    def convert(self, input):
        if input not in self:
            raise ValueError(f'{input} not in source range [{self.src.start}, {self.src.stop})')
        return input + self.delta
    
@dataclass
class Map:
    mappings: list[Mapping]

    def __post_init__(self):
        self.mappings.sort(key=lambda m: m.src_start)
        filler_mappings = []
        if self.mappings[0].src.start > 0:
            filler_mappings.append(Mapping(dst_start=0, src_start=0, length=self.mappings[0].src.start))
        if self.mappings[-1].src.stop < sys.maxsize:
            filler_mappings.append(Mapping(dst_start=self.mappings[-1].src.stop,
                                          src_start=self.mappings[-1].src.stop,
                                          length=sys.maxsize - self.mappings[-1].src.stop))
        for i in range(len(self.mappings) - 1):
            # no gap:
            if self.mappings[i].src.stop == self.mappings[i+1].src.start:
                continue
            # fill gap:
            filler_mappings.append(Mapping(dst_start=self.mappings[i].src.stop,
                                          src_start=self.mappings[i].src.stop,
                                          length=self.mappings[i+1].src.start - self.mappings[i].src.stop))
        self.mappings += filler_mappings
        self.mappings.sort(key=lambda m: m.src_start)

    def convert(self, input):
        for mapping in self.mappings:
            try:
                return mapping.convert(input)
            except ValueError:
                continue
        else:
            #return input
            raise ValueError

    def merge_in(self, other):
        combined = []
        for mapping in sorted(self.mappings, key=lambda m: m.dst_start):
            for o_mapping in other.mappings:
                if (o_mapping.src.start > mapping.dst.stop
                    or o_mapping.src.stop <= mapping.dst.start):
                    continue
                overlap = (max(mapping.dst.start, o_mapping.src.start), min(mapping.dst.stop,  o_mapping.src.stop))
                combined.append(Mapping(
                    dst_start = overlap[0] + o_mapping.delta,
                    src_start = overlap[0] - mapping.delta,
                    length = overlap[1] - overlap[0]
                ))
        return Map(combined)


if __name__ == '__main__':
    import sys
    sys.exit(main())
