import sys
import math


if len(sys.argv) > 1 and sys.argv[1] == "--test":
    file = "test_input.txt"
else:
    file = "input.txt"

with open(file) as inputfile:
    lines = [l.strip("\n") for l in inputfile.readlines()]

steps = lines[0]

map = {}
for line in lines[2:]:
    line = line.replace("=","").replace("(","").replace(")","").replace(",","")
    map[line.split()[0]] = {"left": line.split()[1], "right": line.split()[2]}

node = "AAA"
num_steps = 0
while True:
    for step in steps:
        if step == "L":
            node = map[node]["left"] 
        elif step == "R":
            node = map[node]["right"] 
    
        num_steps += 1
        if node == "ZZZ":
            break
    if node == "ZZZ":
        break

print("Part 1: ", num_steps)

# Part 2

# find the period of each cycle independently, then take the lowest common multiple

nodes = [node for node in map.keys() if node[-1] == "A"]
periods = []
for node in nodes:
    num_steps = 0
    first_end, second_end = None, None
    while True:
        for step in steps:
            if step == "L":
                node = map[node]["left"] 
            elif step == "R":
                node = map[node]["right"] 

            num_steps += 1

            if node[-1] == "Z":
                if first_end is None:
                    first_end = num_steps
                else:
                    second_end = num_steps
                if second_end is not None:
                    break
        if second_end is not None:
            periods.append(second_end - first_end)
            break

print(f"Part 2: {math.lcm(*periods)}")
