import sys
from typing import Tuple, List

if len(sys.argv) > 1 and sys.argv[1] == "--test":
    file = "test_input.txt"
else:
    file = "input.txt"

DEBUG=True

with open(file) as inputfile:
    lines = [l.strip("\n") for l in inputfile.readlines()]

def tilt_rocks(rocks: List[List]) -> List[List]:
    # roll all of the rocks to the north
    for y in range(1, len(rocks)):
        for x in range(len(rocks[y])):
            if rocks[y][x] == "O":
                for dy in range(1, y+1):
                    if rocks[y-dy][x] != ".":
                        rocks[y][x] = "."
                        rocks[y-dy+1][x] = "O"
                        break
                    elif y-dy == 0:
                        rocks[y][x] = "."
                        rocks[0][x] = "O"
                        break
    return rocks

assert tilt_rocks([[".", "#"],["O", "."],[".", "O"]]) == [["O","#"],[".", "O"],[".","."]]

def rotate_cw(rocks: List[List]) -> List[List]:
    # create a 90deg CW rotated copy of an array
    new_rocks = []
    for x in range(len(rocks[0])):
        new_rocks.append([row[x] for row in rocks][::-1])

    return new_rocks

assert rotate_cw([[1,2],[3,4]]) == [[3,1],[4,2]]

def spin(rocks: List[List]) -> List[List]:
    # tilting north, west, south, east is equivalent to 4x (tilt north, rotate 90deg cw)
    for _ in range(4):
        rocks = rotate_cw(tilt_rocks(rocks))
    return rocks

def get_load(rocks: List[List]) -> int:
    load = 0
    for y in range(len(rocks)):
        for x in range(len(rocks[y])):
            if rocks[y][x] == "O":
                load += len(rocks) - y

    return load

# part 1
rocks = tilt_rocks([list(line) for line in lines])
print(f"Part 1: {get_load(rocks)}")

# part 2
seen = {}
load = {}
rocks = [list(line) for line in lines]

# assume that that the load is periodic with a fixed lead-in
# (i.e. 3,4,5,1,2,1,2,1,2,...1,2)
for i in range(1_000_000_000):
    rocks = spin(rocks)
    hash = ""
    for row in rocks:
        hash += "".join(row)
    if hash in seen: # we've hit a loop, can exit and find the period + offset
        break
    seen[hash] = i
    load[i] = get_load(rocks)

period = i - seen[hash]
offset = seen[hash]
    
# assume periodic
remaining_moves = 1_000_000_000 - offset - 1 # 1 is to adjust for 1-vs-0 indexed.
position  = (remaining_moves % period) + offset
load = load[position]

print(f"Part 2: {load}")