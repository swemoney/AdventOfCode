from utils import Directions, Point
from collections import namedtuple

# Day 18

PlanStep = namedtuple("PlanStep", ["direction","length","color"])
DIRECTIONS = {
    "U": Directions.north,
    "R": Directions.east,
    "D": Directions.south,
    "L": Directions.west,
    "0": Directions.east,
    "1": Directions.south,
    "2": Directions.west,
    "3": Directions.north }

def run_part_1(data):
    return get_area(data)

def run_part_2(data):
    plan = [PlanStep(DIRECTIONS[step.color[-1]], int(step.color[:-1], 16), "") for step in data]
    return get_area(plan)

def get_area(plan: list[PlanStep]) -> int:
    verts, perimeter = dig_edges(plan, Point(0, 0))
    return int(shoelace(verts) + (perimeter / 2) + 1)

def dig_edges(plan: list[PlanStep], start: Point) -> tuple[list[Point], int]:
    dug = [start]
    perimeter = 0
    for step in plan:
        y = dug[-1].y + (step.direction.y * step.length)
        x = dug[-1].x + (step.direction.x * step.length)
        dug.append(Point(y, x))
        perimeter += step.length
    return (dug, perimeter)

def shoelace(dug: list[Point]):
    area_y, area_x = 0, 0
    for i in range(len(dug) - 1):
        area_y += dug[i].y * dug[i + 1].x
        area_x += dug[i].x * dug[i + 1].y
    return abs(area_x - area_y) / 2

def parse_input(data):
    plan = []
    for line in data:
        direction, length, color = line.split(" ")
        plan.append(PlanStep(DIRECTIONS[direction], int(length), color.strip("(#)")))
    return plan
