from dataclasses import dataclass, fields

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

@dataclass(frozen=True)
class Vector3(Vector2):
    z: int

DIRECTIONS = {
    "N": Vector2(0, -1),
    "NE": Vector2(1, -1),
    "E": Vector2(1, 0),
    "SE": Vector2(1, 1),
    "S": Vector2(0, 1),
    "SW": Vector2(-1, 1),
    "W": Vector2(-1, 0),
    "NW": Vector2(-1, -1)
}

@dataclass(frozen=True)
class Direction:
    coords: Vector2
    name: str
    short: str

    def __getattr__(self, attr):
        if attr in ["x","y"]:
            return getattr(self.coords, attr)
        return self.coords
   
class Directions:
    north = Direction(coords=DIRECTIONS["N"], name="North", short="N")
    northeast = Direction(coords=DIRECTIONS["NE"], name="North East", short="NE")
    east = Direction(coords=DIRECTIONS["E"], name="East", short="E")
    southeast = Direction(coords=DIRECTIONS["SE"], name="South East", short="SE")
    south = Direction(coords=DIRECTIONS["S"], name="South", short="S")
    southwest = Direction(coords=DIRECTIONS["SW"], name="South West", short="SW")
    west = Direction(coords=DIRECTIONS["W"], name="West", short="W")
    northwest = Direction(coords=DIRECTIONS["NW"], name="North West", short="NW")

def clamp(n, min, max):
    if n < min: return min
    elif n > max: return max
    else: return n 
