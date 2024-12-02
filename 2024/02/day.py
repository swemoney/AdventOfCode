# Day 2

def run_part_1(data):
    report_safety = [is_safe(report) for report in data]
    return sum(list(map(int, report_safety)))

def run_part_2(data):
    safe_reports = 0
    for report in data:
        if is_safe(report):
            safe_reports += 1
            continue
        if is_dampened_safe(report):
            safe_reports += 1
    return safe_reports

def is_dampened_safe(report):
    for i, _ in enumerate(report):
        report_copy = report.copy()
        del report_copy[i]
        if (is_safe(report_copy)):
            return True
    return False

def is_safe(report):
    incrementing = report[0] < report[1]
    for i, curr_level in enumerate(report):
        if i == 0: continue
        prev_level = report[i-1]
        if incrementing:
            if prev_level > curr_level: return False
            diff = curr_level - prev_level
        else:
            if prev_level < curr_level: return False
            diff = prev_level - curr_level
        if diff < 1 or diff > 3: return False
    return True

def parse_input(data):
    # Each report is returned as an array of integers
    return [list(map(int, report.split())) for report in data]
