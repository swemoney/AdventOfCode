from enum import Enum
from typing import NamedTuple, Optional

# Day 24

class GateType(Enum):
    AND = "AND"
    OR = "OR"
    XOR = "XOR"

class Gate(NamedTuple):
    type: GateType
    inputs: list[str]
    output: str

    def has_input(self, input: str) -> bool:
        return input in self.inputs
    
type Wires = dict[str, Optional[int]]
type Gates = list[Gate]

def run_part_1(data: tuple[Wires, Gates]):
    wires, gates = data
    wires = calculate_gates(wires, gates)
    bits = dict_to_bitarray(all_wires(wires, "z"))
    return binary_to_decimal(bits)

# Didn't have time to wrap my brain around part 2
def run_part_2(data: tuple[Wires, Gates]):
    return "N/A"

def dict_to_bitarray(wires: Wires):
    return [bit[1] for bit in sorted(wires.items(), reverse=True)]

def binary_to_decimal(bitarray: list[int]):
    return sum(val * (2 ** idx) for idx, val in enumerate(reversed(bitarray)))

def all_wires(wires: Wires, wire_prefix: str):
    return {wire: val for wire, val in wires.items() if wire[0] == wire_prefix}

def calculate_gates(wires: Wires, gates: Gates) -> Wires:
    while any(val == None for wire, val in wires.items() if (wire[0] == "z" or wire[0] == "x" or wire[0] == "y")):
        for gate in gates:
            if wires[gate.output] != None: continue
            wires[gate.output] = calculate_gate(wires, gate)
    return wires

def calculate_gate(wires: Wires, gate: Gate) -> Optional[int]:
    if any(wires[input] == None for input in gate.inputs):
        return None
    
    match gate.type:
        case GateType.AND:
            return wires[gate.inputs[0]] & wires[gate.inputs[1]]
        case GateType.OR:
            return wires[gate.inputs[0]] | wires[gate.inputs[1]]
        case GateType.XOR:
            return wires[gate.inputs[0]] ^ wires[gate.inputs[1]]

def parse_input(data) -> tuple[Wires, Gates]:
    line_break = data.index("")
    wires, gates = {}, []

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
        gates.append(Gate(GateType(gate_type), [wire_1, wire_2], output_wire))

    return wires, gates
