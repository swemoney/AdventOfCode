from utils import Directions, Point
from collections import defaultdict

# Day 21

VALID_MOVES = [Directions.north, Directions.east, Directions.south, Directions.west]
PLOT = "."
ROCK = "#"
START = "S"

def run_part_1(data):
    plots, _ = walk(garden=data, steps=64)
    return len(plots)

def run_part_2(data): # Took about a minute to run on my machine. Still worked!
    steps = 26501365
    _, quad_points = walk(garden=data, steps=steps)
    s = (steps//len(data[0]))
    q0 = quad_points[0]
    q1 = quad_points[1] - quad_points[0]
    q2 = quad_points[2] - quad_points[1]
    num_plots = q0 + q1 * s + (s * (s - 1) // 2) * (q2 - q1)
    return num_plots

def walk(garden: list[list[str]], steps: int) -> set[Point]:
    start = start_point(garden)
    visited = defaultdict(set)
    visited[0].add(start)
    quadratic_points = []
    for step in range(steps):
        for tile in visited[step]:
            for move in VALID_MOVES:
                next_tile = Point(tile.y + move.y, tile.x + move.x)
                if not garden[next_tile.y % len(garden)][next_tile.x % len(garden[0])] == ROCK:
                    visited[step + 1].add(next_tile)
        
        # Part 2 Stuff
        if step % len(garden[0]) == steps % len(garden[0]):
            quadratic_points.append(len(visited[step]))
        if len(quadratic_points) == 3: break

    return (visited[steps], quadratic_points)

def start_point(garden: list[list[str]]) -> Point:
    for y, row in enumerate(garden):
        for x, col in enumerate(row):
            if col == START: return Point(y, x)

def parse_input(data):
    return [list(row) for row in data]
