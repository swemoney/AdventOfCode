from itertools import product
from tqdm import tqdm

# Day 7

P1_OPS = ["*","+"]
P2_OPS = ["*","+","||"]

def run_part_1(data):
    true_calibrations = [calibration[0] for calibration in data if is_true_calibration(calibration, P1_OPS)]
    return sum(true_calibrations)

def run_part_2(data): # ~4 minutes to brute force this. I don't have the time to refactor it. It still works!
    true_calibrations = []
    for calibration in tqdm(data, position=0, leave=True, desc="Calibrations"):
        if is_true_calibration(calibration, P2_OPS):
            true_calibrations.append(calibration[0])
    return sum(true_calibrations)

def is_true_calibration(calibration, possible_ops):
    num_ops = len(calibration[1]) - 1
    op_combos = list(product(possible_ops, repeat=num_ops))
    for ops in tqdm(op_combos, position=1, leave=False, desc="Operators"):
        nums = calibration[1].copy()
        for i, op in enumerate(ops):
            if op == "||":
                nums[i+1] = int(f"{nums[i]}{nums[i+1]}")
            else:
                eq = f"{nums[i]} {op} {nums[i+1]}"
                nums[i+1] = eval(eq)
            if nums[i+1] > calibration[0]: break
        if nums[-1] == calibration[0]:
            return True

def parse_input(data):
    ret = []
    for line in data:
        line_data = line.split(": ")
        ret.append((int(line_data[0]), list(map(int, line_data[1].split(" ")))))
    return ret
