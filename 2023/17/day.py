from utils import DIRECTIONS, Point
from heapq import heappop, heappush
from typing import Self

# Day 17

VALID_DIRECTIONS = [
    DIRECTIONS["N"], 
    DIRECTIONS["E"], 
    DIRECTIONS["S"], 
    DIRECTIONS["W"]]
OPPOSITE_DIRECTIONS = {
    DIRECTIONS["N"]: DIRECTIONS["S"], 
    DIRECTIONS["E"]: DIRECTIONS["W"], 
    DIRECTIONS["S"]: DIRECTIONS["N"], 
    DIRECTIONS["W"]: DIRECTIONS["E"]}

def run_part_1(data):
    graph = Graph(grid=data, start_node=Point(0, 0))
    end_coords = Point(len(data) - 1, len(data[0]) - 1)
    return graph.get_best_path(end_coords, min_steps=0, max_steps=3)

def run_part_2(data):
    graph = Graph(grid=data, start_node=Point(0, 0))
    end_coords = Point(len(data) - 1, len(data[0]) - 1)
    return graph.get_best_path(end_coords, min_steps=4, max_steps=10)

def parse_input(data):
    return [[int(char) for char in list(row)] for row in data]

class Node:
    def __init__(self, coords: Point, cost: int, direction: Point, steps: int):
        self.cost = cost
        self.coords = coords
        self.steps = steps
        self.direction = direction

    def __lt__(self, other: Self):
        return self.cost < other.cost
    
    def __hash__(self):
        return hash(self.to_hash())
    
    def __eq__(self, other: Self):
        return self.to_hash() == other.to_hash()
    
    def to_hash(self) -> (Point, Point, int):
        return (self.coords, self.direction, self.steps)
    
    def get_neighbors(self, max_y: int, max_x: int, min_steps: int, max_steps: int) -> list[Self]:
        neighbors = []
        for direction in VALID_DIRECTIONS:
            if direction == OPPOSITE_DIRECTIONS[self.direction]: continue
            if direction == self.direction and self.steps >= max_steps: continue
            if not direction == self.direction and self.steps < min_steps: continue
            
            neighbor_coords = Point(self.coords.y + direction.y, self.coords.x + direction.x)
            if not in_bounds(neighbor_coords, max_y, max_x): continue

            steps = self.steps + 1 if direction == self.direction else 1
            neighbors.append( Node(neighbor_coords, 0, direction, steps) )
        return neighbors
    
class Graph:
    def __init__(self, grid: [[int]], start_node: Point):
        self.grid = grid
        self.max_y = len(grid) - 1
        self.max_x = len(grid[0]) - 1
        self.start_node = start_node

        self.queue = []
        for direction in VALID_DIRECTIONS:
            neighbor = Point(start_node.y + direction.y, start_node.x + direction.x)
            if not in_bounds(neighbor, self.max_y, self.max_x): continue
            self.queue.append(Node(neighbor, grid[neighbor.y][neighbor.x], direction, 1))

    def get_best_path(self, end_coords: Point, min_steps: int, max_steps: int):
        visited = set()
        while self.queue:
            node: Node = heappop(self.queue)

            if node.coords == end_coords: 
                if node.steps < min_steps: continue
                return node.cost
            
            if node in visited: continue
            visited.add(node)

            for neighbor in node.get_neighbors(self.max_y, self.max_x, min_steps, max_steps):
                neighbor.cost = node.cost + self.grid[neighbor.coords.y][neighbor.coords.x]
                heappush(self.queue, neighbor)

        return -1

def in_bounds(coords: Point, max_y: int, max_x: int) -> bool:
    return coords.y >= 0 and coords.x >= 0 and coords.y <= max_y and coords.x <= max_x
