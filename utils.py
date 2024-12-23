from dataclasses import dataclass, fields
from heapq import heappush, heappop

# Various methods that I could probably use in multiple puzzles

# Access dict with dot notation
class DotDict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

@dataclass(frozen=True)
class Vector2:
    x: int
    y: int

    def __add__(self, other):
        return type(self)(*[getattr(self, f.name) + getattr(other, f.name) for f in fields(self)])
    
    def __sub__(self, other):
        return type(self)(*[getattr(self, f.name) - getattr(other, f.name) for f in fields(self)])
    
    def __mul__(self, other):
        return type(self)(*[getattr(self, f.name) * getattr(other, f.name) for f in fields(self)])
    
    def __div__(self, other):
        return type(self)(*[getattr(self, f.name) / getattr(other, f.name) for f in fields(self)])
    
    def __eq__(self, other):
        if not isinstance(other, Vector2): return False
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        if not isinstance(other, Vector2): return False
        return (self.x, self.y) < (other.x, other.y)
    
    def __gt__(self, other):
        if not isinstance(other, Vector2): return False
        return (self.x, self.y) > (other.x, other.y)
    
    def __le__(self, other):
        if not isinstance(other, Vector2): return False
        return (self.x, self.y) <= (other.x, other.y)
    
    def __ge__(self, other):
        if not isinstance(other, Vector2): return False
        return (self.x, self.y) >= (other.x, other.y)
    
    def __hash__(self):
        return hash(str(self))
    
    def __str__(self):
        return f"Vector2({self.x}, {self.y})"
    
    def __repr__(self):
        return str(self)

@dataclass(frozen=True)
class Vector3(Vector2):
    z: int

@dataclass(frozen=True)
class Direction:
    coords: Vector2
    name: str
    short: str

    def __getattr__(self, attr):
        if attr in ["x","y"]:
            return getattr(self.coords, attr)
        return super().__getattribute__(attr)
   
@dataclass(frozen=True)
class Directions:
    north = Direction(coords=Vector2(0, -1), name="North", short="N")
    northeast = Direction(coords=Vector2(1, -1), name="North East", short="NE")
    east = Direction(coords=Vector2(1, 0), name="East", short="E")
    southeast = Direction(coords=Vector2(1, 1), name="South East", short="SE")
    south = Direction(coords=Vector2(0, 1), name="South", short="S")
    southwest = Direction(coords=Vector2(-1, 1), name="South West", short="SW")
    west = Direction(coords=Vector2(-1, 0), name="West", short="W")
    northwest = Direction(coords=Vector2(-1, -1), name="North West", short="NW")

def clamp(n, min, max):
    if n < min: return min
    elif n > max: return max
    else: return n

def array2d_to_dict(l, vector2=False, convert_with=None):
    d = {}
    for y in range(len(l)):
        for x in range(len(l[y])):
            val = convert_with(l[y][x]) if convert_with != None else l[y][x]
            if vector2:
                d[Vector2(x, y)] = val
            else:
                d[(x,y)] = val
    return d

def print_grid(grid: dict[Vector2, str]):
    all_x = [pos.x for pos in grid.keys()]
    all_y = [pos.y for pos in grid.keys()]
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    for y in range(min_y, max_y + 1):
        row = ""
        for x in range(min_x, max_x + 1):
            row += grid.get(Vector2(x, y), "?")
        print(row.strip())

class AStarNode:
    def __init__(self, coords: Vector2, parent=None):
        self.coords = coords
        self.parent = parent

        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f
    
CARDINAL_DIRECTIONS = [Directions.east.coords, Directions.south.coords, Directions.west.coords, Directions.north.coords]

def a_star(free_spaces: set[Vector2], start_coords: Vector2, end_coords: Vector2, deltas: list[Vector2] = CARDINAL_DIRECTIONS):
    open_nodes: list[AStarNode] = []
    closed: set[Vector2] = set()

    start_node  = AStarNode(start_coords)
    heappush(open_nodes, start_node)

    while open_nodes:
        current_node = heappop(open_nodes)
        closed.add(current_node.coords)
        
        if current_node.coords == end_coords:
            path: list[Vector2] = []
            while current_node:
                path.append(current_node.coords)
                current_node = current_node.parent
            return path[::-1]
        
        for neighbor in get_neighbors(free_spaces, current_node.coords, deltas):
            if neighbor in closed: continue
            neighbor_node = AStarNode(neighbor, parent=current_node)
            neighbor_node.g = current_node.g + 1
            neighbor_node.h = manhattan_distance(neighbor, end_coords)
            neighbor_node.f = neighbor_node.g + neighbor_node.h

            existing_node = next((node for node in open_nodes if node.coords == neighbor), None)
            if existing_node and existing_node.g <= neighbor_node.g: continue

            heappush(open_nodes, neighbor_node)

    return None

def manhattan_distance(a: Vector2, b: Vector2):
    return abs(a.x - b.x) + abs(a.y - b.y)

def get_neighbors(free_spaces: set[Vector2], coords: Vector2, deltas: list[Vector2] = CARDINAL_DIRECTIONS):
    return [coords + delta for delta in deltas if coords + delta in free_spaces]