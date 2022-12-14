# Day 13

from json import loads
from functools import cmp_to_key
from math import prod

def run_part_1(data):
    pairs = []
    pair = []
    for line in data:
        if line == "":
            pairs.append(pair)
            pair = []
            continue      
        pair.append(loads(line))
    
    correct_pairs = []
    for i, p in enumerate(pairs):
        if compare(*p) <= 0:
            correct_pairs.append(i+1)
    return sum(correct_pairs)

def run_part_2(data):
    packets = []
    for line in data:
        if line == "": continue
        packets.append(loads(line))
    packets.append([[2]])
    packets.append([[6]])
    
    sorted_packets = sorted(packets, key=cmp_to_key(compare))
    return prod(i+1 for i, packet in enumerate(sorted_packets) if packet in [[[2]],[[6]]])

def compare(lhs, rhs):
    if type(lhs) is not type(rhs):
        if type(lhs) == int:
            return compare([lhs], rhs)
        else:
            return compare(lhs, [rhs])
    
    elif type(lhs) == int:
        if lhs < rhs: return -1
        else: return int(lhs > rhs)

    return next(
        (cmp for left, right in zip(lhs, rhs) if (cmp := compare(left, right))),
        -1 if len(lhs) < len(rhs) else int(len(lhs) > len(rhs)))

def parse_input(data):
    return data
