from utils import Directions, Vector2, array2d_to_dict

# Day 4

NEIGHBORS = [
    Directions.north, Directions.northeast,
    Directions.east, Directions.southeast,
    Directions.south, Directions.southwest,
    Directions.west, Directions.northwest]

PAPER = "@"
SPACE = "."
NEIGHBOR_MAX = 3

def count_accessible_paper(data: dict, remove_accessible_paper: bool = False):
    accessible = 0

    for coords, tile in data.items():
        if tile is not PAPER: continue

        paper_found = 0
        for neighbor in NEIGHBORS:
            c = coords + neighbor.coords
            paper_found += (data.get(c, SPACE) == PAPER)
            if paper_found > NEIGHBOR_MAX: break

        if paper_found <= NEIGHBOR_MAX:
            accessible += 1
            if remove_accessible_paper:
                data[coords] = SPACE

    return accessible

def run_part_1(data):
    return count_accessible_paper(data)

def run_part_2(data):
    total_accessible_paper = 0
    accessible_paper = 0
    
    while True:
        accessible_paper = count_accessible_paper(data, remove_accessible_paper=True)
        if accessible_paper == 0: break
        total_accessible_paper += accessible_paper

    return total_accessible_paper

def parse_input(data):
    return array2d_to_dict(data, vector2=True)
