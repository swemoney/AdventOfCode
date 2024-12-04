import re

# Day 3

MUL = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
DONT = re.compile(r"don\'t\(\)")
DO = re.compile(r"do\(\)")

def run_part_1(data):
    muls = MUL.findall(data)
    prods = [int(m[0]) * int(m[1]) for m in muls]
    return sum(prods)

def run_part_2(data):
    muls = list(MUL.finditer(data))
    donts = list(DONT.finditer(data))
    dos = list(DO.finditer(data))

    curr_mul, curr_dont, curr_do = 0, 0, 0
    valid_muls = []

    dont = False
    while curr_mul <= len(muls) - 1:
        mul_pos = muls[curr_mul].span()[0]
        dont_pos = donts[curr_dont].span()[0]
        do_pos = dos[curr_do].span()[0]

        if mul_pos > dont_pos:
            dont = True
            curr_dont = min(curr_dont + 1, len(donts) - 1)

        if mul_pos > do_pos:
            dont = False
            curr_do = min(curr_do + 1, len(dos) - 1)

        if dont == False:
            valid_muls.append(muls[curr_mul])

        curr_mul += 1
    
    prods = [int(m.group(1)) * int(m.group(2)) for m in valid_muls]
    return sum(prods)

def parse_input(data):
    return "".join(data)
