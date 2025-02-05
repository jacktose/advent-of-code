#!/usr/bin/env python3

"""
https://adventofcode.com/2024/day/16
Day 16: Reindeer Maze
"""

from __future__ import annotations
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, InitVar, field
from heapq import heappop, heappush
from itertools import pairwise
from typing import NamedTuple

import sys; import os; sys.path.append(os.path.abspath('../../util'))
from Grid import Direction, Grid_Immutable, Grid_Mutable, Point
from Intfinity import intfinity as inf
from Display import style


def main():
    ex_data_1 = get_input('./example1')
    ex_data_2 = get_input('./example2')
    data = get_input('./input')
    
    print('example 1.1:', part_1(ex_data_1), '= 7036?',  end='\n\n')
    print('example 1.2:', part_1(ex_data_2), '= 11048?', end='\n\n')
    print('part 1:',      part_1(data),                  end='\n\n')  # 130536
    print('example 2.1:', part_2(ex_data_1), '= 45?',    end='\n\n')
    print('example 2.2:', part_2(ex_data_2), '= 64?',    end='\n\n')
    print('part 2:',      part_2(data),                  end='\n\n')  # 1024

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = Maze(f.read())
    return data

def part_1(data: Maze) -> int:
    '''Analyze your map carefully. What is the lowest score a Reindeer could possibly get?'''
    maze = data
    maze.dijkstra()
    return maze.lowest_cost()

def part_2(data: Maze) -> int:
    '''How many tiles are part of at least one of the best paths through the maze?'''
    maze = data
    # Dijkstra's was run in part_1, same object
    paths = maze.best_paths()
    #maze.print_paths(paths)
    visited = set(node.point for path in paths for node in path)
    return len(visited)


class Node(NamedTuple):
    point: Point
    dir: Direction

