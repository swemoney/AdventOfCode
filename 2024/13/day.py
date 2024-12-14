from utils import Vector2
from itertools import combinations
import re

# Day 13

PRESS_COST = Vector2(3, 1)

def run_part_1(data):
    machine_costs = [find_solution_with_maths(machine) for machine in data]
    return sum(machine_costs)

def run_part_2(data):
    machine_costs = [find_solution_with_maths(machine, offset=10000000000000) for machine in data]
    return sum(machine_costs)

def find_solution_with_maths(machine, offset=0):
    a, b, p = machine
    p = p + Vector2(offset, offset)
    num_presses_a, num_presses_b = None, None

    # I guess linear algebra > brute force. I need to go back to high school.
    bp = (b.x * p.y - b.y * p.x)
    ba = (b.x * a.y - b.y * a.x)
    if (bp / ba) == (bp // ba): # This should make sure we have an integer solution
        num_presses_a = bp // ba 
        pa = (p.y - num_presses_a * a.y)
        if (pa / b.y) == (pa // b.y):
            num_presses_b = (pa // b.y)
    if None not in [num_presses_a, num_presses_b]:
        return num_presses_a * 3 + num_presses_b
    
    return 0

# Brute force took 3.7 seconds for part 1. Didn't even attempt it for part 2.
def find_wins(machine, max_presses=100):
    wins = []
    for a in range(max_presses):
        for b in range(max_presses):
            loc_a = Vector2(machine[0].x * a, machine[0].y * a)
            loc_b = Vector2(machine[1].x * b, machine[1].y * b)
            if (loc_a + loc_b) != machine[2]: continue
            wins.append(Vector2(a, b))
    return wins

def win_cost(presses):
    return presses * PRESS_COST

# Return the data as 3 vector2 objects. (button_a, button_b, prize_location)
def parse_input(data):
    data.append("")
    xy_re = re.compile(r"X[\+\=](\d+)\,\sY[\+\=](\d+)")

    machines = []
    for idx, line in enumerate(data):
        if line != "": continue
        machine = []
        for i in range(3, 0, -1):
            m = xy_re.search(data[idx-i])
            machine.append(Vector2(int(m.group(1)), int(m.group(2))))
        machines.append(machine)
    return tuple(machines)
