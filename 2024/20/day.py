from utils import array2d_to_dict, Vector2, Directions
from collections import defaultdict
from functools import cache
from typing import NewType
import math

# Day 20

Tile = NewType("Tile", str)
Grid = NewType("Grid", dict[Vector2, Tile])

START = "S"
END = "E"
SPACE = "."
WALL = "#"

DIRECTIONS = [Directions.east.coords, Directions.south.coords, Directions.west.coords, Directions.north.coords]

def run_part_1(data):
    SAVE_PICOSECONDS = 100
    edges, start, end, cheats = create_graph(data)
    distance_from_start = dijkstra(edges, start)
    distance_from_end = dijkstra(edges, end)

    target_distance = distance_from_start[end] - SAVE_PICOSECONDS
    
    cheat_counts = defaultdict(int)
    total = 0

    for cheat_start, cheat_ends in cheats.items():
        for cheat_end in cheat_ends:
            dist = distance_from_start[cheat_start] + 2 + distance_from_end[cheat_end]
            if dist <= target_distance:
                cheat_counts[distance_from_start[end] - dist] += 1
                total += 1

    return total

# Not very fast but works. About 12 seconds on my machine. Good enough for me.
def run_part_2(data):
    SAVE_PICOSECONDS = 100
    edges, start, end, cheats = create_graph(data, taxi_cheats=20)
    distance_from_start = dijkstra(edges, start)
    distance_from_end = dijkstra(edges, end)
    
    target_distance = distance_from_start[end] - SAVE_PICOSECONDS

    cheat_counts = defaultdict(int)
    total = 0

    for cheat_start, cheat_ends in cheats.items():
        for cheat_end, radius in cheat_ends:
            dist = distance_from_start[cheat_start] + radius + distance_from_end[cheat_end]
            if dist <= target_distance:
                cheat_counts[distance_from_start[end] - dist] += 1
                total += 1

    return total

def create_graph(grid: Grid, taxi_cheats: int = 0) -> tuple[dict[Vector2, set[Vector2]], Vector2, Vector2, dict[Vector2, set[Vector2]]]:
    start = get_tile_coords(grid, START)
    end = get_tile_coords(grid, END)

    edges = defaultdict(set)
    cheats = defaultdict(set)
    seen = {start, }
    todo = {start, }

    while len(todo) > 0:
        current_node = todo.pop()
        for direction in DIRECTIONS:
            neighbor = current_node + direction

            if neighbor not in grid.keys():
                continue

            if grid[neighbor] != WALL:
                edges[current_node].add(neighbor)
                if neighbor not in seen:
                    todo.add(neighbor)
                    seen.add(neighbor)
                continue

            if taxi_cheats == 0:
                if (next_neighbor := neighbor + direction) in grid.keys() and grid[next_neighbor] != WALL:
                    cheats[current_node].add(next_neighbor)

            else:

                for radius in range(2, taxi_cheats + 1):
                    for cheat in filter(lambda coords: coords in grid.keys() and grid[coords] != WALL, taxicab_circle(current_node, radius)):
                        cheats[current_node].add((cheat, radius))

    return edges, start, end, cheats

def dijkstra(edges: set[Vector2], start: Vector2) -> dict[Vector2, int]:
    visited = {start, }
    distance = defaultdict(lambda: math.inf, {start: 0})

    while len(visited) > 0:
        current_node = min(visited, key=lambda coords: distance[coords])
        visited.remove(current_node)

        for neighbor in edges[current_node]:
            neighbor_score = distance[current_node] + 1
            if neighbor_score < distance[neighbor]:
                distance[neighbor] = neighbor_score
                visited.add(neighbor)

    return distance

@cache
def taxicab_circle(coords, r):
    for offset in range(r):
        inv_offset = r - offset
        yield Vector2(coords.x + offset, coords.y + inv_offset)
        yield Vector2(coords.x + inv_offset, coords.y - offset)
        yield Vector2(coords.x - offset, coords.y - inv_offset)
        yield Vector2(coords.x - inv_offset, coords.y + offset)

def get_tile_coords(grid: Grid, tile: Tile) -> Vector2:
    return next(k for k, v in grid.items() if v == tile)

def parse_input(data) -> Grid:
    return Grid(array2d_to_dict(data, vector2=True, convert_with=Tile))
