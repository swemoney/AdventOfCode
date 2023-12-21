from collections import deque
from math import lcm, prod
from copy import deepcopy
import re

# Day 20

module_re = re.compile(r"(%|&)?(.+) -> (.+)")

def run_part_1(data):
    modules, _ = deepcopy(data)
    return prod(press_button(modules, num_presses=1_000))

def run_part_2(data):
    modules, rx_input = deepcopy(data)
    return press_button(modules, num_presses=10_000, rx_input=rx_input)

class Module:
    def __init__(self, mod_type: str, name: str, outputs: list[str]):
        self.mod_type = mod_type
        self.name = name
        self.outputs = outputs
        self.inputs = {}
        self.is_on = False

    def recv_pulse(self, input_name: str, input_high: bool) -> bool:
        match self.mod_type:
            case "%":
                if input_high: return None
                self.is_on = not self.is_on
                return self.is_on

            case "&":
                self.inputs[input_name] = input_high
                return not all(value == True for value in self.inputs.values())
            
            case _:
                return input_high

def press_button(modules: dict[str, Module], num_presses: int, rx_input = None):
    pulses_low, pulses_high = 0, 0
    rx_input_inputs = {}

    for i in range(num_presses):
        
        curr_mod = modules["broadcaster"]
        pulses_low += 1

        pulse = curr_mod.recv_pulse(None, input_high=False)
        queue = deque([(curr_mod, pulse)])

        while queue:
            curr_mod, pulse = queue.popleft()
            for output in curr_mod.outputs:

                if pulse: pulses_high += 1
                else: pulses_low += 1

                if modules.get(output) is None: continue

                # Part 2
                if rx_input is not None and modules[output].name == rx_input and pulse == True:
                    if rx_input_inputs.get(curr_mod.name) is None:
                        rx_input_inputs[curr_mod.name] = i + 1
                    if all(mod in rx_input_inputs.keys() for mod in modules[output].inputs):
                        return lcm(*rx_input_inputs.values())
                    
                next_pulse = modules[output].recv_pulse(curr_mod.name, input_high=pulse)
                if next_pulse is not None:
                    queue.append((modules[output], next_pulse))

    return (pulses_low, pulses_high)

def parse_input(data):
    modules = {}
    rx_input = None

    for line in data:
        mod_type, mod_name, output_str = module_re.findall(line)[0]
        outputs = output_str.split(", ")
        if mod_type == "": 
            modules["broadcaster"] = Module(mod_type="broadcast", name="broadcaster", outputs=outputs)
        else: 
            modules[mod_name] = Module(mod_type=mod_type, name=mod_name, outputs=outputs)

    # Fill in the inputs for all the modules
    for mod_name, mod in modules.items():
        for output in mod.outputs:
            if modules.get(output) is not None:
                modules[output].inputs[mod_name] = False
            if output == "rx":
                rx_input = mod_name

    return (modules, rx_input)
