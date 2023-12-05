import re

# Day 5

re_num = re.compile(r"(\d+)")

# part 1
def run_part_1(data):
    seeds, maps = data
    locations = find_seed_locations(seeds, maps)
    return min(locations.values())

def find_seed_locations(seeds, maps):
    locations = {}
    for seed in seeds:
        num = seed
        for map in maps.values():
            num = find_in_map(map, num)
        locations[seed] = num
    return locations

def find_in_map(map, num):
    for src, dest, length in map:
        src_range = range(src, src + length)
        if num in src_range:
            diff = num - src
            return dest + diff
    return num

# part 2
def run_part_2(data):
    seeds, maps = data
    seed_ranges = [(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]

    for map in maps.values():
        seed_ranges_mapped = []

        while seed_ranges:
            seed_start, seed_end = seed_ranges.pop()
            mapped = False

            for src, dest, length in map:
                overlap_start = max(seed_start, src)
                overlap_end = min(seed_end, src + length)
                if overlap_start < overlap_end:
                    seed_ranges_mapped.append((overlap_start - src + dest, overlap_end - src + dest))

                    if seed_start < overlap_start:
                        seed_ranges.append((seed_start, overlap_start))
                    if overlap_end < seed_end:
                        seed_ranges.append((overlap_end, seed_end))
                    
                    mapped = True
                    break
            
            if not mapped:
                seed_ranges_mapped.append((seed_start, seed_end))

        seed_ranges = seed_ranges_mapped

    return min(seed_ranges_mapped)[0]

def parse_input(data):
    d = {}
    current_map = ""
    for line in data:
        if line.find("seeds:") != -1:
            seeds = [int(num) for num in re_num.findall(line)]
            continue

        if line.find("map:") != -1:
            current_map = line.split(" ")[0]
            d[current_map] = []
            continue

        if line == "": continue

        dest_start, src_start, length = [int(num) for num in line.split(" ")]
        d[current_map].append((src_start, dest_start, length)) # makes more sense to have the source first to me
    return (seeds, d)
