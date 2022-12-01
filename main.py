from importlib import import_module
import datetime
import time

YEAR = 2022
DAY = 1

def file_not_found(filename):
    print(f"Could not locate {filename}")
    print(f"Make sure it's present at ./{2022}/{DAY:02}/{filename}")
    exit()

try:
    puzzle = import_module(f"{YEAR}.{DAY:02}.day")
except ImportError:
    file_not_found(f"day.py")
    
try:
    with open(f"{YEAR}/{DAY:02}/input.txt") as f:
        input_data = [l.rstrip('\n') for l in f.readlines()]
        data = puzzle.parse_input(input_data)
except FileNotFoundError:
    file_not_found("input.txt")

print(f"Running day {DAY}, part 1...", end=" ")
start_time = time.time()
result1 = getattr(puzzle, f"run_part_1")(data)
end_time = time.time()
print(f"Completed in {(end_time - start_time):0.5f} seconds")
print(f"Running day {DAY}, part 2...", end=" ")
start_time = time.time()
result2 = getattr(puzzle, f"run_part_2")(data)
end_time = time.time()
print(f"Completed in {(end_time - start_time):0.5f} seconds")

res1_str = f"Part 1: {result1}"
res2_str = f"Part 2: {result2}"
tag_size = max(len(res1_str), len(res2_str)) + 2
res_decoration = (
    f"        .__.        .{'='*tag_size}.\n"
    f"      .(\\\\//).  .---[ {res1_str.ljust(tag_size-2, ' ')} ]\n"
    f"     .(\\\\()//)./    [ {res2_str.ljust(tag_size-2, ' ')} ]\n"
    f" .----(\)\/(/)----. '{'='*tag_size}'\n"
    f" |     ///\\\\\     |\n"
    f" |    ///||\\\\\    |\n"
    f" |   //`||||`\\\\   |\n"
    f" |      ||||      |\n"
    f" '------====------'   Happy Christmas!\n"
)
print(res_decoration)