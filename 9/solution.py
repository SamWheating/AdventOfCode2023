import sys
from typing import List

if len(sys.argv) > 1 and sys.argv[1] == "--test":
    file = "test_input.txt"
else:
    file = "input.txt"

with open(file) as inputfile:
    lines = [l.strip("\n") for l in inputfile.readlines()]

def next_item(nums: List[int]):
    total = 0
    while True:
        total += nums[-1]
        next_nums = [(nums[i] - nums[i-1]) for i in range(1, len(nums))]
        if all([i == 0 for i in next_nums]):
            return total
        nums = next_nums

import pdb
pdb.set_trace()

assert next_item([0, 3, 6, 9, 12, 15]) == 18
assert next_item([1, 3, 6, 10, 15, 21]) == 28
assert next_item([10, 13, 16, 21, 30, 45]) == 68

def prev_item(nums: List[int]) -> int:
    nums.reverse()
    return next_item(nums)

assert prev_item([0, 3, 6, 9, 12, 15]) == -3
assert prev_item([1, 3, 6, 10, 15, 21]) == 0
assert prev_item([10, 13, 16, 21, 30, 45]) == 5

# Part 1
total = 0
for line in lines:
    nums = [int(n) for n in line.split()]
    total += next_item(nums)

print(f"Part 1: {total}")

# Part 2
total = 0
for line in lines:
    nums = [int(n) for n in line.split()]
    total += prev_item(nums)

print(f"Part 2: {total}")
