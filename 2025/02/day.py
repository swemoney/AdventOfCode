import re

# Day 2

def run_part_1(data):
    valid_ids = []

    for r in data:
        for x in r:
            id = str(x)
            if id[:len(id)//2] == id[(len(id)//2):]:
                valid_ids.append(int(id))

    return sum(valid_ids)

def run_part_2(data):
    valid_ids = []

    for r in data:
        for x in r:
            id = str(x)
            for i in range(1, len(id)//2 + 1):
                pattern = id[:i]
                if len(id) % len(pattern) != 0:
                    continue

                if id.count(pattern) == len(id)//len(pattern):
                    valid_ids.append(int(id))
                    break

    return sum(valid_ids)

def parse_input(data):
    ranges = []
    for r in data[0].split(","):
        low, high = r.split("-")
        ranges.append(range(int(low), int(high)+1))
    return ranges
