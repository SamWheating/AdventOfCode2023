from typing import List
import sys
from dataclasses import dataclass

if len(sys.argv) > 1 and sys.argv[1] == "--test":
    file = "test_input.txt"
else:
    file = "input.txt"

with open(file) as inputfile:
    lines = [l.strip('\n') for l in inputfile.readlines()]

@dataclass
class Game:
    round_id: int
    red: int
    green: int
    blue: int

def parse_round(round: str) -> List[Game]:
    round_id = int(round.split(" ")[1][:-1])
    games = []
    for subgame in round.split(";"):
        counts = {"red": 0, "green": 0, "blue": 0}
        for chunk in subgame.split(", "):
            colour = chunk.split(" ")[-1]
            count = int(chunk.split(" ")[-2])
            counts[colour] += count
    
        games.append(
            Game(round_id, counts["red"], counts["green"], counts["blue"])
        )

    return games

games = parse_round("Game 6: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
assert len(games) == 3
assert games[0].blue == 3
assert games[0].round_id == 6

# part 1:
total = 0
for line in lines:
    for game in parse_round(line):
        if game.red > 12:
            break
        if game.green > 13:
            break
        if game.blue > 14:
            break
    else:
        total += game.round_id

print(f"Part 1: {total}")

# part 2:
total = 0
for line in lines:
    games = parse_round(line)
    red = max([g.red for g in games])
    green = max([g.green for g in games])
    blue = max([g.blue for g in games])

    total += red*green*blue

print(f"Part 2: {total}")
