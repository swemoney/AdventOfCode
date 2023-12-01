# Day 1

def run_part_1(data: [str]):
    vals = []
    for line in data:
        val = find_first_digit(line)
        val += find_first_digit(line[::-1])
        vals.append(int(val))
    print(len(vals))
    return sum(vals)

def run_part_2(data: [str]):
    vals = []
    for line in data:
        val = find_first_digit_or_word(line)
        print(val)
        vals.append(int(val))
    print(len(vals))
    return sum(vals)

def find_first_digit(string: str) -> str:
    for char in string:
        if char.isdigit():
            return char
    return None

def find_first_digit_or_word(string: str) -> str:
    to_find = ['0','one','two','three','four','five','six','seven','eight','nine','1','2','3','4','5','6','7','8','9']
    lowest_index = -1
    highest_index = -1
    lowest_num = ""
    highest_num = ""
    for i, num in enumerate(to_find):
        low_found = string.find(num)
        if not low_found == -1:
            if lowest_index == -1 or lowest_index >= low_found:
                lowest_index = low_found
                lowest_num = num if num.isdigit() else str(i)
        high_found = string.rfind(num)
        if not high_found == -1:
            if highest_index == -1 or highest_index <= high_found:
                highest_index = high_found
                highest_num = num if num.isdigit() else str(i)
    return lowest_num + highest_num

def replaced_digits(data: [str]) -> [str]:
    new_data = []
    replacements = {'one':'1', 'two':'2', 'three':'3', 'four':'4', 'five':'5', 'six':'6', 'seven':'7', 'eight':'8', 'nine':'9'}
    for line in data:
        new_line = line
        for num, digit in replacements.items():
            new_line = new_line.replace(num, digit)
        new_data.append(new_line)
    return new_data

def parse_input(data):
    return data
