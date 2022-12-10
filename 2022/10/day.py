# Day 10

SCREEN_WIDTH = 40
SCREEN_HEIGHT = 6

def run_part_1(data):
    cycles_to_test = [20, 60, 100, 140, 180, 220]
    values, cycle, x = [], 1, 1
    for instruction in data:
        if len(cycles_to_test) == 0:
            break
        if instruction == "noop":
            cycle += 1
            continue
        inc_x = int(instruction.split(" ")[1])
        cycle += 2
        x += inc_x
        if cycle == cycles_to_test[0]:
            values.append(x * cycles_to_test.pop(0))
        elif cycle > cycles_to_test[0]:
            values.append((x - inc_x) * cycles_to_test.pop(0))
    return sum(values)

def run_part_2(data):
    screen = ""
    instruction, cycle, x = 0, 1, 1
    instruction_finished = len(data[0].split(" "))
    while instruction < len(data):
        sprite = range(x-1,x+2)
        screen += "#" if ((cycle-1) % SCREEN_WIDTH) in sprite else "."
        inst = data[instruction].split(" ")
        if cycle == instruction_finished:
            if inst[0] == "addx":
                x += int(inst[1])
            instruction_finished = cycle + len(inst)
            instruction += 1
        cycle += 1

    screen_lines = [screen[i: i+40] for i in range(0, len(screen), 40)]
    for l in screen_lines: print(l) # Print the CRT screen
    return f"See Above --^"

def parse_input(data):
    return data
