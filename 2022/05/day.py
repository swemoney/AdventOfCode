# Day 5

from copy import deepcopy
import re

def run_part_1(data):
    stacks, instructions = deepcopy(data[0]), data[1]
    for instruction in instructions:
        for _ in range(instruction[0]):
            moving = stacks[instruction[1]].pop()
            stacks[instruction[2]].append(moving)
    return "".join(item[-1] for item in stacks)

def run_part_2(data):
    stacks, instructions = deepcopy(data[0]), data[1]
    for instruction in instructions:
        moving = stacks[instruction[1]][-instruction[0]:]
        stacks[instruction[2]].extend(moving)
        del stacks[instruction[1]][-instruction[0]:]
    return "".join(item[-1] for item in stacks)

def parse_input(data):
    stacks = [[],[],[],[],[],[],[],[],[]]
    instructions = []
    parsing = "stacks"
    for line in data:
        if line == "" or line[1] == "1":
            parsing = "instructions"
            continue
        if parsing == "stacks":
            for idx, char in enumerate(line):
                if (idx-1) % 4 == 0 and char != " ":
                    stacks[int((idx-1)/4)].append(char)
        if parsing == "instructions":
            match = re.search("^move (\d+) from (\d+) to (\d+)$", line)
            instructions.append([int(match.group(1)), int(match.group(2))-1, int(match.group(3))-1])

    reversed_stacks = []
    for stack in stacks:
        reversed_stacks.append(list(reversed(stack)))

    return (reversed_stacks, instructions)
