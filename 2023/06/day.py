import re
import math

# Day 6

re_num = re.compile(r"(\d+)")

def run_part_1(data):
    times, dists = data
    possibles = [find_possible_wins(race_time, dists[race_num]) for race_num, race_time in enumerate(times)]
    return math.prod(possibles)

def run_part_2(data):
    time = int("".join(str(t) for t in data[0]))
    dist = int("".join(str(d) for d in data[1]))
    return find_possible_wins(time, dist)

def find_possible_wins(race_time, distance_to_beat):
    first_winning_time = find_winning_time(race_time, distance_to_beat)
    last_winning_time = find_winning_time(race_time, distance_to_beat, reverse=True)
    return len(range(first_winning_time, last_winning_time)) + 1

def find_winning_time(race_time, distance_to_beat, reverse = False):
    race_range = range(race_time - 1, 1, -1) if reverse else range(1, race_time - 1)
    for hold_time in race_range:
        if (race_time - hold_time) * hold_time > distance_to_beat:
            return hold_time

def parse_input(data):
    times = [int(t) for t in re_num.findall(data[0])]
    dists = [int(d) for d in re_num.findall(data[1])]
    return (times, dists)
