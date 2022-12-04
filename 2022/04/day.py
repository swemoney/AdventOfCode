# Day 4

def ranges_overlap(rng1, rng2, entirely=False):
    set1, set2 = set(rng1), set(rng2)
    set_overlap = set1 & set2
    if entirely == False:
        return len(set_overlap) > 0
    if set1 == set_overlap or set2 == set_overlap:
        return True
    return False

def number_of_overlapping_sections(data, entirely=False):
    overlaps = 0
    for pair in data:
        if ranges_overlap(pair[0], pair[1], entirely=entirely):
            overlaps += 1
    return overlaps

def run_part_1(data):
    return number_of_overlapping_sections(data, entirely=True)

def run_part_2(data):
    return number_of_overlapping_sections(data, entirely=False)

# Convert the string representations of each pair into ranges
def parse_input(data):
    pairs = []
    for pair_raw in data:
        pair = []
        elves_raw = pair_raw.split(",")
        for elf_raw in elves_raw:
            sections = [int(section) for section in elf_raw.split("-")]
            pair.append(range(sections[0], sections[1] + 1)) # Python range stops aren't inclusive
        pairs.append(pair)
    return pairs
