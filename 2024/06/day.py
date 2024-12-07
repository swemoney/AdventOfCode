from utils import array2d_to_dict
from tqdm import tqdm
from copy import deepcopy

# Day 6

START_POS = "^"
OBSTACLE = "#"
DIRS = [(0,-1),(1,0),(0,1),(-1,0)]

def run_part_1(data):
    visited_with_directions = find_visited(data, get_starting_coords(data))
    visited_coords = {coords for (coords, _) in visited_with_directions} # create a new set of coords without the direction information
    return len(visited_coords)

def run_part_2(data):
    starting_coords = get_starting_coords(data)
    potential_obstacle_locations = {coords for (coords, _) in find_visited(data, starting_coords)}
    potential_obstacle_locations.remove(starting_coords)

    valid_obstable_locations = []
    for coords in tqdm(potential_obstacle_locations):
        if is_loop_with_new_obstacle(data, coords, starting_coords): 
            valid_obstable_locations.append(coords)

    return len(valid_obstable_locations)

def get_starting_coords(grid) -> tuple[int, int]:
    return list(grid.keys())[list(grid.values()).index(START_POS)]

def find_visited(grid, starting_coords) -> list[tuple[tuple[int,int], int]]:
    dir_idx, coords = 0, starting_coords
    visited = {(starting_coords, dir_idx)}
    while coords is not None:
        next_coords = (coords[0] + DIRS[dir_idx][0], coords[1] + DIRS[dir_idx][1])
        next_spot = grid.get(next_coords)

        if next_spot == None:
            coords = None
            continue

        if next_spot == OBSTACLE:
            dir_idx = (dir_idx + 1) % 4
            continue

        if (next_coords, dir_idx) in visited:
            return None
        
        coords = next_coords
        visited.add((coords, dir_idx))
    
    return visited

def is_loop_with_new_obstacle(grid, coords, starting_coords):
    if grid.get(coords) == OBSTACLE or coords == starting_coords: 
        return False
    
    new_grid = deepcopy(grid)
    new_grid[coords] = OBSTACLE
    return find_visited(new_grid, starting_coords) is None

def parse_input(data):
    return array2d_to_dict(data)
