from utils import array2d_to_dict, Vector2, Directions, Direction
from typing import NewType

# Day 15

Tile = NewType("Tile", str)
type Grid = tuple[dict[Vector2, Tile], Vector2]

DIRECTIONS = {
    "^": Directions.north,
    ">": Directions.east,
    "v": Directions.south,
    "<": Directions.west
}

SMALL_BOX = Tile("O")
BIG_BOX = [Tile("["), Tile("]")]
WALL  = Tile("#")
SPACE = Tile(".")
ROBOT = Tile("@")

# With the way my template is structured, I found it hard to find good places to consolidate code so I just ran everything in the part1 and part2 methods

def run_part_1(data):
    grid, _, instructions = data # use warehouse1 (ignore warehose2)
    robot_pos = get_robot_pos(grid)

    for direction in instructions:
        dest_coords = robot_pos + DIRECTIONS[direction]
        dest_tile = grid.get(dest_coords, WALL)
        if dest_tile == WALL: continue
        if dest_tile == SPACE: 
            robot_pos = move_robot(grid, robot_pos, dest_coords)
            continue
        
        if (empty_coords := next_empty_space(grid, dest_coords, DIRECTIONS[direction])) == None: continue
        robot_pos = move_robot(grid, robot_pos, dest_coords, empty_coords)

    gps = [gps_coords(coords) for coords,tile in grid.items() if tile == SMALL_BOX]
    return sum(gps)

def run_part_2(data):
    _, grid, instructions = data # Use warehouse2 this time
    robot_pos = get_robot_pos(grid)
    for direction in instructions:
        d = DIRECTIONS[direction]
        dest_coords = robot_pos + d
        dest_tile = grid.get(dest_coords, WALL)
        if dest_tile == WALL: continue
        if dest_tile == SPACE:
            robot_pos = move_robot(grid, robot_pos, dest_coords)
            continue

        # Horizontal movement (Similar to part 1 but we shift each tile until the empty space instead of just swapping the first and last tiles)
        if direction in ["<",">"]:
            if (empty_coords := next_empty_space(grid, dest_coords, DIRECTIONS[direction])) == None: continue
            while empty_coords != dest_coords:
                grid[empty_coords] = grid[empty_coords - d]
                empty_coords = empty_coords - d
            robot_pos = move_robot(grid, robot_pos, dest_coords)

        # Vertical movement (More complex)
        else:

            # Construct a list of all tiles that need to be moved
            def get_box_chain():
                queue = []
                queue.append(robot_pos)
                visited = {}
                visited[dest_coords] = grid[dest_coords]
                while queue:
                    curr_coords = queue.pop(0)
                    peek_coords = curr_coords + d

                    if grid[peek_coords] == WALL: return None
                    if grid[peek_coords] == SPACE: continue

                    visited[peek_coords] = grid[peek_coords]
                    if grid[peek_coords] in BIG_BOX:
                        if grid[peek_coords] == BIG_BOX[0]:   # [
                            other_side_coords = peek_coords + Directions.east
                        elif grid[peek_coords] == BIG_BOX[1]: # ]
                            other_side_coords = peek_coords + Directions.west
                        queue.append(peek_coords)
                        queue.append(other_side_coords)
                        visited[other_side_coords] = grid[other_side_coords]
                return visited
            
            tiles_to_shift = get_box_chain()
            if tiles_to_shift:
                for coords, _ in tiles_to_shift.items():
                    grid[coords] = SPACE
                for coords, tile in tiles_to_shift.items():
                    grid[coords + d] = tile

                robot_pos = move_robot(grid, robot_pos, dest_coords)

    gps = [gps_coords(coords) for coords,tile in grid.items() if tile == BIG_BOX[0]]
    return sum(gps)

def move_robot(grid: Grid, old_coords, new_coords, empty_coords=None):
    grid[old_coords] = SPACE
    grid[new_coords] = ROBOT
    if empty_coords != None: grid[empty_coords] = SMALL_BOX
    return new_coords

def next_empty_space(grid: Grid, coords: Vector2, direction: Direction) -> Vector2:
    dest_coords = coords + direction
    dest_tile = grid.get(dest_coords, WALL)
    while dest_tile != WALL:
        if dest_tile == SPACE: return dest_coords
        dest_coords = dest_coords + direction
        dest_tile = grid.get(dest_coords, WALL)
    return None

def gps_coords(coords: Vector2) -> int:
    return (100 * coords.y) + coords.x

def get_robot_pos(grid: Grid) -> Vector2:
    return list(grid.keys())[list(grid.values()).index(ROBOT)]

def parse_input(data) -> tuple[Grid, str, Vector2]: # warehouse_1, warehouse_2, insructions
    warehouse_1, warehouse_2, instructions = [], [], []
    divider = data.index("")
    for idx, line in enumerate(data):
        if idx < divider: 
            warehouse_1.append(line)
            warehouse_2.append(line.replace("#","##").replace("O","[]").replace(".","..").replace("@","@."))
        else: instructions.append(line)
    return (
        array2d_to_dict(warehouse_1, vector2=True, convert_with=Tile), 
        array2d_to_dict(warehouse_2, vector2=True, convert_with=Tile), 
        "".join(instructions)
    )