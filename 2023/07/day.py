from collections import defaultdict
from itertools import product
import re

# Day 7

CARDS = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
CARDS_INTERESTING = ['J','2','3','4','5','6','7','8','9','T','Q','K','A']

class Hand:
    cards: str
    card_counts: [int]

    def __init__(self, hand: str, bid: int = 0, make_it_interesting: bool = False):
        self.make_it_interesting = make_it_interesting
        self.cards = hand
        self.bid = bid
        self.calculate_hand()

    def __eq__(self, other: object) -> bool:
        return self.cards == other.cards

    def __lt__(self, other: object) -> bool:
        if self.hand_strength == other.hand_strength:
            return self.card_strengths < other.card_strengths
        return self.hand_strength < other.hand_strength

    def calculate_hand(self) -> None: # cache some calculated values
        counts = defaultdict(lambda:0)
        cards = self.best_hand_with_jokers if self.make_it_interesting else self.cards
        for card in cards:
            counts[card] += 1
        self.card_counts = sorted(counts.values())
        self.card_strengths = [self.card_strength(card) for card in self.cards]

    def card_strength(self, card: str) -> int: # card strength based on card order
        return CARDS_INTERESTING.index(card) if self.make_it_interesting else CARDS.index(card)
    
    @property
    def hand_strength(self) -> int: # Returns the overall hand strength 
        if self.is_five_of_a_kind: return 7
        if self.is_four_of_a_kind: return 6
        if self.is_full_house: return 5
        if self.is_three_of_a_kind: return 4
        if self.is_two_pair: return 3
        if self.is_one_pair: return 2
        return 1
    
    @property
    def best_hand_with_jokers(self) -> str:
        all_hands = []
        for card in CARDS_INTERESTING:
            hands = [(c,) if c != "J" else ("J", card) for c in self.cards]
            all_hands.extend(''.join(c) for c in product(*hands))
        all_hands = list(set(all_hands)) # remove dupes
        hands = sorted([Hand(hand) for hand in all_hands], reverse=True)
        return hands[0].cards

    @property
    def is_five_of_a_kind(self) -> bool:
        return self.card_counts == [5]

    @property
    def is_four_of_a_kind(self) -> bool:
        return self.card_counts == [1,4]

    @property
    def is_full_house(self) -> bool:
        return self.card_counts == [2,3]

    @property
    def is_three_of_a_kind(self) -> bool:
        return self.card_counts == [1,1,3]

    @property
    def is_two_pair(self) -> bool:
        return self.card_counts == [1,2,2]

    @property
    def is_one_pair(self) -> bool:
        return self.card_counts == [1,1,1,2]
    
def run_part_1(data):
    winnings = 0
    hands = sorted([Hand(*hand) for hand in data])
    for i, hand in enumerate(hands):
        winnings += (hand.bid * (i + 1))
    return winnings

def run_part_2(data):
    winnings = 0
    hands = sorted([Hand(*hand, make_it_interesting=True) for hand in data])
    for i, hand in enumerate(hands):
        winnings += (hand.bid * (i + 1))
    return winnings

def parse_input(data):
    hands = []
    for hand in data:
        cards, bid = hand.split(" ")
        hands.append((cards, int(bid)))
    return hands
