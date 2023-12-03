import re
import math

# Day 3

line_offsets = [-1, 0, 1]
part_num_pattern = re.compile(r'(\d+)')
rand_sym_pattern = re.compile(r'[^\d\.]')
gear_pattern = re.compile(r'(\*)')

def run_part_1(data):
    part_numbers, _ = calculate_engine_data(data)
    return sum(list(part_numbers.values()))

def run_part_2(data):
    _, gears = calculate_engine_data(data)
    gear_ratios = [math.prod(gear) for gear in gears.values() if len(gear) == 2]
    return sum(gear_ratios)

def are_neighbors(y, x, py, px, num_len):
    return (x >= px - 1) and (x <= px + num_len) and (y >= py - 1) and (y <= py + 1)

def calculate_engine_data(data):
    part_numbers, gears = {}, {}
    for line_num, line in enumerate(data):
        part_matches = part_num_pattern.finditer(line)
        for part in part_matches:
            for line_offset in line_offsets:
                cur_line = line_num + line_offset
                if cur_line < 0 or cur_line >= len(data): continue
                symbol_matches = rand_sym_pattern.finditer(data[cur_line])
                for symbol in symbol_matches:
                    if are_neighbors(cur_line, symbol.span()[0], line_num, part.span()[0], len(part.group())):
                        part_numbers[(line_num, part.span()[0])] = int(part.group())
                        if symbol.group() == "*":
                            gear_index = (cur_line, symbol.span()[0])
                            gear = gears.get(gear_index)
                            if gear is not None:
                                gear.append(int(part.group()))
                            else:
                                gear = [int(part.group())]
                            gears[gear_index] = gear
                        break
    return (part_numbers, gears)

def parse_input(data):
    return data
