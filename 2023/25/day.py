import networkx as nx
from math import prod

# Day 25

def run_part_1(data):
    graph = create_graph(data)
    for edge in nx.minimum_edge_cut(graph):
        graph.remove_edge(*edge)
    group_sizes = [len(connections) for connections in nx.connected_components(graph)]
    return prod(group_sizes)

def run_part_2(data):
    return "LET IT SNOW!"

def create_graph(connections: set[tuple[str, str]]):
    return nx.from_edgelist(connections)

def parse_input(data):
    connections = set()
    for line in data:
        left, right = line.split(": ")
        for connection in right.split():
            connections.add((left, connection))
    return connections
