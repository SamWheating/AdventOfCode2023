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
        col = [row[x] for row in rocks]
        new_rocks.append(col[::-1])

    return new_rocks

assert rotate_cw([[1,2],[3,4]]) == [[3,1],[4,2]]

def spin(rocks: List[List]) -> List[List]:
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
for i in range(1_000_000_000):
    rocks = spin(rocks)
    hash = ""
    for row in rocks:
        hash += "".join(row)
    if hash in seen:
        print(f"step {i} was also step {seen[hash]}")
        break
    seen[hash] = i
    load[i] = get_load(rocks)

period = i - seen[hash]
offset = seen[hash]
    
# assume periodic
remaining_moves = 1_000_000_000 - offset
position  = (remaining_moves % period) + offset
load = load[position-1] # I had an off-by-one somewhere, this accounts for it.

print(f"Part 2: {load}")