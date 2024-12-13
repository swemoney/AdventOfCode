from utils import array2d_to_dict, Vector2, Directions

DIRECTIONS = [Directions.north, Directions.east, Directions.south, Directions.west]

# Day 12

def run_part_1(data):
    regions, costs = find_regions(data), []

    for plant, plant_regions in regions.items():
        for region in plant_regions:
            costs.append(calculate_sides(data, region, plant)[0] * len(region))

    return sum(costs)

def run_part_2(data):
    regions, costs = find_regions(data), []

    for plant, plant_regions in regions.items():
        for region in plant_regions:
            costs.append(calculate_sides(data, region, plant)[1] * len(region))

    return sum(costs)

def find_regions(grid):
    regions: dict[str, list[set[Vector2]]] = {}

    for coords, plant in grid.items():
        if not any(coords in plant_region for plant_region in regions.get(plant, [])):
            region = find_connected(grid, coords)
            regions.setdefault(plant, []).append(region)
    return regions

def find_connected(grid, coords):
    start_coords = coords
    visited, to_visit = set(), [coords]
    plant = grid[start_coords]

    while to_visit:
        visiting_coords = to_visit.pop()
        visited.add(visiting_coords)
        for direction in DIRECTIONS:
            next_coords = visiting_coords + direction
            next_plant = grid.get(next_coords)
            if not next_plant == None and next_plant == plant and next_coords not in visited:
                to_visit.append(next_coords)
    return visited

def calculate_sides(grid, region, plant):
    perimeter, shared = 0, 0

    for coord in region:
        if grid.get(coord + Directions.north, "") != plant: # north
            perimeter += 1
            if grid.get(coord + Directions.west, "") == plant and grid.get(coord + Directions.northwest, "") != plant:
                shared += 1

        if grid.get(coord + Directions.south, "") != plant: # south
            perimeter += 1
            if grid.get(coord + Directions.west, "") == plant and grid.get(coord + Directions.southwest, "") != plant:
                shared += 1

        if grid.get(coord + Directions.west, "") != plant: # west
            perimeter += 1
            if grid.get(coord + Directions.north, "") == plant and grid.get(coord + Directions.northwest, "") != plant:
                shared += 1

        if grid.get(coord + Directions.east, "") != plant: # east
            perimeter += 1
            if grid.get(coord + Directions.north, "") == plant and grid.get(coord + Directions.northeast, "") != plant:
                shared += 1

    return perimeter, perimeter - shared

# Used this in part 1, switched to the side search above for both parts
def calculate_perimeter(region):
    perimeter = 0
    for coords in region:
        plot_perimeter = 4
        for direction in DIRECTIONS:
            neighbor = coords + direction
            if neighbor in region:
                plot_perimeter -= 1
        perimeter += plot_perimeter
    return perimeter

def parse_input(data):
    return array2d_to_dict(data, vector2=True)
