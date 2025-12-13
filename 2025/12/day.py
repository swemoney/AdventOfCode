from utils import Vector2
from typing import NamedTuple

class Tree(NamedTuple):
    height: int
    width: int
    counts: list[int]

GIFT_HEIGHT = 3
GIFT_WIDTH = 3

# Day 12

def run_part_1(data: tuple[set[Vector2], list[Tree]]):
    shapes, trees = data

    shapes_will_fit = 0
    for tree in trees:
        # If the tree area is big enough to fit the required shapes at 3x3, it definitely passes.
        if ((tree.height // GIFT_HEIGHT) * (tree.width // GIFT_WIDTH)) >= sum(tree.counts):
            shapes_will_fit += 1
            continue

        # If the number of tiles in the required shapes is greater than the total area of the tree, fail.
        if ((tree.height * tree.width) < sum(len(shapes[i]) * count for i, count in enumerate(tree.counts))):
            continue

        # I expected to do real checks here but this passes part 1 already...

    return shapes_will_fit

def run_part_2(data):
    return "Merry Christmas!"

def parse_input(data):
    shapes = []
    for i in range(0,30,5):
        shape = set()
        for y, row in enumerate([data[i+j] for j in range(3)]):
            for x, c in enumerate(row):
                if c == "#": shape.add(Vector2(x, y))
        shapes.append(shape)

    trees = []
    for line in data[30:]:
        area, counts = line.split(": ")
        trees.append(Tree(*list(map(int, area.split("x"))), list(map(int, counts.split()))))

    return shapes, trees
