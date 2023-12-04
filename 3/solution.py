from typing import List, Dict, Iterable
import sys

if len(sys.argv) > 1 and sys.argv[1] == "--test":
    file = "test_input.txt"
else:
    file = "input.txt"

with open(file) as inputfile:
    lines = [l.strip('\n') for l in inputfile.readlines()]

def get_surrounding_values(board: List[Iterable], y: int, x: int):
    values = []
    for i in range(max(0, y-1), min(len(board), y+2)):
        for j in range(max(0, x-1), min(x+2, len(board[0]))):
            if not (i == y and j == x):
                values.append(board[i][j])
    return values

assert get_surrounding_values(["aaa", "aba", "aaa"],1,1) == ["a"]*8
assert get_surrounding_values(["aaa", "add", "ada"],2,2) == ["d"]*3
assert get_surrounding_values(["abc", "def", "ghi"],1,0) == ["a","b","e","g","h"]

def is_symbol_nearby(board: List[str], y: int, x: int) -> bool:
    surrounding = get_surrounding_values(board,y,x)
    return any([v not in '1234567890.' for v in surrounding])

assert not is_symbol_nearby(["...",".7.","..."], 1, 1) 
assert is_symbol_nearby([".*.",".7.","..."], 1, 1) 
assert is_symbol_nearby(["...","/7.","..."], 1, 1) 
assert not is_symbol_nearby(["!..","...","..7"], 2, 2) 

# PART 1

total = 0
for y in range(len(lines)):
    is_part = False
    cur_value = 0
    for x in range(len(lines[y])):

        if lines[y][x].isdigit():
            cur_value = cur_value * 10 + int(lines[y][x])
            is_part = is_part or is_symbol_nearby(lines, y, x)

        else:
            if is_part: # have we seen an adjacent symbol while parsing this number?
                total += cur_value
                is_part = False
            cur_value = 0 

    if is_part:
        total += cur_value

print(f"Part 1: {total}")

# PART 2:

# Create a new board where each cell is a reference to a map of numbers
#
#  1  2  3  .  .      1  1  1  .  . 
#  .  *  .  .  .  ->  .  .  .  .  .   and {1: 123, 2: 456}
#  .  .  4  5  6      .  .  2  2  2 
#
# then we can just count the number of unique values surrounding each *

board = [[None]*len(lines[0]) for _ in range(len(lines))]
values: Dict[int, int] = {}
for y in range(len(lines)):
    cur_value = 0
    for x in range(len(lines[y])):
        index = len(values)
        if lines[y][x].isdigit():
            cur_value = cur_value * 10 + int(lines[y][x])
            board[y][x] = index
        else:
            if cur_value > 0:
                values[index] = cur_value
                cur_value = 0
    if cur_value > 0: # special case, have to write out the number after wrapping
        values[index] = cur_value
        cur_value = 0   

# now look for all of the asterixes with exactly two adjacent numbers
total = 0
for y in range(len(lines)):
    for x in range(len(lines[y])):
        if lines[y][x] == "*":
            adjacent_nums = set([s for s in get_surrounding_values(board, y, x) if s is not None])
            # add the ratio to the total, if applicable
            if len(adjacent_nums) == 2:
                ratio = 1
                for num in adjacent_nums:
                    ratio *= values[num]                
                total += ratio

# 79621339: too low
print(f"Part 2: {total}")

