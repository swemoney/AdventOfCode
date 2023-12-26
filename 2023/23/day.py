from collections import defaultdict
from utils import Directions, Vector2

# Day 23

DIRECTIONS = [
    Directions.north, 
    Directions.east, 
    Directions.south, 
    Directions.west
]

FOREST = "#"

SLOPE = {list("^>v<")[i]: direction for i, direction in enumerate(DIRECTIONS)}

def run_part_1(data):
    hiking_map, start, end = data
    return find_path_lengths(hiking_map, start, end)[0]

def run_part_2(data):
    hiking_map, start, end = data
    graph = create_graph(set(hiking_map.keys()), start, end)
    return hike_graph(graph, start)

# Used for part 1
def find_path_lengths(hiking_map: dict[Vector2, str], start: Vector2, end: Vector2):
    queue = [(start, set())]
    paths = []
    while queue:
        pos, path = queue.pop(0)
        if pos == end:
            paths.append(path)
            continue
        valid_dirs = [SLOPE[hiking_map[pos]]] if hiking_map[pos] in SLOPE.keys() else DIRECTIONS
        for direction in valid_dirs:
            next_pos = pos + direction.coords
            next_tile = hiking_map.get(next_pos)
            if next_tile == None or next_pos in path:
                continue
            next_path = set(path)
            next_path.add(next_pos)
            queue.append((next_pos, next_path))
    return sorted([len(p) for p in paths], reverse=True)

# Used for part 2
def create_graph(hiking_map: set[Vector2], start: Vector2, end: Vector2):
    graph = defaultdict(list)
    queue = [(start, start, {start})] # current, previous, seen
    while queue:
        node, prev_node, seen = queue.pop()
        
        if node == end:
            graph["final"] = (prev_node, len(seen) - 1)
            continue
        
        neighbors = []
        for direction in DIRECTIONS:
            neighbor = Vector2(node.x + direction.x, node.y + direction.y)
            if neighbor not in seen and neighbor in hiking_map:
                neighbors.append(neighbor)

        if len(neighbors) == 1:
            neighbor = neighbors.pop()
            queue.append((neighbor, prev_node, seen | {neighbor}))

        if len(neighbors) > 1:
            steps = len(seen) - 1
            if (node, steps) in graph[prev_node]:
                continue
            graph[prev_node].append((node, steps))
            graph[node].append((prev_node, steps))
            while neighbors:
                neighbor = neighbors.pop()
                queue.append((neighbor, node, {node, neighbor}))
    return graph

def hike_graph(graph: dict[Vector2, tuple[Vector2, int]], start: Vector2):
    max_steps = 0
    final_node, final_steps = graph["final"]
    queue = [(start, 0, {start})] # current, steps, seen
    while queue:
        node, steps, seen = queue.pop()
        if node == final_node:
            max_steps = max(steps, max_steps)
            continue
        for neighbor, dist in graph[node]:
            if neighbor not in seen:
                queue.append((neighbor, steps + dist, seen | {neighbor}))

    return max_steps + final_steps

def parse_input(data):
    start = Vector2(1, 0)
    end = Vector2(len(data[0])-2, len(data)-1)
    return ({Vector2(x, y): col for y, row in enumerate(data) for x, col in enumerate(row) if not col == FOREST}, start, end)
