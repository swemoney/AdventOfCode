# Day 16

# Directions
UP = (-1, 0)
DOWN = (1, 0)
RIGHT = (0, 1)
LEFT = (0, -1)

# Map Tiles
SPACE = "."
S_SIDE = "-"
S_TALL = "|"
MIRRORS = ["/", "\\"]

# Redirections
MIRROR_DIR = {
    "/": { UP: RIGHT, DOWN: LEFT, RIGHT: UP, LEFT: DOWN },
    "\\": { UP: LEFT, DOWN: RIGHT, RIGHT: DOWN, LEFT: UP },
}

def run_part_1(data):
    return len(trace_beams(data, (0, -1), RIGHT))

def run_part_2(data):
    best_energy = 0
    for x in range(len(data)): # top row (DOWN)
        best_energy = max(best_energy, len(trace_beams(data, (-1, x), DOWN)))
    for x in range(len(data)): # bottom row (UP)
        best_energy = max(best_energy, len(trace_beams(data, (len(data), x), UP)))
    for y in range(len(data[0])): # left col (RIGHT)
        best_energy = max(best_energy, len(trace_beams(data, (y, -1), RIGHT)))
    for y in range(len(data[0])): # right col (LEFT)
        best_energy = max(best_energy, len(trace_beams(data, (y, len(data[0])), LEFT)))
    return best_energy

def trace_beams(data: [[str]], start_loc: (int, int), start_dir: (int, int)) -> set:
    energized = set()
    loc_stack = [(start_loc, start_dir)]
    while loc_stack:
        loc, dir = loc_stack.pop()
        loc = (loc[0] + dir[0], loc[1] + dir[1])

        if loc[0] < 0 or loc[1] < 0: continue
        if loc[0] >= len(data) or loc[1] >= len(data[0]): continue
        if (loc, dir) in energized: continue

        energized.add((loc, dir))

        tile = data[loc[0]][loc[1]]
        loc_stack.extend(updated_directions(loc, dir, tile))
    return set(l for l, _ in energized)
        
def updated_directions(loc: (int, int), dir: (int, int), tile: str) -> ((int,int),(int,int)):
    if tile in MIRRORS:
        return [(loc, MIRROR_DIR[tile][dir])]
    
    if tile == S_SIDE and (dir == UP or dir == DOWN):
        return [(loc, RIGHT), (loc, LEFT)]
    
    if tile == S_TALL and (dir == RIGHT or dir == LEFT):
        return [(loc, UP), (loc, DOWN)]
    
    return [(loc, dir)]

def parse_input(data):
    return [list(row) for row in data]
