# Day 3

# Differences in ASCII values and priority values for upper and lower case items
LOWER_DIFF = 96
UPPER_DIFF = 38

def calculate_score(items):
    score = sum(ord(item)-LOWER_DIFF if item.islower() else ord(item)-UPPER_DIFF for item in items)
    return score

def run_part_1(data):
    duplicates = []
    for rucksack in data:
        comp_size = len(rucksack) // 2
        comp1 = rucksack[:comp_size]
        comp2 = rucksack[comp_size:]
        dups = set(comp1) & set(comp2)
        duplicates.extend(list(dups))
    return calculate_score(duplicates)

def run_part_2(data):
    group, badges = 0, []
    while group < len(data):
        groups = data[group:group+3]
        badges.extend(list(set.intersection(*[set(list) for list in groups])))
        group += 3
    return calculate_score(badges)

def parse_input(data):
    return data
