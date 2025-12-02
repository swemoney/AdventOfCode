# Day 1

MIN = 0
MAX = 100
START = 50

def run_part_1(data):
    dial_location = START
    hit_zero = 0

    for rotate_amount in data:
        dial_location += rotate_amount
        hit_zero += int(dial_location % MAX == MIN)

    return hit_zero

def run_part_2(data):
    dial_location = START
    hit_zero = 0

    for rotate_amount in data:
        if (rotate_amount > MIN) and (dial_location + rotate_amount >= MAX):
            hit_zero += (dial_location + rotate_amount) // MAX

        elif (dial_location != MIN) and (dial_location + rotate_amount <= MIN):
            hit_zero += 1 + abs(dial_location + rotate_amount) // MAX

        elif rotate_amount <= -MAX:
            hit_zero += abs(rotate_amount) // MAX

        dial_location = (dial_location + rotate_amount) % MAX

    return hit_zero

def parse_input(data):
    return [int(seq[1:]) * {"L":-1, "R":1}[seq[0]] for seq in data]
