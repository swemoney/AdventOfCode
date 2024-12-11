from tqdm import tqdm
from functools import cache

# Day 11

def run_part_1(data):
    return blink_times(data, 25)

def run_part_2(data):
    return blink_times(data, 75)

def blink_times(stones, blinks):
    num_stones = 0
    for stone in stones: 
        num_stones += count(stone, blinks)
    return num_stones

@cache
def count(stone, blinks):
    rules = [replace_0_with_1, split_even_digit_stones, replace_times_2024]
    while blinks > 0:
        for rule in rules:
            if (new_stone := rule(stone)) == False: continue

            stone = new_stone
            blinks -= 1

            if type(stone) is list:
                num_stones = 0
                for split_stone in stone: 
                    num_stones += count(split_stone, blinks)
                return num_stones

    return 1

# Rule 1
def replace_0_with_1(stone) -> list[str]:
    if not stone == "0": return False
    return ["1"]

# Rule 2
def split_even_digit_stones(stone) -> list[str]:
    if not len(stone) % 2 == 0: return False
    return [stone[:len(stone)//2].lstrip("0") or "0", stone[len(stone)//2:].lstrip("0") or "0"]

# Rule 3
def replace_times_2024(stone) -> list[str]:
    return [str(int(stone) * 2024)]

# Brute force attempt at part 1 (do not attempt on part 2)
def brute_force_blink_times(stones, times):
    for _ in range(times):
        stones = [stone for nested_stone in brute_force_blink(stones) for stone in nested_stone]
    return stones

def brute_force_blink(stones):
    rules = [replace_0_with_1, split_even_digit_stones, replace_times_2024]
    for idx, stone in enumerate(stones):
        for rule in rules:
            if (new_stone := rule(stone)) == False: continue
            stones[idx] = new_stone
            break
    return stones

def parse_input(data):
    return data[0].split(" ")
