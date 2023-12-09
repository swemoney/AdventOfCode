import re, math

# Day 8

def run_part_1(data):
    rl_list, nodes = data
    number_of_steps = traverse_nodes('AAA', 'ZZZ', rl_list, nodes)
    return number_of_steps

def run_part_2(data):
    rl_list, nodes = data
    start_nodes = [node for node in nodes if node.endswith('A')]
    start_node_steps = []
    for start_node in start_nodes:
        start_node_steps.append(traverse_nodes(start_node, 'Z', rl_list, nodes))
    return math.lcm(*start_node_steps)

def traverse_nodes(current_node: str, end_node: str, rl_list: str, nodes: [str]):
    number_of_steps = 0
    while not current_node.endswith(end_node):
        rl = rl_list[number_of_steps % len(rl_list)]
        current_node = nodes[current_node][0] if rl == "L" else nodes[current_node][1]
        number_of_steps += 1
    return number_of_steps

def parse_input(data):
    rl = data[0]
    nodes = {}
    for node in data[2:]:
        node_parts = re.findall(r"([A-Z0-9]{3})", node)
        nodes[node_parts[0]] = (node_parts[1], node_parts[2])
    return (rl, nodes)
