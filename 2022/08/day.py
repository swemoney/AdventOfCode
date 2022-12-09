# Day 8

import numpy as np
from copy import copy

def run_part_1(data):
    hidden, max_x, max_y = prepare_data(data)
    for x in range(1, max_x - 1):
        for y in range(1, max_y - 1):
            sides = [
                data[x, :y], data[x, y+1:],
                data[:x, y], data[x+1:, y]]
            if any(np.max(side) < data[x, y] for side in sides):
                continue
            hidden[x, y] = 1 # This tree should be blocked

    return np.size(data) - np.sum(hidden)

def run_part_2(data):
    scenic_scores, max_x, max_y = prepare_data(data)
    for x in range(1, max_x - 1):
        for y in range(1, max_y - 1):
            sides = [
                np.flip(data[x, :y]), data[x, y+1:],
                np.flip(data[:x, y]), data[x+1:, y]]
            trees = []
            for side in sides:
                if np.any(side >= data[x, y]):
                    trees.append(np.where(side >= data[x, y])[0][0] + 1)
                else:
                    trees.append(side.size)
            scenic_scores[x, y] = np.prod(np.array(trees))
    return np.max(scenic_scores)

def prepare_data(data):
    empty_data = copy(data)
    empty_data.fill(0)
    return (empty_data, data.shape[0], data.shape[1])

def parse_input(data):
    return np.array([[int(height) for height in list(line)] for line in data])
