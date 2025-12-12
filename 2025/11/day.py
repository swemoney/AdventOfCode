from functools import cache

# Day 11

class hashdict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))

@cache
def count(data, position, target):
    return 1 if position == target else sum(count(data, nxt, target) for nxt in data.get(position, []))

def run_part_1(data):
    return count(data, "you", "out")

def run_part_2(data):
    fft =  count(data, "svr", "fft") * count(data, "fft", "dac") * count(data, "dac", "out") 
    dac = count(data, "svr", "dac") * count(data, "dac", "fft") * count(data, "fft", "out")
    return fft + dac 

def parse_input(data):
    return hashdict({device: frozenset(outs.split()) for device, outs in [line.split(": ") for line in data]})
