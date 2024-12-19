from functools import cache
# Day 19

def run_part_1(data):
    towels, designs = data
    counts = [find_arrangements(design, towels) for design in designs]
    return sum([count != 0 for count in counts])

def run_part_2(data):
    towels, designs = data
    counts = [find_arrangements(design, towels) for design in designs]
    return sum(counts)

@cache
def find_arrangements(design, towels):
    if len(design) == 0: return 1
    count = 0
    for towel in towels:
        if not design.startswith(towel): continue
        count += find_arrangements(design[len(towel):], towels)
    return count

def parse_input(data) -> tuple[tuple[str], tuple[str]]:
    return (tuple(data[0].split(", ")), tuple([line for line in data[2:]]))
