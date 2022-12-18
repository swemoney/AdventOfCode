# Day 16

import re

class Valve:
    def __init__(self, name, rate, neighbors):
        self.name = name
        self.rate = int(rate)
        self.neighbors = neighbors

def travel(valves, steps, prev_valve, time_remaining, states, state, flow, result):
    result[state] = max(result.get(state, 0), flow)
    for valve in valves:
        minutes = time_remaining - steps[prev_valve][valve] - 1
        if (states[valve] & state) or (minutes <=0): continue
        travel(valves, steps, valve, minutes, states, state | states[valve], 
                      flow + (minutes * valves[valve].rate), result)
    return result

def run_part_1(data):
    valves, valve_open_states, steps = data
    return max(travel(valves, steps, "AA", 30, valve_open_states, 0, 0, {}).values())

def run_part_2(data):
    valves, valve_open_states, steps = data
    paths = travel(valves, steps, "AA", 26, valve_open_states, 0, 0, {})
    pressure_released = [my_pressure + elephant_pressure for my_steps, my_pressure in paths.items() 
                    for elephant_steps, elephant_pressure in paths.items() if not my_steps & elephant_steps]
    return max(pressure_released)

def parse_input(data):
    valves = {}
    for line in data:
        m = re.match("^Valve (.+) has.*=(\d+);.*valves? (.+)$", line)
        valves[m.group(1)] = Valve(m.group(1), m.group(2), m.group(3).split(", "))
    
    steps = {x:{y:1 if y in valves[x].neighbors else float('inf') for y in valves} for x in valves}
    for x in steps: # Floyd-Warshall
        for y in steps:
            for z in steps:
                steps[y][z] = min(steps[y][z], steps[y][x] + steps[x][z])

    valves_with_flow = {name: valve for (name, valve) in valves.items() if valve.rate > 0}
    valve_open_states = {v: 1 << i for i, v in enumerate(valves)}
    return valves_with_flow, valve_open_states, steps























# def dfs(rates, neighbors, pos, pressure_inc, valves_open, time_remaining):
#     if time_remaining <= 0: return 0
#     valves_open_key = ".".join(sorted(valves_open))
#     cached_score = CACHE.get((pos, valves_open_key, time_remaining))
#     if cached_score: return cached_score
    
#     stk = []
#     for prev_pos in pos:
#         if prev_pos:
#             tmp = [(neighbor_pos, 0, set()) for neighbor_pos in neighbors[prev_pos]]
#         else:
#             tmp = [(prev_pos, 0, set())]
#         if prev_pos and rates[prev_pos] > 0 and prev_pos not in valves_open:
#             tmp += [(prev_pos, rates[prev_pos], {prev_pos})]
#         stk.append(tmp)

#     score = 0
#     for pos0, pressure_inc0, neighbor_valve0 in stk[0]:
#         for pos1, pressure_inc1, neighbor_valve1 in stk[1]:
#             if neighbor_valve0 and neighbor_valve1 and neighbor_valve0 == neighbor_valve1:
#                 continue
#             score = max(score, dfs(rates, neighbors, (pos0, pos1),
#                                     pressure_inc + pressure_inc0 + pressure_inc1,
#                                     valves_open | neighbor_valve0 | neighbor_valve1,
#                                     time_remaining - 1))
#     score += pressure_inc
#     CACHE[(pos, valves_open_key, time_remaining)] = score
#     return score

# def run_part_1(data):
#     PROGRESS["iterations"] = 0
#     cache = {}
#     rates, neighbors = data
#     pressure = dfs(rates, neighbors, ("AA", None), 0, set(), 30)
#     print("\n\n")
#     return pressure

# def run_part_2(data):
#     PROGRESS["iterations"] = 0
#     cache = {}
#     rates, neighbors = data
#     pressure = dfs(rates, neighbors, ("AA", "AA"), 0, set(), 26)
#     print("\n\n")
#     return pressure

# def parse_input(data):
#     rates, neighbors = {}, {}
#     for line in data:
#         m = re.match("^Valve (.+) has.*=(\d+);.*valves? (.+)$", line)
#         rates[m.group(1)] = int(m.group(2))
#         neighbors[m.group(1)] = m.group(3).split(", ")
#     return rates, neighbors




# R, N = {},{}
# for l in open(0).read().splitlines():
#     valve = l[6:8]
#     rate, ns = l[23:].split(';')
#     R[valve] = int(rate)
#     N[valve] = ''.join(ns.split()[4:]).split(',')

# cache = {}
# def dfs(pos, per_min, open_valves, mins_left):
#     if mins_left <= 0: 
#         return 0
#     vs = '.'.join(sorted(open_valves))
#     cached_score = cache.get((pos, vs, mins_left), -1)
#     if cached_score >= 0:
#         return cached_score
#     st = [([(npos, 0, set()) for npos in N[ppos]] if ppos else [(ppos, 0, set())])
#           + ([(ppos, R[ppos], {ppos})] if ppos and R[ppos] > 0 and ppos not in open_valves else [])
#           for ppos in pos]
#     score = 0
#     for pos0, per_min0, nvalve0 in st[0]:
#         for pos1, per_min1, nvalve1 in st[1]:
#             if nvalve0 and nvalve1 and nvalve0 == nvalve1:
#                 continue
#             score = max(score, dfs((pos0, pos1),
#                                    per_min+per_min0+per_min1,
#                                    open_valves | nvalve0 | nvalve1,
#                                    mins_left-1))
#     score += per_min
#     cache[(pos, vs, mins_left)] = score
#     return score

# print ('Part1: ', dfs(('AA', None), 0, set(), 30))
# print ('Part2:', dfs(('AA', 'AA'), 0, set(), 26))

