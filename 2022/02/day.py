# Day 2

WINNING_MOVE = {
    "Rock": "Paper",
    "Paper": "Scissors",
    "Scissors": "Rock"
}

POINTS = {
    "Rock": 1,
    "Paper": 2,
    "Scissors": 3,
    "Loss": 0,
    "Draw": 3,
    "Win": 6
}

def run_part_1(data):
    CODES = {
        "A": "Rock",
        "X": "Rock",
        "B": "Paper",
        "Y": "Paper",
        "C": "Scissors",
        "Z": "Scissors"
    }

    score = 0

    for round in data:
        opponent, me = [CODES[move] for move in round.split(" ")]

        score += POINTS[me]
        if WINNING_MOVE[opponent] == me:
            score += POINTS["Win"]
        elif opponent == me:
            score += POINTS["Draw"]

    return score

def run_part_2(data):
    CODES = {
        "A": "Rock",
        "X": "Loss",
        "B": "Paper",
        "Y": "Draw",
        "C": "Scissors",
        "Z": "Win"
    }

    score = 0

    for round in data:
        opponent, outcome = [CODES[move] for move in round.split(" ")]
        score += POINTS[outcome]
        if outcome == "Win":
            score += POINTS[WINNING_MOVE[opponent]]
        elif outcome == "Draw":
            score += POINTS[opponent]
        elif outcome == "Loss":
            score += POINTS[
                next(losing_move for losing_move, winning_move in WINNING_MOVE.items() if winning_move == opponent)
            ]

    return score

def parse_input(data):
    return data
