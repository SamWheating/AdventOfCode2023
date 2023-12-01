import sys

if len(sys.argv) > 1 and sys.argv[1] == "--test":
    file = "test_input.txt"
else:
    file = "input.txt"

with open(file) as inputfile:
    lines = [l.strip('\n') for l in inputfile.readlines()]

total = 0
for line in lines:
    first = last = None
    for c in line:
        if c.isdigit():
            if first is None:
                first = int(c)
            last = int(c)

    total = total + 10*first + last

print(f"Part 1: {total}")

total = 0
for line in lines:
    line = line.replace("one", "one1one")
    line = line.replace("two", "two2two")
    line = line.replace("three", "three3three")
    line = line.replace("four", "four4four")
    line = line.replace("five", "five5five")
    line = line.replace("six", "six6six")
    line = line.replace("seven", "seven7seven")
    line = line.replace("eight", "eight8eight")
    line = line.replace("nine", "nine9nine")

    first = last = None
    for c in line:
        if c.isdigit():
            if first is None:
                first = int(c)
            last = int(c)

    total = total + 10*first + last

print(f"Part 2: {total}")
