from tqdm import tqdm
from collections import Counter, deque

# Day 22

PRUNE_CONSTANT = 16777216
CHANGES = 2000

def run_part_1(data):
    secret_numbers = []
    for secret_number in tqdm(data, desc="Secret Numbers"):
        secret_numbers.append(calculate_secret_number(secret_number))
    return sum(secret_numbers)

def run_part_2(data):
    secret_numbers, price_sequences = get_best_prices(data)
    return price_sequences.most_common(1)[0][1]

def calculate_secret_number(secret_number: int) -> int:
    for i in range(CHANGES):
        secret_number = calculate_single_iteration(secret_number)
    return secret_number

def calculate_single_iteration(secret_number: int) -> int:
    secret_number = step_1(secret_number)
    secret_number = step_2(secret_number)
    secret_number = step_3(secret_number)
    return secret_number

def calculate_prices(secret_number: int) -> int:
    diff_sequence = deque()
    results = {}
    previous_price = secret_number % 10

    for _ in range(CHANGES):
        secret_number = calculate_single_iteration(secret_number)
        price = secret_number % 10
        diff = price - previous_price
        diff_sequence.append(diff)

        if len(diff_sequence) > 4:
            diff_sequence.popleft()
        if len(diff_sequence) == 4:
            if (seq := tuple(diff_sequence)) not in results:
                results[seq] = price
        previous_price = price
    
    return secret_number, results

def step_1(secret_number: int) -> int:
    number = secret_number * 64
    return mix_and_prune(secret_number, number)

def step_2(secret_number: int) -> int:
    number = secret_number // 32
    return mix_and_prune(secret_number, number)

def step_3(secret_number: int) -> int:
    number = secret_number * 2048
    return mix_and_prune(secret_number, number)

def mix_and_prune(secret_number: int, mixin: int) -> int:
    secret_number = mix(secret_number, mixin)
    return prune(secret_number)

def mix(secret_number: int, mixin: int) -> int:
    return secret_number ^ mixin

def prune(secret_number: int) -> int:
    return secret_number % PRUNE_CONSTANT

def get_best_prices(first_secrets: list[int]):
    sequences = Counter()
    secret_numbers = []
    for first_secret in tqdm(first_secrets, desc="Get Best Prices"):
        secret_number, prices = calculate_prices(first_secret)
        secret_numbers.append(secret_number)
        sequences.update(prices)
    return secret_numbers, sequences

def parse_input(data):
    return list(map(int, data))
