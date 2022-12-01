# Day 1

def calories_carried_by_each_elf(data):
    elves = [0]
    for calories in data:
        if calories == '':
            elves.append(0)
            continue
        elves[-1] += int(calories)
    return elves

def run_part_1(data):
    elves = calories_carried_by_each_elf(data)
    return max(elves)

def run_part_2(data):
    elves = calories_carried_by_each_elf(data)
    return sum(sorted(elves)[-3:])

def parse_input(data):
    return data
