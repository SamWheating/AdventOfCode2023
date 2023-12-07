from dataclasses import dataclass
from functools import cmp_to_key
import sys

if len(sys.argv) > 1 and sys.argv[1] == "--test":
    file = "test_input.txt"
else:
    file = "input.txt"

with open(file) as inputfile:
    lines = [l.strip("\n") for l in inputfile.readlines()]


def camel_classify(hand: str, jokers: bool = False) -> int:
    """
    Classify a hand and return a number based on hand precednece, in order to compare

    5 of a kind -> 6
    4 of a kind -> 5
    full house -> 4
    3 of a kind -> 3
    2 pair -> 2
    one pair -> 1
    else -> 0

    if jokers = True, remove the jokers at the start and add them back in as the most frequent card.
    """

    counts = [hand.count(c) for c in set(hand)] + [0]
    counts.sort(reverse=True)

    if jokers:
        num_jokers = hand.count("J")
        if num_jokers != 0:
            counts.remove(num_jokers)
            counts[0] += num_jokers

    if counts[0] == 5:
        return 6

    if counts[0] == 4:
        return 5  # four of a kind

    if counts[0] == 3 and counts[1] == 2:
        return 4  # full house

    if counts[0] == 3:
        return 3  # 3 of a kind

    if counts[0] == counts[1] == 2:
        return 2  # 2 pair

    if counts[0] == 2:
        return 1  # one pair

    return 0


assert camel_classify("11111") == 6
assert camel_classify("11112") == 5
assert camel_classify("11122") == 4
assert camel_classify("11123") == 3
assert camel_classify("11223") == 2
assert camel_classify("11234") == 1
assert camel_classify("12345") == 0

assert camel_classify("T55J5", True) == 5
assert camel_classify("KTJJT", True) == 5
assert camel_classify("QQQJA", True) == 5


# implements 3-way compare, -1, 0, 1
def camel_compare(hand1, hand2, jokers: bool = False) -> int:
    precedence = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    if jokers:
        precedence.remove("J")
        precedence.append("J")
    if camel_classify(hand1, jokers) > camel_classify(hand2, jokers):
        return 1
    if camel_classify(hand1, jokers) < camel_classify(hand2, jokers):
        return -1
    for i, c in enumerate(hand1):
        if precedence.index(c) < precedence.index(hand2[i]):
            return 1
        if precedence.index(c) > precedence.index(hand2[i]):
            return -1
    return 0


assert camel_compare("22222", "23456") == 1
assert camel_compare("222A2", "222K2") == 1
assert camel_compare("T55J5", "QQQJA") == -1


@dataclass
class Hand:
    hand: str
    bid: int

hands = []
for line in lines:
    hands.append(Hand(line.split()[0], int(line.split()[1])))

# Part 1
hands.sort(key=cmp_to_key(lambda a, b: camel_compare(a.hand, b.hand)))
total = 0
for i, hand in enumerate(hands):
    total += (1 + i) * hand.bid

print(f"Part 1: {total}")

# Part 1
hands.sort(key=cmp_to_key(lambda a, b: camel_compare(a.hand, b.hand, True)))
total = 0
for i, hand in enumerate(hands):
    total += (1 + i) * hand.bid

print(f"Part 1: {total}")
