from copy import deepcopy

# Day 13

def run_part_1(data):
    reflections = [line_of_reflection(pattern) for pattern in data]
    return sum(reflections)

def run_part_2(data):
    h_reflections = [line_of_reflection_with_smudges(pattern, 1) for pattern in data]
    v_reflections = [line_of_reflection_with_smudges(pattern_cols(pattern), 1) for pattern in data]
    return (sum(h_reflections) * 100) + sum(v_reflections)

def line_of_reflection_with_smudges(pattern: [str], num_of_smudges: int) -> int:
    for line in range(1, len(pattern)):
        lhs = reversed(pattern[:line])
        rhs = pattern[line:]
        smudges_found = 0
        for a, b, in zip(lhs, rhs):
            for c1, c2 in zip(a, b):
                if c1 != c2: 
                    smudges_found += 1
        if smudges_found == num_of_smudges: return line
    return 0
                
def pattern_cols(pattern):
    return ["".join([row[i] for row in pattern]) for i in range(len(pattern[0]))]

def parse_input(data):
    patterns, curr_pattern = [], []
    for i, line in enumerate(data):
        if line == "" or i == len(data) - 1:
            patterns.append(list(curr_pattern))
            curr_pattern.clear()
            continue
        curr_pattern.append(line)
    return patterns

# v-- Naive part 1 code I did away with for the tiny code above --v
def line_of_reflection(pattern: [str]):
    pattern_vert = pattern_cols(pattern)
    potential_h_reflections = find_potential_reflections(pattern)
    potential_v_reflections = find_potential_reflections(pattern_vert)
    for i in potential_h_reflections:
        if test_full_reflection(pattern, i):
            return (i + 1) * 100
    for i in potential_v_reflections:
        if test_full_reflection(pattern_vert, i):
            return (i + 1)
    return 0

def test_full_reflection(pattern: [str], idx: int) -> False:
        j = 0
        search_rng, backwards = search_range(pattern, idx)
        for i in search_rng:
            other_i = idx - j 
            if backwards: other_i = idx + 1 + j
            if not pattern[i] == pattern[other_i]:
                return False
            j += 1
        return True

def search_range(pattern: [str], idx: int) -> (range, bool):
    if idx + 1 < len(pattern) / 2:
        return (range(idx, -1, -1), True)
    else:
        return (range(idx + 1, len(pattern)), False)

def find_potential_reflections(lines: [str]) -> [int]:
    potential_reflections = []
    for i, line in enumerate(lines):
        if i + 1 == len(lines): break
        if line == lines[i + 1]:
            potential_reflections.append(i)
    return potential_reflections
