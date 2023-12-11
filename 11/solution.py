import sys

if len(sys.argv) > 1 and sys.argv[1] == "--test":
    file = "test_input.txt"
else:
    file = "input.txt"

with open(file) as inputfile:
    lines = [l.strip("\n") for l in inputfile.readlines()]

map = []
for line in lines:
    if len(line) == line.count("."):
        map.append(list(line))
    map.append(list(line))

new_map = [[] for line in range(len(map))]
for x in range(len(map[0])):
    col = [row[x] for row in map]
    if len(col) == col.count("."):
        for y in range(len(map)):
            new_map[y].append(".")
    for y in range(len(map)):
        new_map[y].append(map[y][x])

map = new_map

galaxies = []
for y in range(len(map)):
    for x in range(len(map[0])):
        if map[y][x] == "#":
            map[y][x] = len(galaxies)
            galaxies.append((y,x))

distance = 0
for a in range(len(galaxies)-1):
    for b in range(a+1, len(galaxies)):
        distance += (abs(galaxies[a][0] - galaxies[b][0]) + abs(galaxies[a][1] - galaxies[b][1])) 

print(f"Part 1: {distance}")

map = [list(line) for line in lines]

galaxies = {}
empty_rows = []
empty_cols = []

# part 2
for y in range(len(lines)):
    if len(lines[y]) == lines[y].count("."):
        empty_rows.append(y)

for x in range(len(map[0])):
    col = [row[x] for row in map]
    if len(col) == col.count("."):
        empty_cols.append(x)

for y in range(len(map)):
    for x in range(len(map[0])):
        if map[y][x] == "#":
            galaxies[len(galaxies)] = (y,x)


new_galaxies = {}
for galaxy in galaxies:
    new_galaxies[galaxy] = (galaxies[galaxy][0], galaxies[galaxy][1])

for row in empty_rows:
    for galaxy in galaxies.keys():
        if galaxies[galaxy][0] > row:
            new_galaxies[galaxy] = (new_galaxies[galaxy][0] + 999999, new_galaxies[galaxy][1])

for col in empty_cols:
    for galaxy in galaxies.keys():
        if galaxies[galaxy][1] > col:
            new_galaxies[galaxy] = (new_galaxies[galaxy][0], new_galaxies[galaxy][1] + 999999)

galaxies = new_galaxies

distance = 0
for a in range(len(galaxies)-1):
    for b in range(a+1, len(galaxies)):
        distance += (abs(galaxies[a][0] - galaxies[b][0]) + abs(galaxies[a][1] - galaxies[b][1])) 

print(f"Part 2: {distance}")
