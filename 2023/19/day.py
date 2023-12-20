import re
from collections import namedtuple
from operator import lt, gt

# Day 19

rules_re = re.compile(r"(.+){(.+)}")
rule_re  = re.compile(r"(.+)([><]){1}(.+):(.+)")
parts_re = re.compile(r"([^=]+)=([^=]+)(?:,|$)")

Rule = namedtuple("Rule", ["cat","op","val","dest"])

OPS = {">": gt, "<": lt}

ACCEPT = "A"
REJECT = "R"
START_WORKFLOW = "in"
LT = "<"
GT = ">"

def run_part_1(data):
    accepted = evaluate_parts(*data)
    val = 0
    for part in accepted:
        val += part["x"] + part["m"] + part["a"] + part["s"]
    return val

def run_part_2(data):
    rules, _ = data
    part = {"x": [1,4000], "m": [1,4000], "a": [1,4000], "s": [1,4000]}
    return narrow_ranges(part, rules, START_WORKFLOW)

# Part 2 Stuff
def narrow_ranges(part, rules, workflow):
    accepted = 0

    for rule in rules[workflow]:
        if type(rule) is str:
            accepted += check_destination(part, rules, rule)
            continue

        if OPS[rule.op](part[rule.cat][0], int(rule.val)) and OPS[rule.op](part[rule.cat][1], int(rule.val)):
            accepted += check_destination(part, rules, rule.dest)
            break

        if (rule.op == LT and part[rule.cat][0] >= int(rule.val) and part[rule.cat][1] >= int(rule.val)) or \
           (rule.op == GT and part[rule.cat][0] <= int(rule.val) and part[rule.cat][1] <= int(rule.val)):
            continue

        modified = part.copy()
        if rule.op == LT: 
            modified[rule.cat] = [part[rule.cat][0], int(rule.val) - 1]
            part[rule.cat] = [int(rule.val), part[rule.cat][1]]
        else: 
            modified[rule.cat] = [int(rule.val) + 1, part[rule.cat][1]]
            part[rule.cat] = [part[rule.cat][0], int(rule.val)]

        accepted += check_destination(modified, rules, rule.dest)
    return accepted

def check_destination(part, rules, dest):
    if dest == ACCEPT:
        return (part["x"][1] - part["x"][0] + 1) * (part["m"][1] - part["m"][0] + 1) * \
               (part["a"][1] - part["a"][0] + 1) * (part["s"][1] - part["s"][0] + 1)
    if dest == REJECT:
        return 0
    return narrow_ranges(part, rules, dest)


# Part 1 Stuff
def evaluate_parts(rules, parts):
    return [part for part in parts if is_accepted(part, rules, START_WORKFLOW)]

def is_accepted(part, rules, workflow) -> bool:
    for rule in rules[workflow]:
        if type(rule) is str:
            return check_accepted(part, rules, rule)
        if OPS[rule.op](part[rule.cat], int(rule.val)):
            return check_accepted(part, rules, rule.dest)
            
def check_accepted(part, rules, dest) -> bool:
    if dest == ACCEPT:
        return True
    if dest == REJECT:
        return False
    return is_accepted(part, rules, dest)


# Input Parsing
def parse_input(data):
    rules = {}
    parts = []
    
    done_with_rules = False
    for line in data:
        if line == "":
            done_with_rules = True
            continue

        if done_with_rules:
            parts.append({category: int(rating) for category, rating in parts_re.findall(line.strip("{}"))})
            continue

        rule_list = []
        rule_name, rule_str = rules_re.findall(line)[0]
        for rule in rule_str.split(","):
            if not ":" in rule: rule_list.append(rule)
            else: rule_list.append(Rule(*rule_re.findall(rule)[0]))
        rules[rule_name] = rule_list

    return (rules, parts)
