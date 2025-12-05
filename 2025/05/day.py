import math

# Day 5

def run_part_1(data):
    fresh, available = data

    fresh_found = 0
    for ingredient in available:
        for fresh_range in fresh:
            if ingredient in fresh_range:
                fresh_found += 1
                break

    return fresh_found

def run_part_2(data):
    fresh, _ = data
    fresh.sort(key=lambda r: r[0])

    total_fresh_ids = 0
    max_fresh_id = -1
    for fresh_range in fresh:
        min_fresh_id = max(max_fresh_id + 1, fresh_range[0])
        max_fresh_id = max(max_fresh_id, fresh_range[-1])
        total_fresh_ids += max(0, max_fresh_id - min_fresh_id + 1)

    return total_fresh_ids

def parse_input(data):
    fresh = []
    available = []

    fresh_is_done = False
    for line in data:
        if line == "":
            fresh_is_done = True
            continue

        if fresh_is_done:
            available.append(int(line))
        else:
            first, second = line.split("-")
            fresh.append(range(int(first), int(second) + 1))

    return (fresh, available)
