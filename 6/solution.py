from typing import Dict, List
from collections import defaultdict
from dataclasses import dataclass
import sys

if len(sys.argv) > 1 and sys.argv[1] == "--test":
    file = "test_input.txt"
else:
    file = "input.txt"

with open(file) as inputfile:
    lines = [l.strip("\n") for l in inputfile.readlines()]

def get_distances_for_given_time(duration: int) -> List[int]:
    distances = []
    
    for i in range(duration): # holding the button for every possible amount of time
        distances.append(i * (duration-i))
    
    return distances

# Part 1

times = [int(t) for t in lines[0].split(":")[1].split()]
distances = [int(d) for d in lines[1].split(":")[1].split()]

product = 1
for i in range(len(times)):
    total = 0
    for d in get_distances_for_given_time(times[i]):
        if d > distances[i]:
            total += 1

    product *= total

print(f"Part 1: {product}")
    
# Part 2

# this can be done in constant time using the quadratic formula...
# solve 0 = x**2 - time*x - distance  and take the difference of the two results.
# but since there's only 62m numbers to process, we can just loop this.

time = int(lines[0].split(":")[1].replace(" ", ""))
distance = int(lines[1].split(":")[1].replace(" ", ""))

total = 0
for i in range(time):
    if i * (time - i) > distance:
        total += 1

print(f"Part 2: {total}")


