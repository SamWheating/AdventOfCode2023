import sys
from typing import Tuple, List

if len(sys.argv) > 1 and sys.argv[1] == "--test":
    file = "test_input.txt"
else:
    file = "input.txt"

DEBUG=True

with open(file) as inputfile:
    lines = [l.strip("\n") for l in inputfile.readlines()]

def is_h_symmetrical(view: List[str], x):
    """check that view is symmetrical along a vertical line to the left of x"""
    width = min(x, (len(view[0])-x))
    for row in view:
        if row[x-width:x] != row[x:x+width][::-1]:
            return False
    return True

assert is_h_symmetrical(["abba", "cddc", "effe"], 2)
assert not is_h_symmetrical(["abba", "cddc", "effe"], 1)
assert is_h_symmetrical(["xabba", "ycddc", "zeffe"], 3)

def is_v_symmetrical(view: List[str], y) -> bool:
    """check that view is symmetrical along a horizontal line above y"""
    height = min(y, (len(view)-y))
    for x in range(len(view[0])):
        col = [row[x] for row in view]
        #print(col[y-height:y], col[y:y+height][::-1])
        if col[y-height:y] != col[y:y+height][::-1]:
            return False
    
    return True

assert is_v_symmetrical(["ab","cd","cd","ab"], 2)
assert is_v_symmetrical(["ab","cd","cd","ab","zz"], 2)
assert not is_v_symmetrical(["ac","cd","cd","ab"],2)

assert is_v_symmetrical(['#...##..#', '#....#..#', '..##..###', '#####.##.', '#####.##.', '..##..###', '#....#..#'], 4)
assert not is_v_symmetrical(['#...##..#', '#....#..#', '..##..###', '#####.##.', '#####.##.', '..##..###', '#....#..#'], 3)

def count_h_smudges(view: List[str], x) -> int:
    "given a grid and a vertical line, how many pixels are out of place?"
    width = min(x, (len(view[0])-x))
    smudges = 0
    for row in view:
        for i in range(width):
            if row[x-width:x][i] != row[x:x+width][::-1][i]:
                smudges += 1    
    return smudges

assert count_h_smudges(["abba", "cddc", "effe"], 2) == 0
assert count_h_smudges(["zbba", "cddc", "effe"], 2) == 1
assert count_h_smudges(["zzba", "zzdc", "zzfe"], 2) == 6

def count_v_smudges(view: List[str], y) -> int:
    "given a grid and a horizontal line, how many pixels are out of place?"
    height = min(y, (len(view)-y))
    smudges = 0
    for x in range(len(view[0])):
        col = [row[x] for row in view]
        for i in range(height):
            if col[y-height:y][i] != col[y:y+height][::-1][i]:
                smudges += 1
    
    return smudges

assert count_v_smudges(["aa","bb","bb","aa"], 2) == 0
assert count_v_smudges(["ac","bb","bb","aa"], 2) == 1

blocks = []
block = []
for line in lines:
    if len(line) == 0:
        blocks.append(block)
        block = []
    else:
        block.append(line)
blocks.append(block)

# Part 1
horizontal_planes = []
vertical_planes = []
for i, block in enumerate(blocks):
    for y in range(1,len(block)):
        if is_v_symmetrical(block, y):
            if DEBUG:
                print(f"block {i} symmetrical across y={y}:")
                for row in block[:y]:
                    print(row)
                print("---------------")
                for row in block[y:]:
                    print(row)
                print("\n")
            vertical_planes.append(y)
            break
    else:
        for x in range(1,len(block[0])):
            if is_h_symmetrical(block, x):
                if DEBUG:
                    print(f"block {i} symmetrical across x={x}")
                    for row in block:
                        print("".join(row[:x]) + "|" + "".join(row[x:]))
                    print("\n")
                horizontal_planes.append(x)
                break
        else:
            print(f"not symmetrical! {block}")
            for line in block:
                print(line)

total = 0
for h in horizontal_planes:
    total += h
for v in vertical_planes:
    total += 100*v

print(f"Part 1: {total}") # 21272 -> too low

# Part 2
horizontal_planes = []
vertical_planes = []
for i, block in enumerate(blocks):
    for y in range(1,len(block)):
        if count_v_smudges(block, y) == 1:
            if DEBUG:
                print(f"block {i} new axis y={y}:")
            vertical_planes.append(y)
            break
    else:
        for x in range(1,len(block[0])):
            if count_h_smudges(block, x) == 1:
                if DEBUG:
                    print(f"block {i} new axis x={x}")
                horizontal_planes.append(x)
                break
        else:
            print(f"not symmetrical! {block}")
            for line in block:
                print(line)

total = 0
for h in horizontal_planes:
    total += h
for v in vertical_planes:
    total += 100*v

print(f"Part 2: {total}")
