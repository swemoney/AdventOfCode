from utils import Vector2
from collections import namedtuple
from typing import NewType
import heapq
import math

# Day 16

Tile = NewType("Tile", str)
WALL = Tile("#")
SPACE = Tile(".")
START = Tile("S")
END = Tile("E")

Direction = namedtuple("Direction", ["x", "y"])
EAST = Direction(x=1, y=0)
WEST = Direction(x=-1, y=0)
NORTH = Direction(x=0, y=-1)
SOUTH = Direction(x=0, y=1)

DIRECTIONS = {
    EAST: [EAST, SOUTH, NORTH],
    WEST: [WEST, SOUTH, NORTH],
    SOUTH: [SOUTH, WEST, EAST],
    NORTH: [NORTH, WEST, EAST]
}

Node = namedtuple("Node", ["coords", "direction"])

def run_part_1(data):
    navigatable_tiles, start_pos, end_pos = data
    dist = dijkstra(navigatable_tiles, [Node(start_pos, EAST)])
    best = math.inf
    for d in [EAST, WEST, SOUTH, NORTH]:
        end_node = Node(end_pos, d)
        if end_node in dist:
            best = min(best, dist[end_node])
    return best

def run_part_2(data):
    navigatable_tiles, start_pos, end_pos = data

    start_to_end = dijkstra(navigatable_tiles, [Node(start_pos, EAST)])
    end_to_start = dijkstra(navigatable_tiles, [Node(end_pos, d) for d in [EAST, WEST, NORTH, SOUTH]])
    optimal_path = run_part_1(data)

    flipped_directions = {EAST: WEST, WEST: EAST, NORTH: SOUTH, SOUTH: NORTH}
    result = set()

    for coords in navigatable_tiles:
        for direction in [EAST, WEST, NORTH, SOUTH]:
            state_from_start = Node(coords, direction)
            state_from_end = Node(coords, flipped_directions[direction])
            if state_from_start in start_to_end and state_from_end in end_to_start:
                if (start_to_end[state_from_start] + end_to_start[state_from_end] == optimal_path):
                    result.add(coords)
    return len(result)

def dijkstra(navigatable_tiles, nodes):
    dist = {}
    heap = []
    for node in nodes:
        dist[node] = 0
        heapq.heappush(heap, (0, node))

    while heap:
        score, node = heapq.heappop(heap)
        if dist[node] < score: continue

        for next_direction in DIRECTIONS[node.direction]:
            next_node = Node(node.coords, next_direction)
            if next_node not in dist or dist[next_node] > score + 1000:
                dist[next_node] = score + 1000
                heapq.heappush(heap, (score + 1000, next_node))

        next_coords = node.coords + node.direction
        next_node = Node(next_coords, node.direction)
        if next_coords in navigatable_tiles and (next_node not in dist or dist[next_node] > score + 1):
            dist[next_node] = score + 1
            heapq.heappush(heap, (score + 1, next_node))

    return dist

def parse_input(data) -> tuple[set[Vector2], Vector2, Vector2]: # navigatable tiles, start coords, end coords
    navigatable = set()
    for y, line in enumerate(data):
        for x, tile in enumerate(line):
            if tile in [SPACE, START, END]: navigatable.add(Vector2(x, y))
            if tile == START: start_pos = Vector2(x, y)
            if tile == END: end_pos = Vector2(x, y)
    return navigatable, start_pos, end_pos
