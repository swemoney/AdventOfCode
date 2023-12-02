import re
import math

# Day 2

draw_re = r"(\d+)\s(red|green|blue)"
game_id_re = r"Game\s(\d+):"

def run_part_1(data):
    valid_cubes = {"red": 12, "green": 13, "blue": 14}
    valid_games = []
    for game in data:
        draws = re.findall(draw_re, game)
        game_id = int(re.match(game_id_re, game).group(1))
        valid_games.append(game_id)
        for num, color in draws:
            if int(num) > valid_cubes[color]:
                valid_games.remove(game_id)
                break
    return sum(valid_games)

def run_part_2(data):
    game_scores = []
    for game in data:
        highest_cubes = {"red": 0, "green": 0, "blue": 0}
        draws = re.findall(draw_re, game)
        for num, color in draws:
            if int(num) > highest_cubes[color]:
                highest_cubes[color] = int(num)
        game_scores.append(math.prod(list(highest_cubes.values())))
    return sum(game_scores)

def parse_input(data):
    return data
