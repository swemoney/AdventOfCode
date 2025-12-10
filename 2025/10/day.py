from typing import NamedTuple
from collections import deque
from z3 import Int, Optimize, sat
import re

class MachineSpecs(NamedTuple):
    lights: list[bool]
    buttons: list[list[int]]
    joltage: list[int]

# Day 10

# Part 1 Stuff (BFS with bitmasks)

def target_mask_from_lights(lights: list[bool]) -> int:
    return int(f"0b{"".join([str(int(l)) for l in reversed(lights)])}", 2)

def masks_from_buttons(buttons: list[list[int]]) -> list[int]:
    return [sum(1 << i for i in button) for button in buttons]

def presses_bfs(target_lights: list[bool], buttons: list[list[int]]):
    num_lights = len(target_lights)
    max_state = 1 << num_lights

    start_mask = 0
    target_mask = target_mask_from_lights(target_lights)
    button_masks = masks_from_buttons(buttons)

    visited = [-1] * max_state
    prev = [None] * max_state

    q = deque([start_mask])
    visited[start_mask] = 0

    while q:
        state = q.popleft()

        if state == target_mask:
            sequence = []
            current = state
            while prev[current] is not None:
                prev_state, button_idx = prev[current]
                sequence.append(button_idx)
                current = prev_state
            return visited[state], reversed(sequence)
        
        for i, mask in enumerate(button_masks):
            next_state = state ^ mask
            if visited[next_state] == -1:
                visited[next_state] = visited[state] + 1
                prev[next_state] = (state, i)
                q.append(next_state)

    return None, None

def run_part_1(data: list[MachineSpecs]):
    return sum(presses_bfs(machine.lights, machine.buttons)[0] for machine in data)

# Part 2 Stuff (Z3)

def presses_z3(buttons, target):
    num_buttons = len(buttons)

    presses = [Int(f"p{i}") for i in range(num_buttons)]
    
    s = Optimize()
    
    for p in presses:
        s.add(p >= 0)

    for counter_idx, t in enumerate(target):
        expr = 0
        for button_idx, button in enumerate(buttons):
            if counter_idx in button:
                expr += presses[button_idx]
        s.add(expr == t)

    s.minimize(sum(presses))

    if s.check() != sat:
        return None
    
    model = s.model()
    return sum([model[p].as_long() for p in presses])

def run_part_2(data: list[MachineSpecs]):
    return sum(presses_z3(machine.buttons, machine.joltage) for machine in data)

def parse_input(data):
    machine_parts_re = re.compile(r'\[(.*?)\]\s*((?:\([^()]*\)\s*)+)\{(.*?)\}')
    
    machines = []
    for line in data:
        m = machine_parts_re.search(line)
        lights = [light == "#" for light in m.group(1)]
        buttons = [list(map(int, button.split(","))) for button in m.group(2).replace("(","").replace(")","").split()]
        joltage = list(map(int, m.group(3).split(",")))
        machines.append(MachineSpecs(lights, buttons, joltage))
    return machines
