from copy import deepcopy

# Day 14

SPACE = "."
ROUND = "O"
CUBE = "#"

NORTH = (-1, 0)
SOUTH = (1, 0)
EAST = (0, 1)
WEST = (0, -1)

def run_part_1(data):
    tilted_mirror = tilt(deepcopy(data), NORTH)
    return calculate_load(tilted_mirror)

def run_part_2(data): # Takes 30 seconds to finish ¯\_(ツ)_/¯
    return run_cycles(deepcopy(data), 1_000_000_000)
            
def run_cycles(data: [[str]], num_cycles):
    mirror = deepcopy(data)
    count, cycle = 0, {}
    round_rocks = round_rock_set(mirror)
    
    while True:
        cycle[frozenset(round_rocks)] = count
        mirror = tilt(mirror, NORTH)
        mirror = tilt(mirror, WEST)
        mirror = tilt(mirror, SOUTH)
        mirror = tilt(mirror, EAST)
        round_rocks = round_rock_set(mirror)
        count += 1

        if frozenset(round_rocks) in cycle.keys():
            repeat = count - cycle[frozenset(round_rocks)]
            if (num_cycles - count) % repeat == 0:
                return calculate_load(mirror)

def round_rock_set(data):
    return set([(y, x) for y, line in enumerate(data) for x, char in enumerate(line) if char == ROUND])

def tilt(data: [[str]], direction: (int, int)):
    if direction == NORTH:
        y_range, x_range = range(len(data)), range(len(data[0]))
    elif direction == SOUTH:
        y_range, x_range = range(len(data), -1, -1), range(len(data[0]))
    elif direction == EAST:
        y_range, x_range = range(len(data)), range(len(data[0]), -1, -1)
    else:
        y_range, x_range = range(len(data)), range(len(data[0]))

    while True:
        rocks_moved = False
        for y in y_range:
            for x in x_range:
                if y + direction[0] < 0 or y + direction[0] >= len(data): continue
                if x + direction[1] < 0 or x + direction[1] >= len(data[0]): continue
                if data[y][x] == ROUND and data[y + direction[0]][x + direction[1]] == SPACE:
                    data[y + direction[0]][x + direction[1]] = ROUND
                    data[y][x] = SPACE
                    rocks_moved = True
        if not rocks_moved: break
    return data

def calculate_load(data: [[str]]):
    load = 0
    for y in range(len(data)):
        for x in range(len(data)):
            if data[y][x] == ROUND:
                load += (len(data) - y)
    return load

def parse_input(data):
    return [list(line) for line in data]
