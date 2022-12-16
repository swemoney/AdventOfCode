# Day 15

import re
from collections import namedtuple
from math import inf

Sensor = namedtuple("Sensor", "x y range")

def manhattan(start_x, start_y, end_x, end_y):
    return abs(start_x - end_x) + abs(start_y - end_y)

def run_part_1(data):
    scan_y = 2000000
    min_x, max_x = inf, -inf
    for sensor in data:
        diff_y = abs(scan_y - sensor.y)
        if diff_y > sensor.range: continue
        diff_x = sensor.range - diff_y
        min_x = min(sensor.x - diff_x, min_x)
        max_x = max(sensor.x + diff_x, max_x)
    return max_x - min_x

def run_part_2(data):
    max_y = 4000000
    for y in range(max_y):
        if x := gap_found(data, y):
            return x * max_y + y
    return (x * max_y) + y

def gap_found(sensors, y): # This took about a minute to complete but brute force is the best I can do right now
    ranges = []
    for sensor in sensors:
        diff_y = abs(y - sensor.y)
        if diff_y > sensor.range: continue
        diff_x = sensor.range - diff_y
        ranges.append((sensor.x - diff_x, sensor.x + diff_x))
    ranges.sort()
    min_x, max_x = ranges[0]
    for start, end in ranges[1:]:
        check_min = min_x - 1
        if start < check_min and end < check_min:
            return check_min
        check_max = max_x + 1
        if start > check_max and end > check_max:
            return check_max
        min_x = min(start, min_x)
        max_x = max(end, max_x)
    return False

def parse_input(data):
    sensors = set()
    for line in data:
        m = list(map(int, re.findall("(-?\d+)", line)))
        range = manhattan(*m)
        sensor = Sensor(m[0], m[1], range)
        sensors.add(sensor)
    return sensors
