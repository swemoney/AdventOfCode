from utils import Vector2, a_star, CARDINAL_DIRECTIONS
from collections import deque
from tqdm import tqdm

MAX_XY, NUM_BYTES = 70, 1024

# Day 18

def run_part_1(data):
    end_coords = Vector2(MAX_XY, MAX_XY)
    start_coords = Vector2(0, 0)
    free_spaces = get_free_spaces_after_bytes_have_fallen(data, NUM_BYTES, end_coords)

    # I spent a stupid amount of time not getting this pretty simple A* algorithm to work.
    # Even added a bfs search which worked. The issue ended up being that the Node class 
    # wasn't being found in the open nodes set when I was adding neighbors. I added a more
    # explicit search for the neighbor coords instead of just a neighbor_node in open_nodes
    # and it finally worked. I think BFS was faster but I wanted to get A* working.
    path = a_star(free_spaces, start_coords, end_coords)
    return len(path) - 1

def run_part_2(data):
    end_coords = Vector2(MAX_XY, MAX_XY)
    start_coords = Vector2(0, 0)

    # I know there are more efficient ways of doing this, but I thought this was a fun way to brute force.
    # Instead of just iterating over each byte backwards, I jump a bunch of bytes and then when I find a path,
    # I split the jump in half and start from where we left off. This finishes in 7 seconds on my machine so 
    # I'm fine with that.
    start_byte = len(data)
    num_jumps = 100
    while num_jumps > 0:
        for num_bytes in tqdm(range(start_byte, NUM_BYTES, -num_jumps)):
            free_spaces = get_free_spaces_after_bytes_have_fallen(data, num_bytes, end_coords)
            path = a_star(free_spaces, start_coords, end_coords)
            if path is not None:
                num_jumps //= 2
                start_byte = num_bytes + num_jumps
                break
    return f"{data[num_bytes].x},{data[num_bytes].y}"

def get_free_spaces_after_bytes_have_fallen(bytes, num_of_bytes, bounds) -> set[Vector2]:
    free_spaces, fallen_bytes = set(), bytes[:num_of_bytes]
    for y in range(bounds.y + 1):
        for x in range(bounds.x + 1):
            coords = Vector2(x, y)
            if coords not in fallen_bytes:
                free_spaces.add(coords)
    return free_spaces

def parse_input(data):
    return [Vector2(*map(int, line.split(","))) for line in data]
