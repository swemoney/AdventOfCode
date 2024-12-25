# Day 25

type Code = tuple[int, int, int, int, int]

LOCK = "#####"
KEY = "....."
EMPTY = "."

def run_part_1(data):
    locks, keys = data
    valid_keys = 0
    for lock in locks:
        for key in keys:
            valid_key = True
            for pin in range(5):
                if key[pin] > (5 - lock[pin]):
                    valid_key = False
            valid_keys += valid_key
    return valid_keys

def run_part_2(data):
    return "N/A"

def parse_input(data) -> tuple[list[Code], list[Code]]:
    locks: list[Code] = []
    keys: list[Code] = []

    # Each new lock or key starts on each 8th index
    for idx in range(0, len(data), 8):
        
        if data[idx] == LOCK:
            code = [-1 for _ in range(5)]
            for pin in range(5):
                for length in range(6):
                    if data[idx + 1 + length][pin] == EMPTY:
                        code[pin] = length
                        break
            locks.append(tuple(code))
            continue

        if data[idx] == KEY:
            code = [-1 for _ in range(5)]
            for pin in range(5):
                for length in range(6):
                    if data[idx + 1 + length][pin] != EMPTY:
                        code[pin] = 5 - length
                        break
            keys.append(tuple(code))
            continue

    return locks, keys
