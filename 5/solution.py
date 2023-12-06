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

@dataclass
class MapItem:
    dest_start: int
    source_start: int
    length: int

mapitem = MapItem(1,2,3)

assert mapitem.dest_start == 1
assert mapitem.source_start == 2
assert mapitem.length == 3

class Mapping:

    def __init__(self, inputlines: List[str]):
        self.mappings = []
        for line in inputlines:
            d,s,l = (int(s) for s in line.split())
            self.mappings.append(MapItem(d,s,l))

    def translate(self, input: int) -> int:
        for m in self.mappings:
            if input >= m.source_start and input < (m.source_start + m.length): # 3054616754
                return m.dest_start + (input - m.source_start)

        return input
    
    def __repr__(self):
        return "\n".join([f"{m.dest_start} {m.source_start} {m.length}" for m in self.mappings])
    
test_mapping = Mapping(["50 98 2", "52 50 48"])
assert test_mapping.translate(0) == 0
assert test_mapping.translate(1) == 1
assert test_mapping.translate(49) == 49
assert test_mapping.translate(50) == 52
assert test_mapping.translate(51) == 53
assert test_mapping.translate(98) == 50

# parsing:
seeds = [int(s) for s in lines[0].split(": ")[1].split()]

# parse input into mappings
seed_soil = Mapping(
    lines[lines.index("seed-to-soil map:")+1:lines.index("soil-to-fertilizer map:")-1]
)
soil_fertilizer = Mapping(
    lines[lines.index("soil-to-fertilizer map:")+1:lines.index("fertilizer-to-water map:")-1]
)
fertilizer_water = Mapping(
    lines[lines.index("fertilizer-to-water map:")+1:lines.index("water-to-light map:")-1]
)
water_light = Mapping(
    lines[lines.index("water-to-light map:")+1:lines.index("light-to-temperature map:")-1]
)
light_temperature = Mapping(
    lines[lines.index("light-to-temperature map:")+1:lines.index("temperature-to-humidity map:")-1]
)
temperature_humidity = Mapping(
    lines[lines.index("temperature-to-humidity map:")+1:lines.index("humidity-to-location map:")-1]
)
humidity_location = Mapping(
    lines[lines.index("humidity-to-location map:")+1:]
)

min_seed = 10**20
for seed in seeds:
    soil = seed_soil.translate(seed)
    fertilizer = soil_fertilizer.translate(soil)
    water = fertilizer_water.translate(fertilizer)
    light = water_light.translate(water)
    temperature = light_temperature.translate(light)
    humidity = temperature_humidity.translate(temperature)
    location = humidity_location.translate(humidity)

    if location < min_seed:
        min_seed = location

print(f"Part 2: {min_seed}")

# Part 2:
# did some napkin math and realized that with a simple brute force I'd only have to calculate ~1.5B values. 
# Computers are fast so I just let it run in the background, where it finished after ~3 hours.
# TODO: fix this (obviously)

from datetime import datetime
min_seed = 10**20
processed = 0
for i in range(0, len(seeds), 2):
    base = seeds[i]
    length = seeds[i+1]
    for seed in range(base, base+length):
        soil = seed_soil.translate(seed)
        fertilizer = soil_fertilizer.translate(soil)
        water = fertilizer_water.translate(fertilizer)
        light = water_light.translate(water)
        temperature = light_temperature.translate(light)
        humidity = temperature_humidity.translate(temperature)
        location = humidity_location.translate(humidity)

        if location < min_seed:
            min_seed = location

        if processed % 1000000 == 0:
            print(datetime.now(), processed)
        processed += 1

print(f"Part 2: {min_seed}")
