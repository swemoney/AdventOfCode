from utils import Vector3
from math import prod
from itertools import combinations

# Day 8

def fast_distance(a: Vector3, b: Vector3):
    return (a.x - b.x)**2 + (a.y - b.y)**2 + (a.z - b.z)**2

def connect_pairs(locations, num_connections):
    all_pairs = []
    for a, b in combinations(locations, 2):
        all_pairs.append((fast_distance(a, b), a, b))

    all_pairs.sort(key=lambda x: x[0])

    connections = []
    for i in range(min(num_connections, len(all_pairs))):
        _, a, b = all_pairs[i]
        connections.append((a, b))

    return connections

def create_circuits(connections):
    parent = {}
    for a, b in connections:
        parent.setdefault(a, a)
        parent.setdefault(b, b)

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(a, b):
        parent_a, parent_b = find(a), find(b)
        if parent_a != parent_b:
            parent[parent_b] = parent_a

    for a, b in connections:
        union(a, b)

    circuits = {}
    for connection in parent:
        root = find(connection)
        circuits.setdefault(root, []).append(connection)

    return sorted(circuits.values(), key=len, reverse=True)

def run_part_1(data):
    connections = connect_pairs(data, 1000)
    circuits = create_circuits(connections)

    return prod([len(c) for c in circuits[:3]])

def run_part_2(data):
    locations = data[:]
    n = len(locations)

    best_i, best_j = None, None
    best_d = float('inf')

    for i in range(n):
        for j in range(i + 1, n):
            d = fast_distance(locations[i], locations[j])
            if d < best_d:
                best_d = d
                best_i, best_j = i, j

    connected = {locations[best_i], locations[best_j]}
    unconnected = set(locations) - connected

    edges = [(locations[best_i], locations[best_j])]

    while unconnected:
        best_edge = None
        best_d = float('inf')

        for c in connected:
            for u in unconnected:
                d = fast_distance(c, u)
                if d < best_d:
                    best_d = d
                    best_edge = (c, u)

        c, u = best_edge
        edges.append(best_edge)

        connected.add(u)
        unconnected.remove(u)

    return edges[-1][0].x * edges[-1][1].x 
    # This takes 25 seconds to run on my machine but I don't have time to do something else right now

def parse_input(data):
    return [Vector3(*[int(num) for num in line.split(",")]) for line in data]
