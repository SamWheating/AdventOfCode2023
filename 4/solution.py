from typing import Dict
from collections import defaultdict
import sys

if len(sys.argv) > 1 and sys.argv[1] == "--test":
    file = "test_input.txt"
else:
    file = "input.txt"

with open(file) as inputfile:
    lines = [l.strip("\n") for l in inputfile.readlines()]

total = 0
matches_per_card: Dict[int, int] = {}
for i in range(len(lines)):
    # hacky parsing, but it works.
    winners = [int(s) for s in lines[i].split(" | ")[0].split(":")[1].split()]
    numbers = [int(s) for s in lines[i].split(" | ")[1].split()]

    matches = len([n for n in numbers if n in winners])
    matches_per_card[i + 1] = matches  # 0-idx to 1-idx, store these for part 2
    total += int(2 ** (matches - 1))

print(f"Part 1: {total}")

# Part 2: Just simulate all of the cards, running one hand at a time
# I'm pretty sure there's a faster more math-y solution here but I was in a hurry

# current hand of cards (card: number in hand)
cards = {c: 1 for c in range(1, len(lines) + 1)}
total = 0
while True:
    next_cards = defaultdict(int)
    for card in [c for c in cards.keys() if cards[c] >= 1]:
        total += cards[card]
        for i in range(1, matches_per_card[card] + 1):
            next_cards[card + i] += cards[card]

    cards = next_cards
    if sum(cards.values()) == 0:  # none left
        break

print(f"Part 2: {total}")
