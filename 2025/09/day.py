from itertools import combinations
from utils import Vector2

# Day 9

def run_part_1(data):
    tile_pairs = combinations(data, 2)
    areas = [(abs(pair[0].y - pair[1].y) + 1) * (abs(pair[0].x - pair[1].x) + 1) for pair in tile_pairs]
    return max(areas)

# Part 2 Stuff

def largest_area_in_polygon(red_tiles: list[Vector2]):
    num_points = len(red_tiles)
    
    edges = [(red_tiles[i], red_tiles[(i + 1) % num_points]) for i in range(num_points)]

    best_area = 0
    for i in range(num_points):
        for j in range(i + 1, num_points):
            point_a, point_b = red_tiles[i], red_tiles[j]
            point_min = Vector2(min(point_a.x, point_b.x), min(point_a.y, point_b.y))
            point_max = Vector2(max(point_a.x, point_b.x), max(point_a.y, point_b.y))

            if is_valid_rectangle(point_min, point_max, edges, red_tiles):
                best_area = max(best_area, ((point_max.x - point_min.x + 1) * (point_max.y - point_min.y + 1)))

    return best_area

def is_valid_rectangle(point_min: Vector2, point_max: Vector2, edges, vertices):
    for corner in [point_min, Vector2(point_min.x, point_max.y), Vector2(point_max.x, point_min.y), point_max]:
        if not is_point_in_polygon(corner, vertices):
            return False
    
    for edge in edges:
        if edge_crosses_rectangle(edge, point_min, point_max):
            return False
        
    return True

def is_point_in_polygon(point: Vector2, red_tiles: list[Vector2]):
    num_points = len(red_tiles)
    crossed = 0

    for i in range(num_points):
        point_a = red_tiles[i]
        point_b = red_tiles[(i + 1) % num_points]

        if point_a.x == point_b.x == point.x:
            if min(point_a.y, point_b.y) <= point.y <= max(point_a.y, point_b.y):
                return True
            
        if point_a.y == point_b.y == point.y:
            if min(point_a.x, point_b.x) <= point.x <= max(point_a.x, point_b.x):
                return True
            
        if point_a.x == point_b.x:
            if point_a.x < point.x and min(point_a.y, point_b.y) < point.y <= max(point_a.y, point_b.y):
                crossed += 1

    return crossed % 2 == 1

def edge_crosses_rectangle(edge: tuple[Vector2, Vector2], point_min: Vector2, point_max: Vector2):
    if edge[0] == edge[1]:
        if point_min.x < edge[0].x < point_max.x:
            if min(edge[0].y, edge[1].y) < point_max.y and max(edge[0].y, edge[1].y) > point_min.y:
                return True
            
    else:
        if point_min.y < edge[0].y < point_max.y:
            if min(edge[0].x, edge[1].x) < point_max.x and max(edge[0].x, edge[1].x) > point_min.x:
                return True
            
    return False

def run_part_2(data):
    return largest_area_in_polygon(data)
    # Another, this takes 10 seconds to run on my machine but I don't have time to do better right now

def parse_input(data):
    return [Vector2(*map(int, line.split(","))) for line in data]
