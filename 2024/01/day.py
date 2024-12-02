from collections import Counter

# Day 1

def run_part_1(data):
    sorted_data = [sorted(ids) for ids in data]
    diffs = [abs(sorted_data[0][i] - sorted_data[1][i]) for i, _ in enumerate(sorted_data[0])]
    return sum(diffs)

def run_part_2(data):
    counts = Counter(data[1])
    similarity_scores = [id * counts.get(id, 0) for id in data[0]]
    return sum(similarity_scores)

def parse_input(data):
    # Split each line and return them as 2 lists
    return list(zip(*(list(map(int, id.split())) for id in data)))
