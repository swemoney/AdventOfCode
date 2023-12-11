from itertools import combinations

# Day 11

GALAXY = "#"
SPACE = "."

def run_part_1(data):
    galaxies, empty_rows, empty_cols = data
    return sum(distances(galaxies, empty_rows, empty_cols, expansion=2))

def run_part_2(data):
    galaxies, empty_rows, empty_cols = data
    return sum(distances(galaxies, empty_rows, empty_cols, expansion=1_000_000))

def distances(galaxies, empty_rows, empty_cols, expansion):
    distances = []
    for g1, g2 in combinations(galaxies, 2):
        small_y, big_y = min(g1[0], g2[0]), max(g1[0], g2[0])
        small_x, big_x = min(g1[1], g2[1]), max(g1[1], g2[1])
        expanded_rows = len([row for row in empty_rows if row in range(small_y, big_y)])
        expanded_cols = len([col for col in empty_cols if col in range(small_x, big_x)])
        distances.append(manhattan(g1, g2) + (expanded_rows*(expansion-1)) + (expanded_cols*(expansion-1)))
    return distances

def manhattan(g1, g2):
    return abs(g2[1] - g1[1]) + abs(g2[0] - g1[0])

def all_galaxies(data):
    return [(y, x) for y in range(len(data)) for x in range(len(data[0])) if data[y][x] == GALAXY]

def find_empty_rows(data):
    return [y for y, row in enumerate(data) if not GALAXY in row]

def find_empty_cols(data):
    cols = [[row[i] for row in data] for i in range(len(data[0]))]
    return [x for x, col in enumerate(cols) if not GALAXY in col]

def parse_input(data):
    empty_rows = find_empty_rows(data)
    empty_cols = find_empty_cols(data)
    galaxies = all_galaxies(data)
    return (galaxies, empty_rows, empty_cols)
