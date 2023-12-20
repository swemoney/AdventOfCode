from collections import namedtuple

# Various methods that I could probably use in multiple puzzles

# Access dict with dot notation
class DotDict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

Point = namedtuple("Point", ["y","x"])
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

