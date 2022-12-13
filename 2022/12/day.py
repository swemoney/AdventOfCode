# Day 12

from copy import deepcopy
from collections import deque

class Node:
    def __init__(self, char):
        self.char = char
        self.pred = None
        self.dist = -1
        self.neighbors = []

def bfs(start, end):
    queue = deque()
    start.dist = 0
    queue.append(start)
    while len(queue) > 0:
        node = queue.popleft()
        for neighbor in node.neighbors:
            if neighbor.dist == -1:
                neighbor.dist = node.dist + 1
                neighbor.pred = node
                queue.append(neighbor)
    return end.dist

def run_part_1(data):
    start, end = data[1:]
    return bfs(start, end)

def run_part_2(data):
    grid, start, end = data
    starts = [node for node in grid.values() if node.char == "a"]
    paths = []
    for start in starts:
        for node in grid.values():
            node.dist = -1
            node.pred = None
        path = bfs(start, end)
        if path > 0: paths.append(path)
    return min(paths)

def parse_input(data):
    grid, start, end = {}, None, None
    for y, row in enumerate(data):
        for x, col in enumerate(row):
            if col == "S":
                start = Node("a")
                grid[(x,y)] = start
                continue
            if col == "E":
                end = Node("z")
                grid[(x,y)] = end
                continue
            grid[(x,y)] = Node(col)

    # Find neighbors
    for (x,y), node in grid.items():
        for (nx, ny) in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
            neighbor = grid.get((nx,ny))
            if neighbor == None: continue
            if (ord(neighbor.char) - 1) <= ord(node.char):
                node.neighbors.append(neighbor)

    return grid, start, end
