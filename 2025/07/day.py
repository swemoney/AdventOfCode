from utils import array2d_to_dict, Vector2, Directions
from collections import deque, defaultdict

# Day 7

START = "S"
SPACE = "."
SPLIT = "^"

def run_part_1(data):
    start, manifold = data

    splitters = 0

    q = deque([start])
    seen = set()

    while q:
        coords = q.popleft()
        if coords in seen:
            continue

        seen.add(coords)

        next_coords = coords + Directions.south
        next_tile = manifold.get(next_coords)
        if next_tile is None:
            continue

        if next_tile == SPLIT:
            splitters += 1
            q.append(next_coords + Directions.east)
            q.append(next_coords + Directions.west)
            continue

        q.append(next_coords)

    return splitters

def run_part_2(data):
    start, manifold = data

    timelines = 0

    q = deque([start])
    paths = defaultdict(int)
    paths[start] = 1

    queued = set([start])

    while q:
        coords = q.popleft()
        queued.remove(coords)

        next_coords = coords + Directions.south
        next_tile = manifold.get(next_coords)
        if next_tile is None:
            timelines += paths[coords]
            continue

        if next_tile == SPLIT:
            new_paths = [next_coords + Directions.east, next_coords + Directions.west]
        else:
            new_paths = [next_coords]

        for new_path_coords in new_paths:
            new_path_tile = manifold.get(new_path_coords)
            if new_path_tile is None:
                timelines += paths[coords]
                continue

            paths[new_path_coords] += paths[coords]
            if new_path_coords not in queued:
                q.append(new_path_coords)
                queued.add(new_path_coords)

    return timelines

def parse_input(data) -> tuple[Vector2, dict[Vector2, str]]:
    manifold = array2d_to_dict(data, vector2=True)
    return (next((coords for coords, tile in manifold.items() if tile == START), None), manifold)
