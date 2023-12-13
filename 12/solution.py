import sys
from typing import Tuple, List

if len(sys.argv) > 1 and sys.argv[1] == "--test":
    file = "test_input.txt"
else:
    file = "input.txt"

with open(file) as inputfile:
    lines = [l.strip("\n") for l in inputfile.readlines()]

def prevalidate_springs(springs: List[str], reqs: Tuple[int]) -> bool:
    """
    Validate that a partial arrangement could still be a viable solution.

    This prunes the search tree, reducing the number of avenues to explore.

    reasons for being invalid:
        - the leftmost n groups don't conform to the req
        - the minimum number of groups is more than the req
    """
    if springs[0] == "?":
        return True
    
    groups = []
    current = 0
    uncertain = False # whether the size of the last group is bounded or not
    for c in springs:
        if c == "#":
            current += 1
        elif c == "?":
            if current != 0:
                uncertain = True
                groups.append(current)
            break
        else:
            if current != 0:
                groups.append(current)
                current = 0

    if len(groups) > len(reqs):
        #print(groups, reqs)
        #print("failed prevalidation - too many groups already")
        return False

    if uncertain and len(groups) >= 1:
        if groups[:-1] != list(reqs)[:len(groups)-1]:
            #print(groups, reqs)
            #print("failed prevalidation - first n-1 groups don't align")
            return False
        if groups[-1] > reqs[len(groups)-1]:
            #print("failed prevalidation, last group is wrong")
            return False
    else:
        if groups != list(reqs)[:len(groups)]:
            #print(groups, reqs)
            #print("Failed prevalidation - first n groups don't align")
            return False
    
    # if we're still here, check number of groups
    min_groups = 0
    prev = None
    for c in springs:
        if c == "?":
            continue
        if c == "#" and prev in {".", None}:
            min_groups += 1
        prev = c

    if min_groups > len(reqs):
        #print("Failed prevalidation - too many groups")
        return False

    return True

# we don't know enough about this one
assert prevalidate_springs("????", (1,1))

# these ones are still viable
assert prevalidate_springs("#.#?.", (1,2))
assert prevalidate_springs("#.#?#", (1,1,1))

# we can already tell that the first group is too long
assert not prevalidate_springs("###?.", (2,1))

# this one has at least 4 groups... gotta go
assert not prevalidate_springs("#.#?.#?.#?", (1,2,3))

assert prevalidate_springs(".###.???????", (3,2,1))



def validate_springs(springs: str, reqs: Tuple[int]) -> bool:
    groups = []
    current = 0
    for c in springs:
        if c == "#":
            current += 1
        else:
            if current != 0:
                groups.append(current)
                current = 0
    if current != 0:
        groups.append(current)

    return list(reqs) == groups


assert validate_springs("##..##", (2,2))
assert validate_springs("#.##.###", (1,2,3))
assert not validate_springs("#.##.###", (2,2,3))

from copy import copy

# TODO: prune the heck out of this
def count_ways(springs: List[str], reqs: Tuple[int]) -> int:

    if springs.count("?") == 0:
        if validate_springs(springs, reqs):
            return 1
        return 0
    
    # are we already done? Since we're greedy-filling this happens often.
    completed = [s.replace("?", ".") for s in springs]
    if validate_springs(completed, reqs):
        return 1
    
    if not prevalidate_springs(springs, reqs):
        #print(f"{springs}, {reqs} failed prevalidation")
        return 0
    
    #print(f"{''.join(springs)}, {reqs} passed prevalidation")

    total = 0
    unknown = springs.index("?")

    yes = [s for s in springs]
    yes[unknown] = "#"
    total += count_ways(yes, reqs)

    no = [s for s in springs]
    no[unknown] = "."
    total += count_ways(no, reqs)

    return total

assert count_ways(list("##.##"), (2,2)) == 1
assert count_ways(list("#####"), (2,2)) == 0
assert count_ways(list("?###????????"), (3,2,1)) == 10

def fivetuple(springs: str) -> str:
    return "?".join([springs]*5)

assert fivetuple("##") == "##?##?##?##?##"

assert(count_ways(list(fivetuple("???.###")), (1,1,3)*5)) == 1

# Part 1
total = 0
for line in lines:
    springs = list(line.split(" ")[0])
    reqs = tuple(int(c) for c in line.split(" ")[1].split(","))
    #print(springs, reqs)
    total += count_ways(springs, reqs)

print(f"Part 1: {total}")

# Part 2:
total = 0
for line in lines:
    springs = list(fivetuple(line.split(" ")[0]))
    print("".join(springs))
    reqs = tuple(int(c) for c in line.split(" ")[1].split(",")) * 5
    #print(springs, reqs)
    total += count_ways(springs, reqs)

print(f"Part 2: {total}")

