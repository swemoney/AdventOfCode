# Day 5

def run_part_1(data):
    rules, updates = data
    valid_updates = [update for update in updates if update_is_valid(update, rules)]
    middles = [middle_item(update) for update in valid_updates]
    return sum(middles)

def run_part_2(data):
    rules, updates = data
    invalid_updates = [update for update in updates if not update_is_valid(update, rules)]
    for update in invalid_updates:
        while not update_is_valid(update, rules):
            fix_update(update, rules)
    middles = [middle_item(update) for update in invalid_updates]
    return sum(middles)

def update_is_valid(update, rules) -> bool:
    for rule in rules:
        if not pages_exist_for_rule(update, rule): continue
        if breaks_rule(update, rule): return False
    return True

def fix_update(update, rules) -> list[int]:
    for rule in rules:
        if not pages_exist_for_rule(update, rule): continue
        if breaks_rule(update, rule):
            before = update.index(rule[1])
            after = update.index(rule[0])
            update[before], update[after] = rule[0], rule[1]
            break
    return update

def breaks_rule(update, rule) -> bool:
    return update.index(rule[0]) > update.index(rule[1])

def pages_exist_for_rule(update, rule) -> bool:
    return (rule[0] in update) and (rule[1] in update)

def middle_item(update) -> int:
    return update[len(update)//2]

def parse_input(data) -> tuple[list[int], list[int]]:
    rules, updates = [], []
    for line in data:
        if "|" in line: # Rule
            rules.append(list(map(int, line.split("|"))))
        elif "," in line: # update
            updates.append(list(map(int, line.split(","))))
    return (rules, updates)
