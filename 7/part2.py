from typing import Dict, List
from collections import defaultdict
from dataclasses import dataclass
from functools import cmp_to_key
import sys

if len(sys.argv) > 1 and sys.argv[1] == "--test":
    file = "test_input.txt"
else:
    file = "input.txt"

with open(file) as inputfile:
    lines = [l.strip("\n") for l in inputfile.readlines()]



def camel_classify(hand: str) -> int:
    # returns points for what kind of hand this is
    # 7: 5 of a kind
    # 6: 4 of a kind
    # 5: full house
    # 4: 3 of a kind
    # 3: 2 pair
    # 2: one pair
    # 1: else

    if len(set(hand)) == 1:
        return 7
    
    counts = defaultdict(int)
    for c in hand:
        counts[c] += 1

    jokers = counts["J"]

    if max(counts.values()) == 4:
        if jokers != 0: return 7 # jokers make full set
        return 6 # four of a kind
    
    if len(set(hand)) == 2:
        if jokers != 0:
            return 7
        return 5 # full house
    
    if max(counts.values()) == 3:
        if jokers != 0:
            return 6 # 1 or more jokers makes this a four of a kind
        return 4 # 3 of a kind

    if len([v for v in counts.values() if v == 2]) == 2:
        if jokers == 2:
            return 6 # 2 jokers can make this 4/kind
        if jokers == 1:
            return 5 # joker can make this a full house
        return 3 # 2 pair

    if max(counts.values()) == 2:
        if jokers != 0:
            return 4 # jokers + 1 other card makes 3 of a kind, 2 cards + 1 joker makes 3 of a kind
        return 2 # one pair
    
    if jokers != 0:
        return 2 # jokers can make this a pair
    
    return 1

assert camel_classify("T55J5") == 6
assert camel_classify("KTJJT") == 6
assert camel_classify("QQQJA") == 6

assert camel_classify("11111") == 7
assert camel_classify("11112") == 6
assert camel_classify("11122") == 5
assert camel_classify("11123") == 4
assert camel_classify("11223") == 3
assert camel_classify("11234") == 2
assert camel_classify("12345") == 1

# J IS THE WEAKEST BC PART 2
CAMEL_PRECEDENCE = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]

# implements 3-way compare, -1, 0, 1
def camel_compare(hand1, hand2) -> int:
    if camel_classify(hand1) > camel_classify(hand2):
        return 1
    if camel_classify(hand1) < camel_classify(hand2):
        return -1
    for i in range(len(hand1)):
        if CAMEL_PRECEDENCE.index(hand1[i]) < CAMEL_PRECEDENCE.index(hand2[i]):
            return 1
        if CAMEL_PRECEDENCE.index(hand1[i]) > CAMEL_PRECEDENCE.index(hand2[i]):
            return -1
    return 0

assert camel_compare("22222", "23456") == 1
assert camel_compare("222A2", "222K2") == 1
assert camel_compare("T55J5", "QQQJA") == -1

def camel_comparer(h1, h2):
    return camel_compare(h1["hand"], h2["hand"])

hands = []
for line in lines:
    hands.append({
        "hand": line.split()[0],
        "bid": int(line.split()[1])
    })

hands.sort(key=cmp_to_key(camel_comparer))

print(hands)

total = 0
for i in range(len(hands)):
    total += (1+i) * hands[i]["bid"]

print(total)
