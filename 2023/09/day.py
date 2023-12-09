# Day 9

def run_part_1(data):
    predictions = 0
    for history in data:
        diffs = find_history_diffs(history)
        predictions += calculate_prediction(diffs, in_the_past=False)
    return predictions

def run_part_2(data):
    predictions = 0
    for history in data:
        diffs = find_history_diffs(history)
        predictions += calculate_prediction(diffs, in_the_past=True)
    return predictions

def find_history_diffs(history: [int]) -> [[int]]:
    diffs = [history]
    while not is_all_zeros(diffs):
        diffs.append([j - i for i, j in zip(diffs[-1][:-1], diffs[-1][1:])])
    diffs.reverse()
    return diffs

def is_all_zeros(diffs: [[int]]) -> bool:
    return len(set(diffs[-1])) == 1 and diffs[-1][0] == 0

def calculate_prediction(diffs: [[int]], in_the_past: bool) -> int:
    for i, diff in enumerate(diffs):
        if i+1 == len(diffs): continue
        diffs[i+1].append(diffs[i+1][0] - diff[-1] if in_the_past else diff[-1] + diffs[i+1][-1])
    return diffs[-1][-1]

def parse_input(data):
    return [list(map(int, history.split(" "))) for history in data]
