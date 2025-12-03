from itertools import combinations
from functools import cache

# Day 3

# First attempt
def best_combination(bank, num):
    return int("".join(max(list(combinations(bank, num)))))

@cache
def memoized_combinations(batteries, digits):

    if digits == 0: return 0
    if len(batteries) == digits:
        return int(batteries)
    
    current_battery = (int(batteries[0]) * 10 ** (digits - 1)) + memoized_combinations(batteries[1:], digits - 1)
    next_battery = memoized_combinations(batteries[1:], digits)

    return max(current_battery, next_battery)

def run_part_1(data):
    return sum([best_combination(bank, 2) for bank in data])

def run_part_2(data):
    return sum([memoized_combinations(bank, 12) for bank in data])

def parse_input(data):
    return data
