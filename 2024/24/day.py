from enum import Enum
from typing import NamedTuple, Optional

# Day 24

class GateType(Enum):
    AND = "AND"
    OR = "OR"
    XOR = "XOR"

class Gate(NamedTuple):
    type: GateType
    input_a: str
    input_b: str
    output_wire: str
    
type Wires = dict[str, Optional[int]]
type Gates = dict[Gate, str]

def run_part_1(data: tuple[Wires, Gates]):
    wires, gates, _ = data
    wires = calculate_gates(wires, gates)
    bits = dict_to_bitarray(all_wires(wires, "z"))
    return binary_to_decimal(bits)

# Not going to lie. I did not understand part 2 at all. I spent way too much time trying to
# figure it out and ultimately found a solution on reddit that didn't look overly complicated
# and didn't rely on manually searching for the errors. I do think in adapting it fit in here,
# I understand what's happening. I just don't have any more time to put into this so it'll have
# to do. https://github.com/guohao/advent-of-code/blob/main/2024/day24/part2.py
def run_part_2(data: tuple[Wires, Gates]):
    _, _, data = data

    wires = {}
    gates = {}

    line_break = data.index("")
    for idx, line in enumerate(data):
        if idx <= line_break: continue

        minmax = lambda a, b: (a, b) if a <= b else (b, a)
        wire_1, gate_type, wire_2, _, output_wire = line.split(" ")
        wire_1, wire_2 = minmax(wire_1, wire_2)
        gates[(GateType(gate_type), wire_1, wire_2)] = output_wire
        wires[output_wire] = GateType(gate_type), wire_1, wire_2

    output = set()
    c = ''

    for idx in range(int(max(wires)[1:])):
        x = f"x{idx:02}"
        y = f"y{idx:02}"
        z = f"z{idx:02}"
        zn = f"z{idx + 1:02}"
        xxy = gates[GateType.XOR, x, y]
        xay = gates[GateType.AND, x, y]

        if not c:
            c = xay
            continue

        a, b = minmax(c, xxy)
        k = GateType.XOR, a, b
        if k not in gates:
            a, b = list(set(wires[z][1:]) ^ set(k[1:]))
            output.add(a)
            output.add(b)
            wires, gates = swap(wires, gates, a, b)
        elif gates[k] != z:
            output.add(gates[k])
            output.add(z)
            wires, gates = swap(wires, gates, z, gates[k])
        k = wires[z]
        xxy = gates[GateType.XOR, x, y]
        xay = gates[GateType.AND, x, y]
        c = gates[GateType.AND, *minmax(c, xxy)]
        c = gates[GateType.OR, *minmax(c, xay)]

    return ",".join(sorted(output))

def swap(wires, gates, a, b):
    wires[a], wires[b] = wires[b], wires[a]
    gates[wires[a]], gates[wires[b]] = gates[wires[b]], gates[wires[a]]
    return wires, gates

def dict_to_bitarray(wires: Wires):
    return [bit[1] for bit in sorted(wires.items(), reverse=True)]

def binary_to_decimal(bitarray: list[int]):
    return sum(val * (2 ** idx) for idx, val in enumerate(reversed(bitarray)))

def all_wires(wires: Wires, wire_prefix: str):
    return {wire: val for wire, val in wires.items() if wire[0] == wire_prefix}

def calculate_gates(wires: Wires, gates: Gates) -> Wires:
    while any(val == None for wire, val in wires.items() if wire[0] == "z"):
        for gate, output_wire in gates.items():
            if wires[output_wire] != None: continue
            wires[output_wire] = calculate_gate(wires, gate)
    return wires

def calculate_gate(wires: Wires, gate: Gate) -> Optional[int]:
    if wires[gate.input_a] == None or wires[gate.input_b] == None:
        return None
    
    match gate.type:
        case GateType.AND:
            return wires[gate.input_a] & wires[gate.input_b]
        case GateType.OR:
            return wires[gate.input_a] | wires[gate.input_b]
        case GateType.XOR:
            return wires[gate.input_a] ^ wires[gate.input_b]

def parse_input(data) -> tuple[Wires, Gates]:
    line_break = data.index("")
    wires, gates = {}, {}

    for idx, line in enumerate(data):
        if idx == line_break: continue
        if idx < line_break:
            wire, val = line.split(": ")
            wires[wire] = int(val)
            continue
        
        wire_1, gate_type, wire_2, _, output_wire = line.split(" ")
        wires[wire_1] = wires.get(wire_1)
        wires[wire_2] = wires.get(wire_2)
        wires[output_wire] = wires.get(output_wire)
        gates[Gate(GateType(gate_type), wire_1, wire_2, output_wire)] = output_wire

    return wires, gates, data
