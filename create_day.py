import sys
import os

YEAR = 2022

DAY_FILE_TEMPLATE = """# Day {day}

def run_part_1(data):
    return "N/A"

def run_part_2(data):
    return "N/A"

def parse_input(data):
    return data
"""

def argument_error(desc):
    print(desc)
    exit()

def create_folder(day):
    path = f"{YEAR}/{day:02}"
    if os.path.exists(path):
        return False

    os.mkdir(path)
    return True

def create_files(day):
    path = f"{YEAR}/{day:02}"
    input_file = open(f"{path}/input.txt", "x")
    input_file.close()

    day_file = open(f"{path}/day.py", "w")
    day_file.write(DAY_FILE_TEMPLATE.replace("{day}", f"{day}"))
    day_file.close()

def main():
    try:
        day_num = int(sys.argv[1])
    except ValueError:
        argument_error(f"Invalid day: {sys.argv[1]}")

    if day_num < 1 or day_num > 25:
        argument_error(f"Day number out of range: {day_num}")

    if create_folder(day_num):
        create_files(day_num)
    else:
        argument_error(f"That day already exists: {day_num}")

if __name__ == "__main__":
    main()