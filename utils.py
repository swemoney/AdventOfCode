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
    
    def __eq__(self, other):
        if not isinstance(other, Vector2): return False
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return not self.eq(other)
    
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
