#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/16
Day 16: Reindeer Maze
"""

from __future__ import annotations
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, InitVar, field
from heapq import heappop, heappush
from itertools import pairwise
#from math import inf
from time import time
from typing import NamedTuple

import sys 
import os
sys.path.append(os.path.abspath('../../util'))
from Grid import Direction, Grid_Immutable, Grid_Mutable, Point
from Intfinity import intfinity as inf


def main():
    ex_data_0 = get_input('./example0')
    ex_data_1 = get_input('./example1')
    ex_data_2 = get_input('./example2')
    data = get_input('./input')
    
    print('example 0:', part_1(ex_data_0), '= _?\n')
    print('example 1.1:', part_1(ex_data_1), '= 7036?')
    print('\nexample 1.2:', part_1(ex_data_2), '= 11048?')
    print('\npart 1:', part_1(data))  # 130536
    print('\nexample 2.1:', part_2(ex_data_1), '= 45?')
    print('\nexample 2.2:', part_2(ex_data_2), '= 64?')
    print('\npart 2:', part_2(data))  # 1024

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = Maze(f.read())
    return data

def part_1(data):
    '''Analyze your map carefully. What is the lowest score a Reindeer could possibly get?'''
    maze = data
    maze.dijkstra()
    maze.true_dijkstra()
    return maze.lowest_cost()

def part_2(data):
    '''How many tiles are part of at least one of the best paths through the maze?'''
    maze = data
    # Dijkstra's was run in part_1, same object
    paths = maze.best_paths()
    visited = set(point for path in paths for point in path)
    return len(visited)


#type Node = tuple[Point, Direction]  
class Node(NamedTuple):
    point: Point
    dir: Direction

@dataclass
class Maze:
    grid_data: InitVar[Iterable[Iterable[str]]|str]
    start_dir: Direction = Direction.E
    step_cost: int = 1
    turn_cost: int = 1000
    grid: Grid_Immutable[str] = field(init=False)
    start: Point = field(init=False)
    end: Point = field(init=False)
    costs: dict[Point, dict[Direction, int]] = field(init=False)
    graph: dict[Node, dict[Node, int]] = field(init=False)
    parents: dict[Point, dict[Direction, list[tuple[Point, Direction]]]] = field(init=False)
    gparents: dict[Node, list[Node]] = field(init=False)

    def __post_init__(self, grid_data):
        self.grid: Grid_Immutable[str] = Grid_Immutable(grid_data)
        self.start = self.grid.find('S')
        self.end = self.grid.find('E')
        DIRECTIONS = (Direction.N, Direction.E, Direction.S, Direction.W)
        self.costs = {point: {dir: inf for dir in DIRECTIONS}
                      for point, char in self.grid.iter_all() if char != '#'}
        self.costs[self.start][self.start_dir] = 0
        self.graph = {Node(point, dir): self._node_weights(point, dir)
                      for point, char in self.grid.iter_all() if char != '#'
                      for dir in DIRECTIONS}
        self.parents = {point: {dir: [] for dir in DIRECTIONS}
                        for point, char in self.grid.iter_all() if char != '#'}
        #TODO: rewrite best_paths() for pure graph style:
        self.gparents = {node: [] for node in self.graph}
    
    def _node_weights(self, point: Point, dir: Direction) -> dict[Node, int]:
        weights = {}
        if self.grid.get_point(nei := point + dir.unit_velocity) not in (None, '#'):
            weights |= {Node(nei, dir): self.step_cost}
        weights |= {Node(point, dir.left):       self.turn_cost,
                    Node(point, dir.right):      self.turn_cost,
                    Node(point, dir.opposite): 2*self.turn_cost}
        return weights

    def true_dijkstra(self):
        '''Use Dijkstra's algorithm to walk the graph, finding best cost from start to each node.
        Implemented for a graph of Node(Point, Direction), much cleaner.'''
        start: Node = Node(self.start, self.start_dir)
        costs: dict[Node, int] = {node: inf for node in self.graph}
        costs[start] = 0
        todo: list[tuple[int, int, Node]] = [(0, x:=0, start)]
        processed = set()
        tasks: int = 0
        start_time = time()
        while todo:
            _, _, node = heappop(todo)
            if node in processed:
                continue
            processed.add(node)
            tasks += 1
            cost_here = costs[node]
            for step, weight in self.graph[node].items():
                if (cost_there := cost_here + weight) < costs[step]:
                    costs[step] = cost_there
                    heappush(todo, (costs[step], x:=x+1, step))
                    self.gparents[step] = [node]
                elif cost_there == costs[step]:
                    self.gparents[step] += [node]
        end_time = time() - start_time
        #print(self._end_costs(costs))
        print(f'{tasks=}\t{end_time=}')

    #def _end_costs(self, costs) -> dict[Direction, int]:
    #    return {dir: costs[Node(self.end, dir)]
    #            for dir in (Direction.N, Direction.E, Direction.S, Direction.W)}

    def dijkstra(self):
        '''Use Dijkstra's algorithm to walk the graph, finding best cost from start to each node.'''
        todo = [(0, self.start, x:=0, self.start_dir)]
        processed = set()
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
                    sort_heuristic: int = cost  # Dijkstra
                    #sort_heuristic: int = cost + self.min_cost_to_end(neigh, dir)  # A*
                    heappush(todo, (sort_heuristic, neigh, x:=x+1, dir))
                elif cost == self.costs[neigh][dir]:
                    self.parents[neigh][dir].append((here, cur_dir))
        end_time = time()
        print('tasks: ', tasks)
        print('time: ', end_time - start_time)
    
    def min_cost_to_end(self, point: Point, dir: Direction) -> int:
        '''Minimum cost from any (point, direction) to end.
        For use in heuristic for A* algorithm.'''
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
        '''List of all paths start->end with best total cost.
        Reverse BFS of sorts from end. Or should I just store parents in dijkstra()?'''
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

    def print_paths(self, paths: Sequence[Sequence[Point]], correct_cost: int = 130536) -> None:
        visited = set(point for path in paths for point in path)
        good_paths, bad_paths = filter_yes_no(lambda p: self.path_cost(p) == correct_cost, paths)
        good_visited = set(point for path in good_paths for point in path)
        bad_visited = set(point for path in bad_paths for point in path)
        grid = Grid_Mutable(self.grid)
        grid[0][0] = style.FAINT + grid[0][0]
        for point in visited:
            char = style.RESET
            match (point in good_visited), (point in bad_visited):
                case True, False:
                    char += style.FG.GREEN
                case True, True:
                    char += style.FG.YELLOW
                case False, True:
                    char += style.FG.RED
            char += 'O' + style.RESET + style.FAINT
            grid[point.row][point.col] = char
        print(grid.string_with_numbers())
        print(style.RESET)

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


if __name__ == '__main__':
    import sys
    sys.exit(main())
