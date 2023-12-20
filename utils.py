from collections import namedtuple
from dataclasses import dataclass

# Various methods that I could probably use in multiple puzzles

# Access dict with dot notation
class DotDict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

# Named tuple for a point/coordinate (y, x)
Point = namedtuple("Point", ["y","x"])

@dataclass
class Direction:
    coords: Point
    name: str
    short: str

    @property
    def y(self):
        return self.coords.y
    
    @property
    def x(self):
        return self.coords.x

class Directions:
    north = Direction(coords=Point(-1, 0), name="North", short="N")
    northeast = Direction(coords=Point(-1, 1), name="North East", short="NE")
    east = Direction(coords=Point(0, 1), name="East", short="E")
    southeast = Direction(coords=Point(1, 1), name="South East", short="SE")
    south = Direction(coords=Point(1, 0), name="South", short="S")
    southwest = Direction(coords=Point(1, -1), name="South West", short="SW")
    west = Direction(coords=Point(0, -1), name="West", short="W")
    northwest = Direction(coords=Point(-1, -1), name="North West", short="NW")

DIRECTIONS = {
    "N": Point(-1, 0),
    "NE": Point(-1, 1),
    "E": Point(0, 1),
    "SE": Point(1, 1),
    "S": Point(1, 0),
    "SW": Point(1, -1),
    "W": Point(0, -1),
    "NW": Point(-1, -1)
}

def clamp(n, min, max):
    if n < min: return min
    elif n > max: return max
    else: return n 

