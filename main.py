from importlib import import_module
import datetime
import time

YEAR = 2022
DAY = 1
PART = 1

def file_not_found(filename):
    print(f"Could not locate {filename}")
    print(f"Make sure it's present at ./{2022}/{DAY:02}/{filename}")
    exit()

try:
    puzzle = import_module(f"{YEAR}.{DAY:02}.part{PART}")
except ImportError:
    file_not_found(f"part{PART}.py")
    
try:
    with open(f"{YEAR}/{DAY:02}/input.txt") as f:
        input_data = [l.rstrip('\n') for l in f.readlines()]
        data = puzzle.parse_input(input_data)
except FileNotFoundError:
    file_not_found("input.txt")

print(f"Running day {DAY}, part {PART}...", end=" ")

start_time = time.time()
result = puzzle.run(data)
end_time = time.time()

print(f"Completed in {(end_time - start_time):0.5f} seconds\n")
print(f"  - Result: {result}\n")