@dataclass
class Maze:
    '''Represent a maze as a Grid_Immutable plus more metadata and functions for solving.'''
    grid: Grid_Immutable[str]           = field(init=False)
    grid_data: InitVar[Iterable[Iterable[str]]|str]
    step_cost: int = 1
    turn_cost: int = 1000
    start_dir: Direction = Direction.E
    start: Point                        = field(init=False, repr=False)
    _start_node: Node                   = field(init=False, repr=False)
    end: Point                          = field(init=False, repr=False)
    _end_nodes: tuple[Node, ...]        = field(init=False, repr=False)
    costs: dict[Node, int]              = field(init=False, repr=False)
    graph: dict[Node, dict[Node, int]]  = field(init=False, repr=False)
    parents: dict[Node, list[Node]]     = field(init=False, repr=False)

    _DIRECTIONS: tuple[Direction, ...] = (Direction.N, Direction.E, Direction.S, Direction.W)

    def __post_init__(self, grid_data):
        self.grid: Grid_Immutable[str] = Grid_Immutable(grid_data)
        self.start = self.grid.find('S')
        self._start_node = Node(self.start, self.start_dir)
        self.end = self.grid.find('E')
        self._end_nodes = tuple(Node(self.end, dir) for dir in self._DIRECTIONS)
        self.graph = {Node(point, dir): self._node_weights(point, dir)
                      for point, char in self.grid.iter_all() if char != '#'
                      for dir in self._DIRECTIONS}
        self.costs: dict[Node, int] = {node: inf for node in self.graph}
        self.parents = {node: [] for node in self.graph}
    
    def _node_weights(self, point: Point, dir: Direction) -> dict[Node, int]:
        '''Generate weights from a Node (Point + Direction) to neighboring Nodes.'''
        weights = {}
        if self.grid.get_point(nei := point + dir.unit_velocity) not in (None, '#'):
            weights |= {Node(nei, dir): self.step_cost}
        weights |= {Node(point, dir.left):       self.turn_cost,
                    Node(point, dir.right):      self.turn_cost,
                    Node(point, dir.opposite): 2*self.turn_cost}
        return weights
    
    def __str__(self) -> str:
        return str(self.grid)

    def dijkstra(self) -> None:
        '''Use Dijkstra's algorithm to walk the graph, finding best cost from start to each node.
        Resulting costs stored in self.costs.'''
        self.costs[self._start_node] = 0
        todo: list[tuple[int, int, Node]] = [(0, x:=0, self._start_node)]
        processed = set()
        while todo:
            _, _, node = heappop(todo)
            if node in processed:
                continue
            processed.add(node)
            cost_here = self.costs[node]
            for step, weight in self.graph[node].items():
                if (cost_there := cost_here + weight) < self.costs[step]:
                    self.costs[step] = cost_there
                    heappush(todo, (self.costs[step], x:=x+1, step))  # Dijkstra
                    #heappush(todo, (self.costs[step] + self.min_cost_to_end(step), x:=x+1, step))  # A*
                    self.parents[step] = [node]
                elif cost_there == self.costs[step]:
                    self.parents[step] += [node]

    def min_cost_to_end(self, node: Node) -> int:
        '''Minimum cost from any (point, direction) to end.
        For use in heuristic for A* algorithm.'''
        vector = self.end - node.point
        taxi_dist = vector.row + vector.col
        dirs_to_end = vector.component_row.direction | vector.component_col.direction
        if node.dir == dirs_to_end:  # Pointing at end
            turns = 0
        elif node.dir in dirs_to_end:  # Pointing in one direction needed, or perp. but aligned
            turns = 1
        else:
            turns = 2
        return (self.step_cost * taxi_dist) + (self.turn_cost * turns)

    def lowest_cost(self) -> int:
        return min(self.costs[node] for node in self._end_nodes)
    
    def best_paths(self) -> list[list[Node]]:
        '''List of all paths start->end with best total cost.
        Reverse BFS of sorts from end. Or should I just store parents in dijkstra()?'''
        best_cost = self.lowest_cost()
        incomplete_paths = [[node] for node, cost in self.costs.items()
                            if node.point == self.end and cost == best_cost]
        paths = []
        while incomplete_paths:
            path = incomplete_paths.pop()
            if (here := path[-1]) == self._start_node:
                paths.append(path[::-1])
                continue
            parents = self.parents[here]
            incomplete_paths.extend(path + [parent] for parent in parents)
        return paths

    def path_cost(self, path: Sequence[Point]|Sequence[Node]) -> int:
        '''Calculate total cost of a path.'''
        if isinstance(path[0], Point):
            return self._path_cost_points(path)  # type: ignore
        elif isinstance(path[0], Node):
            return self._path_cost_nodes(path)  # type: ignore
        else:
            raise TypeError

    def _path_cost_points(self, path: Sequence[Point]) -> int:
        cost: int = 0
        prev_dir = self.start_dir
        for a, b in pairwise(path):
            cost += 1
            dir = (b-a).direction
            if dir != prev_dir:
                cost += 1000
                prev_dir = dir
        return cost

    def _path_cost_nodes(self, path: Sequence[Node]) -> int:
        cost: int = 0
        for a, b in pairwise(path):
            match (a.point == b.point), (a.dir == b.dir):
                case False, True:
                    cost += self.step_cost
                case True, False:
                    cost += self.turn_cost
                case _:
                    raise RuntimeError
        return cost

    def print_paths(self, paths: Sequence[Sequence[Point]|Sequence[Node]],
                    correct_cost: int = 130536) -> None:
        '''Print grid with paths as "O"s.
        Paths of correct cost are green. Paths of wrong cost are red. Overlap is yellow.'''
        visited = set(step for path in paths for step in path)
        is_good = lambda path: self.path_cost(path) == correct_cost
        good_paths, bad_paths = filter_yes_no(is_good, paths)
        good_visited = set(step for path in good_paths for step in path)
        bad_visited = set(step for path in bad_paths for step in path)
        grid = Grid_Mutable(self.grid)
        grid[0][0] = style.FAINT + grid[0][0]
        for step in visited:
            char = style.RESET
            match (step in good_visited), (step in bad_visited):
                case True, False:
                    char += style.FG.GREEN
                case True, True:
                    char += style.FG.YELLOW
                case False, True:
                    char += style.FG.RED
            char += 'O' + style.RESET + style.FAINT
            point: Point = step.point if isinstance(step, Node) else point
            grid.set_point(point, char)
        print(grid.string_with_numbers() + style.RESET)

def filter_yes_no[T](predicate: Callable[[T], bool], iterable: Iterable[T]) -> tuple[list[T], list[T]]:
    '''Like filter() and itertools.filterfalse() in one iteration.
    Returns tuple of lists: Items where predicate is true, items where predicate is false.'''
    yes = []
    no = []
    for item in iterable:
        if predicate(item):
            yes.append(item)
        else:
            no.append(item)
    return yes, no


if __name__ == '__main__':
    import sys
    sys.exit(main())
