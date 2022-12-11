# Day 11

from copy import deepcopy
from math import prod, lcm

def simulate_monkeys(data, rounds=20, worry_reduction=3):
    monkeys = deepcopy(data)
    limit = lcm(*[m["test"] for m in monkeys]) # The secret sauce
    for _ in range(rounds):
        for monkey in monkeys:
            for worry in monkey["items"]:
                monkey["inspections"] += 1
                op = monkey["operation"].replace("old",str(worry))
                worry = eval(op) // worry_reduction % limit
                if worry % monkey["test"] == 0:
                    monkeys[monkey["true"]]["items"].append(worry)
                else:
                    monkeys[monkey["false"]]["items"].append(worry)
            monkey["items"] = []
    return monkeys

def calculate_monkey_activity(monkeys, num_monkeys=2):
    top_monkeys = sorted(monkeys, key=lambda m: m["inspections"])[-num_monkeys:]
    return prod([m["inspections"] for m in top_monkeys])

def run_part_1(data):
    monkeys = simulate_monkeys(data, rounds=20, worry_reduction=3)
    return calculate_monkey_activity(monkeys, num_monkeys=2)

def run_part_2(data):
    monkeys = simulate_monkeys(data, rounds=10000, worry_reduction=1)
    return calculate_monkey_activity(monkeys, num_monkeys=2)

def parse_input(data):
    monkeys = []
    for line in data:
        if line == "": continue
        if line.split(" ")[0] == "Monkey": 
            monkeys.append({"inspections":0})
            continue
        
        param, args = line.split(":")
        if param.strip() == "Starting items":
            monkeys[-1]["items"] = [int(arg) for arg in args.split(",")]
        if param.strip() == "Operation":
            monkeys[-1]["operation"] = args.split("= ")[1]
        if param.strip() == "Test":
            monkeys[-1]["test"] = int(args.split("by ")[1])
        if param.strip() == "If true":
            monkeys[-1]["true"] = int(args.split("monkey ")[1])
        if param.strip() == "If false":
            monkeys[-1]["false"] = int(args.split("monkey ")[1])
    return monkeys
