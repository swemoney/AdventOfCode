from typing import NamedTuple
from collections import defaultdict
from itertools import product

# Day 22

class Vector3(NamedTuple):
    x: int
    y: int
    z: int

class Brick(NamedTuple):
    end1: Vector3
    end2: Vector3

def run_part_1(data):
    num_bricks, supports, supported = calculate_brick_supports(data)
    return sum([not any(len(supported[j]) == 1 for j in supports[i]) for i in range(num_bricks)])

def run_part_2(data):
    num_bricks, supports, supported = calculate_brick_supports(data)

    total = 0
    for i in range(num_bricks):
        falling_bricks = set([i])
        for j in range(i + 1, num_bricks):
            if supported[j].issubset(falling_bricks):
                falling_bricks.add(j)
        total += len(falling_bricks) - 1
    return total

def calculate_brick_supports(bricks: list[Brick]) -> (int, dict[int, set[int]], dict[int, set[int]]):
    supported = defaultdict(set)
    supports = defaultdict(set)
    heights = defaultdict(lambda: (0, -1))

    for i, brick in enumerate(bricks):
        max_height = 0
        brick_supported = set()

        for x, y in product(range(brick.end1.x, brick.end2.x + 1), range(brick.end1.y, brick.end2.y + 1)):
            height, j = heights[(x, y)]
            if height > max_height:
                max_height = height
                brick_supported = set([j])
            elif height == max_height:
                brick_supported.add(j)
        supported[i] = brick_supported

        for j in brick_supported:
            supports[j].add(i)

        z = max_height + brick.end2.z - brick.end1.z + 1
        for x, y in product(range(brick.end1.x, brick.end2.x + 1), range(brick.end1.y, brick.end2.y + 1)):
            heights[(x, y)] = (z, i)

    return (len(bricks), supports, supported)

def parse_input(data):
    bricks = [Brick(Vector3(*[int(coords) for coords in line.split("~")[0].split(",")]),
                    Vector3(*[int(coords) for coords in line.split("~")[1].split(",")])) for line in data]
    bricks = sorted(bricks, key=lambda brick: brick.end1.z)
    return bricks
