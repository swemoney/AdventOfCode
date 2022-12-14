# Day 14

from copy import deepcopy

def run_part_1(data):
    blocked = deepcopy(data)
    max_y = max(blocked, key=lambda c: c[1])[1]
    sand_fallen = 0
    while move_sand(blocked, max_y) is not None:
        sand_fallen += 1
    return sand_fallen

def run_part_2(data):
    blocked = deepcopy(data)
    max_y = max(blocked, key=lambda c: c[1])[1]
    for i in range(500-max_y-5,500+max_y+5): # Add the bottom floor at the maximum size needed
        blocked.add((i,max_y+2))
    sand_fallen = 1
    while move_sand(blocked, max_y) is not None:
        sand_fallen += 1
    return sand_fallen

def move_sand(blocked, max_y, sand_pos=(500,0)):
    x, y = sand_pos
    if y > max_y + 2: return None

    moves = [(x, y+1), (x-1, y+1), (x+1, y+1)]
    for move in moves:
        if move not in blocked:
            return move_sand(blocked, max_y, move)

    if sand_pos == (500,0): return None

    blocked.add(sand_pos)
    return sand_pos

def parse_input(data):
    rocks = set()
    for line in data:
        coords = [[int(pos) for pos in coord.split(",")] for coord in line.split(" -> ")]
        for i, cur in enumerate(coords):
            if i == len(coords) - 1: break
            cx, cy = cur
            nx, ny = coords[i+1]
            if cx == nx: # Vertical Movement
                step = -1 if cy > ny else 1 
                for j in range(cy, ny+step, step):
                    rocks.add((cx,j))
            if cy == ny: # Horizontal Movement
                step = -1 if cx > nx else 1
                for j in range(cx, nx+step, step):
                    rocks.add((j,cy))
    return rocks
