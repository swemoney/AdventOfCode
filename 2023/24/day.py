from utils import Vector3
from dataclasses import dataclass
from itertools import combinations
from typing import Self
import z3

MIN = 200_000_000_000_000
MAX = 400_000_000_000_000

# Day 24

@dataclass(frozen=True)
class Hailstone:
    pos: Vector3
    vel: Vector3

    def path_intersects_2D(self, other: Self) -> bool:
        p, v, op, ov = self.pos, self.vel, other.pos, other.vel # shorthands

        if v.x * ov.y - ov.x * v.y == 0: return False

        x = -(v.x * ov.x * (p.y - op.y) + v.x * ov.y * op.x - ov.x * v.y * p.x) / (ov.x * v.y - v.x * ov.y)
        y = -(v.y * ov.y * (p.x - op.x) + v.y * ov.x * op.y - ov.y * v.x * p.y) / (ov.y * v.x - v.y * ov.x)

        if not (MIN <= x <= MAX) or not (MIN <= y <= MAX): return False

        if ((v.x != 0 and (x - p.x) / v.x < 0) or (ov.x != 0 and (x - op.x) / ov.x < 0)) or \
           ((v.y != 0 and (y - p.y) / v.y < 0) or (ov.y != 0 and (y - op.y) / ov.y < 0)): return False
        
        return True

def run_part_1(data):
    path_collisions = []
    for stone, other in combinations(data, 2):
        path_collisions.append(stone.path_intersects_2D(other))
    return sum(path_collisions)

def run_part_2(data):
    rock_pos = get_rock_starting_position_z3(data)
    return rock_pos.x + rock_pos.y + rock_pos.z

def get_rock_starting_position_z3(hailstones):
    rock = z3.IntVector("r", 6)
    time = z3.IntVector("t", 3)

    solver = z3.Solver()

    for t, hailstone in zip(time, hailstones):
        solver.add(rock[0] + rock[3] * t == hailstone.pos.x + hailstone.vel.x * t)
        solver.add(rock[1] + rock[4] * t == hailstone.pos.y + hailstone.vel.y * t)
        solver.add(rock[2] + rock[5] * t == hailstone.pos.z + hailstone.vel.z * t)
    solver.check()
    model = solver.model()
    return Vector3(*[model[v].as_long() for v in (rock[0], rock[1], rock[2])])

def parse_input(data):
    hailstones = []
    for line in data:
        pos_str, vel_str = line.split(" @ ")
        pos = Vector3(*map(int, pos_str.split(", ")))
        vel = Vector3(*map(int, vel_str.split(", ")))
        hailstones.append(Hailstone(pos, vel))
    return hailstones
