#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/16
Day 16: Reindeer Maze
"""

from __future__ import annotations
#from collections import deque
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass, InitVar
from heapq import heappop, heappush
from itertools import pairwise
from math import inf
from time import time

import sys 
import os
from typing import NamedTuple

from pyrsistent import inc
sys.path.append(os.path.abspath('../../util'))
from Grid import Direction, Grid_Immutable, Grid_Mutable, Grid_Sparse, Point


def main():
    ex_data_1 = get_input('./example1')
    ex_data_2 = get_input('./example2')
    data = get_input('./input')
    
    print('example 1.1:', part_1(ex_data_1), '= 7036?')
    print('\nexample 1.2:', part_1(ex_data_2), '= 11048?')
    print('\npart 1:', part_1(data))  # 130536
    print('\nexample 2.1:', part_2(ex_data_1), '= 45?')
    print('\nexample 2.2:', part_2(ex_data_2), '= 64?')
    print('\npart 2:', part_2(data))

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = Maze(f.read())
    return data

def part_1(data):
    '''Analyze your map carefully. What is the lowest score a Reindeer could possibly get?'''
    #maze = Maze(data)
    maze = data
    #sys.setrecursionlimit(max(sys.getrecursionlimit(), len(maze.costs)))
    #maze.calc_costs_recursive(start=maze.start, start_dir=maze.start_dir)
    #print(maze.ccr_calls)
    #return maze.lowest_cost()
    #maze.calc_costs_iter()
    maze.dijkstra()
    return maze.lowest_cost()
    # 130536

def part_2(data):
    '''How many tiles are part of at least one of the best paths through the maze?'''
    maze = data
    #maze.calc_best_paths()
    #print(maze.str_best_paths())
    #return len(maze.best_paths)
    paths = maze.best_paths()
    good_paths, bad_paths = filter_yes_no(lambda p: maze.path_cost(p) == 130536, paths)
    visited = set(point for path in paths for point in path)
    good_visited = set(point for path in good_paths for point in path)
    bad_visited = set(point for path in bad_paths for point in path)
    grid = Grid_Mutable(maze.grid)
    grid[0][0] = style.FAINT + grid[0][0]
    for point in visited:
        match (point in good_visited), (point in bad_visited):
            case True, False:
                s = style.RESET + style.FG.GREEN
            case True, True:
                s = style.RESET + style.FG.YELLOW
            case False, True:
                s = style.RESET + style.FG.RED
        grid[point.row][point.col] = s + 'O' + style.RESET + style.FAINT
    #for point in good_visited:
    #    grid[point.row][point.col] = style.FG.GREEN + 'O' + style.RESET + style.FAINT
    #for point in bad_visited:
    #    grid[point.row][point.col] = (style.FG.YELLOW if point in good_visited else style.FG.RED) + 'X' + style.RESET + style.FAINT
    print(grid.string_with_numbers())
    print(style.RESET)
    #print(*(maze.path_cost(path) for path in paths))
    return len(visited)
    # 1069 too high

def filter_yes_no[T](predicate: Callable[[T], bool], iterable: Iterable[T]) -> tuple[list[T], list[T]]:
    yes = []
    no = []
    for item in iterable:
        if predicate(item):
            yes.append(item)
        else:
            no.append(item)
    return yes, no

class _fg(NamedTuple):
    BLACK =   '\x1b[30m'
    RED =     '\x1b[31m'
    GREEN =   '\x1b[32m'
    YELLOW =  '\x1b[33m'
    BLUE =    '\x1b[34m'
    MAGENTA = '\x1b[35m'
    CYAN =    '\x1b[36m'
    WHITE =   '\x1b[37m'

class _bg(NamedTuple):
    BLACK =   '\x1b[40m'
    RED =     '\x1b[41m'
    GREEN =   '\x1b[42m'
    YELLOW =  '\x1b[43m'
    BLUE =    '\x1b[44m'
    MAGENTA = '\x1b[45m'
    CYAN =    '\x1b[46m'
    WHITE =   '\x1b[47m'

class style(NamedTuple):
    RESET =         '\x1b[0m'
    BOLD =          '\x1b[1m'
    FAINT =         '\x1b[2m'
    ITALIC =        '\x1b[3m'
    UNDERLINED =    '\x1b[4m'
    INVERSE =       '\x1b[7m'
    STRIKETHROUGH = '\x1b[9m'
    FG = _fg
    BG = _bg

class control(NamedTuple):
    SHOW_CURSOR = '\x1b[?25h'
    HIDE_CURSOR = '\x1b[?25l'
    ERASE_CURSOR_TO_END = '\x1b[0J'
    ERASE_CURSOR_TO_START = '\x1b[1J'
    ERASE_SCREEN = '\x1b[2J'


@dataclass
class Maze:
    grid_data: InitVar[Iterable[Iterable[str]]|str]
    start_dir: Direction = Direction.E
    step_cost: int = 1
    turn_cost: int = 1000

    def __post_init__(self, grid_data):
        self.grid: Grid_Immutable[str] = Grid_Immutable(grid_data)
        self.start = self.grid.find('S')
        self.end = self.grid.find('E')
        DIRECTIONS = (Direction.N, Direction.E, Direction.S, Direction.W)
        self.costs = {point: {dir: inf for dir in DIRECTIONS}
                      for point, char in self.grid.iter_all() if char != '#'}
        self.costs[self.start][self.start_dir] = 0
        self.parents = {point: {dir: [] for dir in DIRECTIONS}
                        for point, char in self.grid.iter_all() if char != '#'}

    def dijkstra(self):
        todo = [(0, self.start, x:=0, self.start_dir)]
        processed = set()
        #best: int = 0
        tasks = 0
        start_time = time()
        while todo:
            _, here, _, cur_dir = heappop(todo)
            if (here, cur_dir) in processed:
                continue
            processed.add((here, cur_dir))
            tasks += 1
            steps = ((cur_dir,       self.costs[here][cur_dir] + self.step_cost),
                     (cur_dir.left,  self.costs[here][cur_dir] + self.step_cost + self.turn_cost),
                     (cur_dir.right, self.costs[here][cur_dir] + self.step_cost + self.turn_cost))
            neighbors = ((neigh, dir, cost) for dir, cost in steps
                         if (neigh := here + dir.unit_velocity) in self.costs)
            for neigh, dir, cost in neighbors:
                if cost < self.costs[neigh][dir]:
                    self.costs[neigh][dir] = cost
                    self.parents[neigh][dir] = [(here, cur_dir)]
                    sort_heuristic = cost  # Dijkstra
                    #sort_heuristic = cost + self.min_cost_to_end(neigh, dir)  # A*
                    heappush(todo, (sort_heuristic, neigh, x:=x+1, dir))
                elif cost == self.costs[neigh][dir]:
                    self.parents[neigh][dir].append((here, cur_dir))
        end_time = time()
        #print('tasks: ', tasks)
        #print('time: ', end_time - start_time)
    
    def min_cost_to_end(self, point: Point, dir: Direction) -> int:
        vector = self.end - point
        taxi_dist = vector.row + vector.col
        dirs_to_end = vector.component_row.direction | vector.component_col.direction
        if dir == dirs_to_end:  # Pointing at end
            turns = 0
        elif dir in dirs_to_end:  # Pointing in one direction needed, or perp. but aligned
            turns = 1
        else:
            turns = 2
        return (self.step_cost * taxi_dist) + (self.turn_cost * turns)

    def lowest_cost(self):
        return min(self.costs[self.end].values())
    
    def best_paths(self) -> list[list[Point]]:
        '''Reverse from end. Or just store parents?'''
        best_cost = min(self.costs[self.end].values())
        incomplete_paths = [[(self.end, dir)] for dir, cost in self.costs[self.end].items() if cost == best_cost]
        paths = []
        while incomplete_paths:
            path = incomplete_paths.pop()
            here, dir = path[-1]
            if here == self.start:
                paths.append([point for point, _ in reversed(path)])
                continue
            parents = self.parents[here][dir]
            incomplete_paths.extend(path + [parent] for parent in parents)
        return paths

    def path_cost(self, path: list[Point]) -> int:
        cost: int = 0
        prev_dir = self.start_dir
        for a, b in pairwise(path):
            cost += 1
            dir = (b-a).direction
            if dir != prev_dir:
                cost += 1000
                prev_dir = dir
        return cost




@dataclass
class Maze2:
    grid_data: InitVar[Iterable[Iterable[str]]|str]
    start_dir: Direction = Direction.E
    step_cost: int = 1
    turn_cost: int = 1000

    def __post_init__(self, grid_data):
        self.grid: Grid_Immutable[str] = Grid_Immutable(grid_data)
        self.start = self.grid.find('S')
        self.end = self.grid.find('E')
        DIR_COSTS_DEFAULT = {Direction.N: inf, Direction.E: inf,
                             Direction.S: inf, Direction.W: inf}
        self.costs: Grid_Sparse[dict[Direction, int]] = Grid_Sparse({point: DIR_COSTS_DEFAULT.copy()
                                                     for point, value in self.grid.iter_all()
                                                     if value in ('.', 'S', 'E')})
        self.costs[self.start][self.start_dir] = 0
        #self.paths: Grid_Sparse[list[tuple[Point, ...]]]
        self.ccr_calls: int = 0
    
    def lowest_cost(self) -> int:
        self.calc_costs_recursive(start=self.start, start_dir=self.start_dir)
        return min(self.costs[self.end].values())

    def calc_costs_iter(self) -> None:
        cci_iterations: int = 0
        todo = [{'point': self.start}]  # include path? replace with path?
        while todo:
            cci_iterations += 1
            #task = todo.pop()
            task = heappop(todo)
            current_costs = self.costs[task['point']]
            best_cost = min(current_costs.values())
            for cheap_direction in (d for d, c in current_costs.items() if c == best_cost):
                for direction in cheap_direction.perpendiculars:
                    step = task['point'] + direction.unit_velocity
                    if self.grid[step.row][step.col] == '#': continue
                    if best_cost + self.turn_cost < current_costs[direction]:
                        current_costs[direction] = best_cost + self.turn_cost
                        #todo.append({'point': step})
                        heappush(todo, {'point': step})
        print(f'{cci_iterations=}')

    def calc_costs_recursive(self, start: Point = None, start_dir: Direction = None) -> None:
        ''''''
        self.ccr_calls += 1
        # Handle defaults:
        if start is None:
            start = self.start
        if start_dir is None:
            if start == self.start:
                start_dir = self.start_dir
            else:
                raise ValueError('Must specify start_dir (except at maze start)')
        
        if start == self.end:
            return

        for direction in (start_dir, start_dir.left, start_dir.right):
            step = start + direction.unit_velocity
            if self.grid[step.row][step.col] == '#':
                continue
            cost = self.costs[start][start_dir] + self.step_cost + (self.turn_cost * (direction != start_dir))
            if cost < self.costs[step][direction]:
                self.costs[step][direction] = cost
                self.calc_costs_recursive(step, direction)
        
    def best_paths(self, to: Point = None, exit_dir: Direction = Direction.ALL) -> list[tuple[Point, ...]]:
        if to is None:
            to = self.end
        if to == self.start:
            return [(to,)]
        
        paths = []
        best_cost_to_get_here = min(self.costs[to].values())
        for direction in self.costs[to].keys():
            prev_step = to - direction.unit_velocity
            if prev_step not in self.costs.keys():
                continue
            if self.costs[to][direction] - (self.turn_cost * (direction == exit_dir)) <= best_cost_to_get_here:
                paths.extend([path + (to,) for path in self.best_paths(prev_step, direction)])
        if paths:
            return paths
        else:
            raise RuntimeError(f'Could not backtrack best path. Stuck at {to}')



visited = []

class Maze1(Grid_Immutable[str]):
    ''''''
    def __init__(self, *args,
                 start_dir: Direction = Direction.E,
                 step_cost: int = 1, turn_cost: int = 1000,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.start_dir = start_dir
        self.step_cost = step_cost
        self.turn_cost = turn_cost
        self.start = self.find('S')
        self.end = self.find('E')
        DIR_COSTS_DEFAULT = {Direction.N: inf, Direction.E: inf,
                             Direction.S: inf, Direction.W: inf}
        self.costs: Grid_Sparse[dict[Direction, int]] = Grid_Sparse({point: DIR_COSTS_DEFAULT.copy()
                                                     for point, value in self.iter_all()
                                                     if value in ('.', 'S', 'E')})
        self.costs[self.start][self.start_dir] = 0
        self.best_paths: set = set()
    
    def calc_costs(self, start: Point = None, start_dir: Direction = None, start_cost: int = 0) -> None:
        if start is None:
            start = self.start
        if start_dir is None:
            if start == self.start:
                start_dir = self.start_dir
            else:
                raise ValueError('Must specify start_dir (except at maze start)')
        
        #if start in visited: print('already visited', start)
        visited.append(start)
        
        costs = self.costs[start]
        costs[start_dir] = min(costs[start_dir], start_cost)
        if start == self.end:
            return
            #return min(self.costs[self.end])
        for direction in start_dir.perpendiculars:
            costs[direction] = min(costs[direction], start_cost + self.turn_cost)
        #costs[direction.left] = min(costs[direction.left], start_cost + self.turn_cost)
        #costs[direction.right] = min(costs[direction.right], start_cost + self.turn_cost)
        #costs[direction.opposite] = min(costs[direction.opposite], start_cost + 2*self.turn_cost)
        for direction in (start_dir,) + start_dir.perpendiculars:
            step = start + direction.unit_velocity
            if self[step.r][step.c] == '#':
                continue
            if costs[direction] + self.step_cost < self.costs[step][direction]:
                self.calc_costs(step, direction, costs[direction] + self.step_cost)
    
    def calc_best_paths(self, start: Point = None, direction: Direction = None) -> None:
        if start is None:
            start = self.end

        self.best_paths.add(start)

        if start == self.start:
            return

        if start == self.end:
            best_cost = min(self.costs[start].values())
            for direction, cost in self.costs[start].items():
                if cost == best_cost:
                    step = start - direction.unit_velocity
                    self.calc_best_paths(step, direction)
            return
        
        for prev_step, prev_dir, addl_cost in (
            (ps := start - direction.unit_velocity,       pd := direction,       self.step_cost),
            (ps := start - direction.left.unit_velocity,  pd := direction.left,  self.step_cost + self.turn_cost),
            (ps := start - direction.right.unit_velocity, pd := direction.right, self.step_cost + self.turn_cost),
        ):
            if ps not in self.costs:
                continue
            cost_to_here = self.costs[ps][pd] + addl_cost
            if cost_to_here == self.costs[start][direction]:
                self.calc_best_paths(prev_step, prev_dir)


    def str_best_paths(self) -> str:
        return '\n'.join(
            ''.join(
                'O' if tile == '.' and Point(r, c) in self.best_paths else tile
                for c, tile in enumerate(row)
            ) for r, row in enumerate(self)
        )
        #out = []
        #for r, row in enumerate(self):
        #    for c, tile in enumerate(row):
        #        if tile == '.' and Point(r, c) in self.best_paths:
        #            out.append('O')
        #        else:
        #            out.append(tile)
        #    out.append('\n')
        #return ''.join(out)

        
        

        



if __name__ == '__main__':
    import sys
    sys.exit(main())
