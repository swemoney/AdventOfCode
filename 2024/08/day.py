from utils import array2d_to_dict, Vector2
from itertools import combinations

# Day 8

def run_part_1(data):
    coords, bounds = data
    unique_signals = set(coords.values())
    antinodes = set()
    for signal in unique_signals:
        antinodes.update(find_antinodes(signal, coords, bounds))
    return len(antinodes)

def run_part_2(data):
    coords, bounds = data
    unique_signals = set(coords.values())
    antinodes = set()
    for signal in unique_signals:
        antinodes.update(find_antinodes(signal, coords, bounds, with_harmonics=True))
    return len(antinodes)

def find_antinodes(signal, coords, bounds, with_harmonics=False):
    ret = set()
    sig_pairs = list(combinations([key for key,val in coords.items() if val == signal], 2))
    for pair in sig_pairs:
        dist = pair[0] - pair[1]

        if with_harmonics:
            ret.update(set(pair))
        
        if not off_map(antinode := pair[0] + dist, bounds):
            ret.add(antinode)
            while with_harmonics and not off_map(antinode := antinode + dist, bounds):
                ret.add(antinode)

        if not off_map(antinode := pair[1] - dist, bounds):
            ret.add(antinode)
            while with_harmonics and not off_map(antinode := antinode - dist, bounds):
                ret.add(antinode)

    return ret

def off_map(node, bounds):
    return node.x >= bounds.x or node.y >= bounds.y or node.x < 0 or node.y < 0

def parse_input(data):
    grid = array2d_to_dict(data, vector2=True)
    return {key:val for key,val in grid.items() if val != "."}, Vector2(len(data[0]), len(data))
