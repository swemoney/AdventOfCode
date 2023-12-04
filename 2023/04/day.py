import re

# Day 4

def run_part_1(data):
    return sum( [card_points(num_matches) for num_matches in card_matches(data)] )

def run_part_2(data):
    number_of_matches = card_matches(data)
    number_of_cards = [1 for _ in data]
    for i in range(len(data)):
        for j in range(number_of_cards[i]):
            for k in range(i + 1, i + number_of_matches[i] + 1):
                number_of_cards[k] += 1
    return sum(number_of_cards)

def card_points(num_matches: [int]):
    return int(1 * pow(2, num_matches - 1))

def card_matches(data):
    return [len(set(card["winning"]) & set(card["mine"])) for card in data]

def parse_input(data):
    cards = []
    for card_data in data:
        winning_data, mine_data = card_data.split(":")[1].split("|")
        winning = [num for num in re.findall(r"(\d+)", winning_data)]
        mine = [num for num in re.findall(r"(\d+)", mine_data)]
        cards.append({"winning": winning, "mine": mine})
    return cards
