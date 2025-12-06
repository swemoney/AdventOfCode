from math import prod

# Day 6

OPERATOR = { "+": sum, "*": prod }

def solve_column(problem):
    return OPERATOR[problem.pop(-1).strip()](list(map(int, problem)))

def run_part_1(data):
    return sum([solve_column(problem) for problem in data])

def parse_for_cephalopods(data):
    cephalopod_formatted = []

    for problem in data:
        width, cols = len(max(problem, key=len)), []
        for c in range(width):
            cols.append("".join(row[c] for row in problem[:-1]).strip())
        cols.append(problem[-1].strip())
        cephalopod_formatted.append(cols)

    return cephalopod_formatted

def run_part_2(data):
    return sum([solve_column(problem) for problem in parse_for_cephalopods(data)])

def parse_input(data):
    data = [r + " " for r in data] # Adding a space to each line makes the last column easier to parse
    problems = []

    i = 0
    while i < len(max(data, key=len)):

        end_of_col = i
        for row in data[:-1]:

            next_space = row[i:].find(" ")
            if next_space + i > end_of_col:
                end_of_col = next_space + i

        problems.append([r[i:end_of_col] for r in data])
        i = end_of_col + 1

    return problems
