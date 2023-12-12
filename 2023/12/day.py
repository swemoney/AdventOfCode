from functools import cache

# Day 12

WORKS = "."
BROKE = "#"
UNKNOWN = "?"

def run_part_1(data):
    arrangements = [arrangement_count(line[0] + WORKS, line[1], 0, 0, 0) for line in data]
    return sum(arrangements)

def run_part_2(data):
    arrangements = [arrangement_count(UNKNOWN.join([line[0]] * 5) + WORKS, line[1] * 5, 0, 0, 0) for line in data]
    return sum(arrangements)

@cache
def arrangement_count(springs: str, records: [int], spring_idx: int, broken_idx: int, record_idx: int):

    # End of Springs
    if spring_idx == len(springs):
        arrangements = 1 if len(records) == record_idx else 0

    # Broken Spring
    elif springs[spring_idx] == BROKE:
        arrangements = arrangement_count(springs, records, spring_idx + 1, broken_idx + 1, record_idx)

    # Working Spring
    elif springs[spring_idx] == WORKS or record_idx == len(records):

        if broken_idx == 0:
            arrangements = arrangement_count(springs, records, spring_idx + 1, 0, record_idx)

        # End of current record, increment records index
        elif record_idx < len(records) and broken_idx == records[record_idx]:
            arrangements = arrangement_count(springs, records, spring_idx + 1, 0, record_idx + 1)
        
        else: arrangements = 0

    # Unknown Spring
    else:
        broken_count = arrangement_count(springs, records, spring_idx + 1, broken_idx + 1, record_idx)
        working_count = 0

        if broken_idx == 0:
            working_count = arrangement_count(springs, records, spring_idx + 1, 0, record_idx)

        # End of current record, increment records index
        elif broken_idx == records[record_idx]:
            working_count = arrangement_count(springs, records, spring_idx + 1, 0, record_idx + 1)

        arrangements = broken_count + working_count

    return arrangements

def parse_input(data):
    parsed_data = []
    for line in data:
        split_line = line.split(" ")
        parsed_data.append((split_line[0], tuple(map(int, split_line[1].split(",")))))
    return parsed_data
