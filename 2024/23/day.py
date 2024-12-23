from collections import defaultdict
from itertools import combinations
import networkx as nx

# Day 23

# Why reinvent the wheel when networkx is made for this?
# I used a couple of loops to find all of the connections of 3's for part 1 
# but rewrote it for networkx after doing part 2

def run_part_1(data):
    return sum( any(computer.startswith("t") for computer in clique) for clique in data if len(clique) == 3 )

def run_part_2(data):
    return ",".join(sorted(max(data, key=len)))

def parse_input(data):
    graph = nx.Graph()
    for connection in [line.split("-") for line in data]:
        graph.add_edge(connection[0], connection[1])

    return list(nx.enumerate_all_cliques(graph))
