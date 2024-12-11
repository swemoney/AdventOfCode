from utils import array2d_to_dict, Vector2, Directions

DIRECTIONS = [
    Directions.north,
    Directions.east,
    Directions.south,
    Directions.west
]

# Day 10

def run_part_1(data):
    trails = 0
    for coords, level in data.items():
        if int(level) == 0:
            visited = set()
            trails += walk(data, coords, 0, visited)
    return trails

def run_part_2(data):
    trails = 0
    for coords, level in data.items():
        if int(level) == 0:
            trails += walk(data, coords, 0, None)
    return trails

def walk(grid, coords, level, visited) -> int:
    if coords.x < 0 or coords.y < 0: return 0
    if (height := grid.get(coords)) == None: return 0
    if not height == level: return 0

    if visited != None:
        if level == 9 and coords not in visited:
            visited.add(coords)
            return 1 if height == level else 0
        
    else:
        if level == 9:
            return 1 if height == level else 0
            
    level += 1
    return sum([walk(grid, coords + direction.coords, level, visited) for direction in DIRECTIONS])

def parse_input(data):
    return array2d_to_dict(data, vector2=True, convert_with=int)
