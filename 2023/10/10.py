#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/10
Day 10: Pipe Maze
"""

def main():
    ex_data_1_1 = get_input('./example1.1.txt')
    ex_data_1_2 = get_input('./example1.2.txt')
    ex_data_2_1 = get_input('./example2.1.txt')
    ex_data_2_2 = get_input('./example2.2.txt')
    ex_data_2_3 = get_input('./example2.3.txt')
    ex_data_2_4 = get_input('./example2.4.txt')
    data = get_input('./input.txt')
    
    print('example 1.1:')
    print(part_1(ex_data_1_1), '= 4?')
    print('example 1.2:')
    print(part_1(ex_data_1_2), '= 8?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2.1:')
    print(part_2(ex_data_2_1), '= 4?')
    print('example 2.2:')
    print(part_2(ex_data_2_2), '= 4?')
    print('example 2.3:')
    print(part_2(ex_data_2_3), '= 8?')
    print('example 2.4:')
    print(part_2(ex_data_2_4), '= 10?')
    
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input.txt') -> tuple[tuple[str, ...], ...]:
    with open(file, 'r') as f:
        data = tuple(tuple(line) for line in f.read().splitlines())
    return data

def part_1(data: tuple[tuple[str, ...], ...]) -> int:
    '''Find the single giant loop starting at S.
    How many steps along the loop does it take to get
    from the starting position to the point farthest from the starting position?'''
    #print('\n'.join([''.join(row) for row in data]))
    return len(trace_path(data)) // 2

def part_2(data: tuple[tuple[str, ...], ...]) -> int:
    '''How many tiles are enclosed by the loop?'''
    #print('\n'.join([''.join(row) for row in data]))
    path = trace_path(data)
    inside = False
    last_corner = None
    area = []
    for r, row in enumerate(data):
        for c, pipe in enumerate(row):
            if (r, c) not in path:
                if inside:
                    area.append((r, c))
                continue
            if pipe == 'S':
                pipe = infer_start_pipe(path)
            match last_corner, pipe:
                case None, '|': inside = not inside
                case _,    '-': pass
                case None, 'L': last_corner = pipe
                case None, 'F': last_corner = pipe
                case 'L',  'J': last_corner = None
                case 'F',  'J': last_corner = None; inside = not inside
                case 'L',  '7': last_corner = None; inside = not inside
                case 'F',  '7': last_corner = None
                case unmatched: raise RuntimeError(f'No match for {unmatched}')
    return len(area)

def trace_path(data) -> list[tuple[int, int]]:
    r, c = find_start(data)
    pipe = None
    path = []

    # Find & make first move
    if   r > 0              and data[r-1][c] in '7|F':
        move = 'n'
    elif r < len(data)-1    and data[r+1][c] in 'J|L':
        move = 's'
    elif c > 0              and data[r][c-1] in 'L-F':
        move = 'w'
    elif c < len(data[0])-1 and data[r][c+1] in 'J-7':
        move = 'e'
    else:
        raise ValueError("Cannot find 'S'")

    while pipe != 'S':
        path.append((r, c))
        
        # find next move:
        match move, pipe:
            case '|' | '-': pass
            case 'n', '7': move = 'w'
            case 'n', 'F': move = 'e'
            case 's', 'J': move = 'w'
            case 's', 'L': move = 'e'
            case 'w', 'L': move = 'n'
            case 'w', 'F': move = 's'
            case 'e', 'J': move = 'n'
            case 'e', '7': move = 's'

        # make move:
        match move:
            case 'n': r -= 1
            case 's': r += 1
            case 'w': c -= 1
            case 'e': c += 1
        pipe = data[r][c]

    return path

def find_start(grid: tuple[tuple[str, ...], ...]) -> tuple[int, int]:
    for r, row in enumerate(grid):
        for c, pipe in enumerate(row):
            if pipe == 'S':
                return r, c
    raise RuntimeError("'S' not found in grid")

def infer_start_pipe(path: list[tuple[int, int]]) -> str:
    start = path[0]
    neighbs = (path[-1], path[1])
    dirs = (direction(start, n) for n in neighbs)
    match tuple(sorted(dirs)):
        case 'e', 'w': return '-'
        case 'n', 's': return '|'
        case 'n', 'w': return 'J'
        case 'e', 'n': return 'L'
        case 's', 'w': return '7'
        case 'e', 's': return 'F'
        case unmatched: raise ValueError(f'No pipe for {unmatched}')

def direction(p1: tuple[int, int], p2: tuple[int, int]) -> str:
    match p2[0] - p1[0], p2[1] - p1[1]:
        case -1,  0: return 'n'
        case  1,  0: return 's'
        case  0, -1: return 'w'
        case  0,  1: return 'e'
        case unmatched: raise ValueError(f'No direction for {unmatched}')


if __name__ == '__main__':
    import sys
    sys.exit(main())

