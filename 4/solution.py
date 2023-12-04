from typing import List, Dict, Iterable
from collections import defaultdict
import sys

if len(sys.argv) > 1 and sys.argv[1] == "--test":
    file = "test_input.txt"
else:
    file = "input.txt"

with open(file) as inputfile:
    lines = [l.strip('\n') for l in inputfile.readlines()]

total = 0
matches_per_card: Dict[int, int] = {}
for i in range(len(lines)):

    winners = []
    numbers = []
    for section in lines[i].split(" | ")[0].split(":")[1].split():
        winners.append(int(section))
    for section in lines[i].split(" | ")[1].split():
        numbers.append(int(section))
    
    matches = 0
    for num in numbers:
        if num in winners:
            matches += 1

    matches_per_card[i+1] = matches # 0-idx to 1-idx, store these for part 2
    if matches > 0:
        total += 2**(matches-1)

print(f"Part 1: {total}")
        
# Part 2: Just simulate all of the cards, running one hand at a time
# I'm pretty sure there's a faster more math-y solution here but I was in a hurry
# (takes ~1.5s on MBP w/ M1 Max LOL)

# current hand of cards (card: number in hand)
cards = {c: 1 for c in range(1, len(lines)+1)} 
total = 0
while True:
    next_cards = {c: 0 for c in range(1, len(lines)+1)}
    for card in cards.keys():
        total += cards[card]
        for _ in range(cards[card]):
            for i in range(1, matches_per_card[card]+1):
                next_cards[card+i] += 1
    
    cards = next_cards
    if sum(cards.values()) == 0:
        break

print(f"Part 2: {total}")
