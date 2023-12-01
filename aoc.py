from importlib import import_module
from pathlib import Path
from datetime import datetime
from pytz import timezone
import time
import argparse

try:
    from aocd.models import Puzzle
except:
    print("AOCD Not Found: https://github.com/wimglenn/advent-of-code-data")
    exit()

parser = argparse.ArgumentParser(description="Advent of Code Runner")
parser.add_argument('-d', '--day', type=int, help="Day of challenge")
parser.add_argument('-y', '--year', type=int, help="Year of challenge")
parser.add_argument('-c', '--create', action="store_true", help="Create template")
parser.add_argument('-t', '--test', action="store_true", help="Run against test data")
args = parser.parse_args()

# Use today's day/year if none is supplied
now = datetime.now(timezone('EST'))
DAY = args.day or now.day
YEAR = args.year or now.year
year_dir = Path(f"{YEAR}")
day_dir = Path(year_dir, f"{DAY:02}")

def create_new_day():
    print(f"Creating Advent of Code template for day {DAY:01} of {YEAR}...")
    print(f" * Fetching puzzle data from adventofcode.com")
    aocd = Puzzle(day=DAY, year=YEAR)
    DAY_FILE = f"# Day {DAY}\n\ndef run_part_1(data):\n    return \"N/A\"\n\ndef run_part_2(data):\n    return \"N/A\"\n\ndef parse_input(data):\n    return data\n"
    README_FILE = f"# Day {DAY} ({YEAR})\n\n`{aocd.title}` [prompt](https://adventofcode.com/{YEAR}/day/{DAY})\n\n## Part 1\n\n## Part 2"

    print(f" * Creating directory: {day_dir}")
    day_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(day_dir, "input.txt")
    if not input_path.exists():
        print(" * Creating input.txt")
        input_path.write_text(aocd.input_data)

    for i, example in enumerate(aocd.examples):
        test_input_path = Path(day_dir, f"input.test{i+1}.txt")
        print(f" * Creating example input {i+1}")
        test_input_path.write_text(aocd.examples[i].input_data)

    test_input_path = Path(day_dir, "input.test2.txt")
    if not test_input_path.exists():
        test_input_path.touch()

    day_file_path = Path(day_dir, "day.py")
    if not day_file_path.exists():
        print(" * Creating day.py")
        day_file_path.write_text(DAY_FILE)
    else:
        print(" * day.py already exists (skipping)")
    
    readme_file_path = Path(day_dir, "README.md")
    if not readme_file_path.exists():
        print(" * Creating README.md")
        readme_file_path.write_text(README_FILE)
    else:
        print(" * README.md already exists (skipping)")

# Create a new day from templates and quit
if args.create:
    create_new_day()
    exit()

if not Path(day_dir, "day.py").exists():
    create_new_day()

puzzle = import_module(f"{YEAR}.{DAY:02}.day")

if args.test:
    with open(Path(day_dir, "input.test1.txt")) as f:
        test_input_1 = [l.rstrip('\n') for l in f.readlines()]
    with open(Path(day_dir, "input.test2.txt")) as f:
        test_input_2 = [l.rstrip('\n') for l in f.readlines()]
    test_data_1 = puzzle.parse_input(test_input_1)
    test_data_2 = puzzle.parse_input(test_input_2)
    print(f"Running Day {DAY} Puzzle Examples...\n")
    result1 = getattr(puzzle, f"run_part_1")(test_data_1)
    result2 = getattr(puzzle, f"run_part_2")(test_data_2)
    print(f"(example) Part 1: {result1}")
    print(f"(example) Part 2: {result2}")
    exit()

with open(Path(day_dir, "input.txt")) as f:
    input_data = [l.rstrip('\n') for l in f.readlines()]
    data = puzzle.parse_input(input_data)

print(f"Running Day {DAY} Puzzles...\n")
start_time1 = time.time()
result1 = getattr(puzzle, f"run_part_1")(data)
end_time1 = time.time()
start_time2 = time.time()
result2 = getattr(puzzle, f"run_part_2")(data)
end_time2 = time.time()

res1_str = f"({(end_time1 - start_time1)*1000:0.2f}ms) Part 1: {result1}"
res2_str = f"({(end_time2 - start_time2)*1000:0.2f}ms) Part 2: {result2}"
tag_size = max(len(res1_str), len(res2_str)) + 2
res_decoration = (
    r"                 ." + f"{'='*tag_size}.\n"
    r"       .__.      [ " + f"{res1_str.ljust(tag_size-2, ' ')} ]\n"
    r"     .(\\//).  .-[ " + f"{res2_str.ljust(tag_size-2, ' ')} ]\n"
    r"    .(\\()//)./  '" + f"{'='*tag_size}'\n"
    r".----(\)\/(/)----." + "\n"
    r"|     ///\\\     |" + "\n"
    r"|    ///||\\\    |" + "\n"
    r"|   //`||||`\\   |" + "\n"
    r"|      ||||      |" + "\n"
    r"|      ||||      |" + "\n"
    r"'------====------'" + "\n"
)
print(res_decoration)