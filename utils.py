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

def array2d_to_dict(l):
    d = {}
    for y in range(len(l)):
        for x in range(len(l[y])):
            d[(x,y)] = l[y][x]
    return d
