from utils import Vector2
from collections import namedtuple
from math import prod
import re

# Day 14

Guard = namedtuple('Guard', ['start_pos','velocity'])

def run_part_1(data):
    bounds = Vector2(101, 103)
    guards = [simulate_guard_movements(guard, bounds) for guard in data]
    split = Vector2(bounds.x//2, bounds.y//2)
    quads = [0, 0, 0, 0]
    for guard in guards:
        if guard.x < split.x and guard.y < split.y: quads[0] += 1
        if guard.x > split.x and guard.y < split.y: quads[1] += 1
        if guard.x < split.x and guard.y > split.y: quads[2] += 1
        if guard.x > split.x and guard.y > split.y: quads[3] += 1
    print(quads)
    return prod(quads)

def run_part_2(data):
    bounds = Vector2(101, 103)
    return simulate_guards_until_no_overlaps(data, bounds)

# Part 2 was a little silly with no direction really so I got a tip that when no guards overlap, they'll form the tree.
def simulate_guards_until_no_overlaps(guards: list[Guard], bounds, seconds=9999):
    guard_coords = [guard.start_pos for guard in guards]
    for second in range(seconds):
        for i, coords in enumerate(guard_coords):
            guard_coords[i] = Vector2((coords.x + guards[i].velocity.x) % bounds.x, (coords.y + guards[i].velocity.y) % bounds.y)
        if not contains_overlaps(guard_coords):
            print_grid(guard_grid(guard_coords, bounds))
            break
    return second + 1

def contains_overlaps(guards):
    seen = set()
    for guard in guards:
        if guard in seen: return True
        seen.add(guard)
    return False

def guard_grid(guard_coords: list[Vector2], bounds):
    grid = blank_grid(bounds)
    for coords in guard_coords:
        grid[coords.x][coords.y] += 1
    return grid

def blank_grid(bounds):
    return [[0 for _ in range(bounds.y)] for _ in range(bounds.x)]

def print_grid(grid):
    for row in grid:
        for col in row:
            if col == 0: print(".", end="")
            else: print(col, end="")
        print("")
    print("","")

# Part 1 movements
def simulate_guard_movements(guard: Guard, bounds, seconds=100):
    pos = guard.start_pos
    for _ in range(seconds):
        new_x = (pos.x + guard.velocity.x) % bounds.x
        new_y = (pos.y + guard.velocity.y) % bounds.y
        pos = Vector2(new_x, new_y)
    return pos

def parse_input(data):
    guards = []
    for guard in data:
        g = re.match(r"^p\=(\-?\d+),(\-?\d+)\sv\=(\-?\d+),(\-?\d+)$", guard)
        guards.append(Guard(
            Vector2(x=int(g.group(1)), y=int(g.group(2))), 
            Vector2(x=int(g.group(3)), y=int(g.group(4)))
        ))
    return guards
