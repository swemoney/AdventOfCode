from utils import array2d_to_dict

# Day 4

XMAS_COORDS = [ # offsets for MAS after finding an X
    [(1,0), (2,0), (3,0)],       # East
    [(1,1), (2,2), (3,3)],       # South East
    [(0,1), (0,2), (0,3)],       # South
    [(-1,1), (-2,2), (-3,3)],    # South West
    [(-1,0), (-2,0), (-3,0)],    # West
    [(-1,-1), (-2,-2), (-3,-3)], # North West
    [(0,-1), (0,-2), (0,-3)],    # North
    [(1,-1), (2,-2), (3,-3)]     # North East
]

MAS_X_COORDS = [ # offsets for M, S, M, S after finding an A
    [(-1,-1), (1, 1), (-1, 1), (1, -1)], 
    [(-1,-1), (1, 1), (1, -1), (-1, 1)],
    [(-1, 1), (1, -1), (1, 1), (-1, -1)],
    [(1, -1), (-1, 1), (1, 1), (-1, -1)]
]

def run_part_1(data):
    og_data, wordsearch = data
    xmas_count = 0
    for y in range(len(og_data)):
        for x in range(len(og_data[y])):
            if not wordsearch[(x,y)] == "X": continue
            for c in XMAS_COORDS:
                if not wordsearch.get((x + c[0][0], y + c[0][1])) == "M": continue
                if not wordsearch.get((x + c[1][0], y + c[1][1])) == "A": continue
                if not wordsearch.get((x + c[2][0], y + c[2][1])) == "S": continue
                xmas_count += 1
    return xmas_count

def run_part_2(data):
    og_data, wordsearch = data
    mas_x_count = 0
    for y in range(len(og_data)):
        for x in range(len(og_data[y])):
            if not wordsearch[(x,y)] == "A": continue
            for c in MAS_X_COORDS:
                if wordsearch.get((x + c[0][0], y + c[0][1])) == "M" and \
                   wordsearch.get((x + c[1][0], y + c[1][1])) == "S" and \
                   wordsearch.get((x + c[2][0], y + c[2][1])) == "M" and \
                   wordsearch.get((x + c[3][0], y + c[3][1])) == "S": mas_x_count += 1
    return mas_x_count

def parse_input(data): # easier to lookup and disregard out of bounds coords in a dictionary
    return data, array2d_to_dict(data)
