import sys
from typing import List, Dict

if len(sys.argv) > 1 and sys.argv[1] == "--test":
    file = "test_input.txt"
else:
    file = "input.txt"

with open(file) as inputfile:
    lines = [l.strip("\n") for l in inputfile.readlines()]


def hash(seq: str) -> int:
    total = 0
    for c in seq:
        total = ((total + ord(c)) * 17) % 256
    return total

assert hash("HASH") == 52
assert hash("rn=1") == 30

class Lens:
    def __init__(self, label: str, length: int):
        self.label = label
        self.length = length


class HashMap:
    def __init__(self):
        self.buckets: Dict[int, List[Lens]] = {i: [] for i in range(256)}

    def update(self, entry: str):
        """
        assumes that every entry matches
        "[a-z]+=[0-9]" or "[a-z]+-"
        """
        label = "".join([c for c in entry if c.isalpha()])
        bucket = hash(label)
        if "=" in entry:
            length = int(entry.split("=")[1])
            self.insert(bucket, Lens(label, length))

        elif "-" in entry:
            self.remove(bucket, label)

    def insert(self, bucket: int, lens: Lens) -> None:
        for i in range(len(self.buckets[bucket])):
            if self.buckets[bucket][i].label == lens.label:
                self.buckets[bucket][i] = lens
                return

        self.buckets[bucket].append(lens)

    def remove(self, bucket: int, label: str) -> None:
        for i in range(len(self.buckets[bucket])):
            if self.buckets[bucket][i].label == label:
                del self.buckets[bucket][i]
                return

    @property
    def power(self):
        power = 0
        for bucket in self.buckets.keys():
            for i in range(len(self.buckets[bucket])):
                power += (bucket + 1) * (i + 1) * self.buckets[bucket][i].length
        return power


if __name__ == "__main__":

    # Part 1
    total = sum([hash(seq) for seq in  lines[0].split(",")])
    print(f"Part 1: {total}")

    # Part 2:
    hm = HashMap()
    for seq in lines[0].split(","):
        hm.update(seq)

    print(f"Part 2: {hm.power}")
