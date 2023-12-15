import re

# Day 15

DASH = "-"
EQUALS = "="

re_step = re.compile(r"(.+)(=|-)(.*)")

def run_part_1(data):
    return sum([hash(step) for step in data.split(",")])

def run_part_2(data):
    boxes = [[] for _ in range(256)]
    steps = data.split(",")
    for step in steps:
        run_step(step, boxes)
    return sum(calculate_focusing_power(boxes))

def calculate_focusing_power(boxes):
    lens_power = []
    for box_i, box in enumerate(boxes):
        for lens_i, lens in enumerate(box):
            lens_power.append( (box_i + 1) * (lens_i + 1) * int(lens["length"]) )
    return lens_power

def run_step(step: str, boxes: [[{str, int}]]):
    label, operation, length = re_step.match(step).groups()
    box = hash(label)
    lens = {"label": label, "length": length}

    old_lens, idx = None, None
    for i, l in enumerate(boxes[box]):
        if l["label"] == label:
            old_lens, idx = l, i
            break

    if operation == DASH and not old_lens == None:
        del boxes[box][idx]
    elif operation == EQUALS:
        if old_lens == None:
            boxes[box].append(lens)
        else:
            boxes[box][idx] = lens

def hash(string: str):
    val = 0
    for char in list(string):
        val = ((val + ord(char)) * 17) % 256
    return val

def parse_input(data):
    return data[0]
