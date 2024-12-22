from utils import Vector2
from collections import Counter
from functools import cache
from typing import Iterator

# Day 21

type KeyPad = dict[str, Vector2]

DPAD = [
    [" ","^","A"],
    ["<","v",">"]]

NPAD = [
    ["7","8","9"],
    ["4","5","6"],
    ["1","2","3"],
    [" ","0","A"]]

NPAD_COORDS = {char: Vector2(x, y) for y, row in enumerate(NPAD) for x, char in enumerate(row)}
DPAD_COORDS = {char: Vector2(x, y) for y, row in enumerate(DPAD) for x, char in enumerate(row)}

KEYPADS = [NPAD_COORDS, DPAD_COORDS]
NUMPAD = 0
DIRPAD = 1

# Took a lot of this code from reddit and made it my own the best I could. Time is too short.
# https://github.com/janek37/advent-of-code/blob/main/2024/day21.py

def run_part_1(data):
    shortest_sequences = [find_shortest_sequence(code, num_robots=2) for code in data]
    return sum(int(code[:-1]) * shortest_sequences[i] for i, code in enumerate(data))

def run_part_2(data):
    shortest_sequences = [find_shortest_sequence(code, num_robots=25) for code in data]
    return sum(int(code[:-1]) * shortest_sequences[i] for i, code in enumerate(data))

@cache
def find_shortest_sequence(code: str, num_robots: int, keypad: int = NUMPAD) -> int:
    sequences = keypad_control_sequences(code, start="A", keypad=keypad)
    
    if num_robots == 0:
        return min(sum(len(part) for part in sequence) for sequence in sequences)
    return min(sum(find_shortest_sequence(code, num_robots - 1, DIRPAD) for code in sequence) for sequence in sequences)

def keypad_control_sequences(code: str, start: str, keypad: int) -> list[list[str]]:
    if code == "": return [[]]
    coords = KEYPADS[keypad][start]
    next_coords = KEYPADS[keypad][code[0]]

    ret = []
    for option in move_options(coords, next_coords, keypad):
        for sequence in keypad_control_sequences(code[1:], start=code[0], keypad=keypad):
            ret.append([option, *sequence])
    return ret

def move_options(start: Vector2, end: Vector2, keypad: int) -> Iterator[str]:
    h_arrow = "<" if end.x < start.x else ">"
    v_arrow = "^" if end.y < start.y else "v"
    dist = Vector2(abs(start.x - end.x), abs(start.y - end.y))

    if start == end: yield "A"
    elif start.x == end.x: yield v_arrow * dist.y + "A"
    elif start.y == end.y: yield h_arrow * dist.x + "A"
    else:
        missing_key = KEYPADS[keypad][" "]
        if not ((missing_key.x == end.x and missing_key.y in nonempty_range(start.y, end.y)) or \
                (missing_key.y == start.y and missing_key.x in nonempty_range(end.x, start.x))):
            yield h_arrow * dist.x + v_arrow * dist.y + "A"

        if not ((missing_key.x == start.x and missing_key.y in nonempty_range(end.y, start.y)) or \
                (missing_key.y == end.y and missing_key.x in nonempty_range(start.x, end.x))):
            yield v_arrow * dist.y + h_arrow * dist.x + "A"

def nonempty_range(start, end) -> range:
    return range(start, end) if start < end else range(start, end, -1)

def parse_input(data):
    return data
