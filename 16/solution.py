import sys
from typing import List
from collections import defaultdict

class Beam:
    def __init__(self,y=0,x=0,dy=0,dx=0):
        self.y = y
        self.x = x
        self.dy = dy
        self.dx = dx

    def reflect(self, mirror):
        if mirror == "/":
            if (self.dy, self.dx) == (1,0):
                self.dy, self.dx = 0, -1
            elif (self.dy, self.dx) == (-1,0):
                self.dy, self.dx = 0, 1
            elif (self.dy, self.dx) == (0,1):
                self.dy, self.dx = -1, 0
            elif (self.dy, self.dx) == (0,-1):
                self.dy, self.dx = 1, 0
        elif mirror == "\\":
            if (self.dy, self.dx) == (1,0):
                self.dy, self.dx = 0, 1
            elif (self.dy, self.dx) == (-1,0):
                self.dy, self.dx = 0, -1
            elif (self.dy, self.dx) == (0,1):
                self.dy, self.dx = 1, 0
            elif (self.dy, self.dx) == (0,-1):
                self.dy, self.dx = -1, 0

    def split(self, splitter) -> List["Beam"]:

        if self.dy == 0 and self.dx != 0 and splitter == "|":
            return [
                Beam(self.y, self.x, dy=1),
                Beam(self.y, self.x, dy=-1)
            ]
        
        if self.dy != 0 and self.dx == 0 and splitter == "-":
            return [
                Beam(self.y, self.x, dx=1),
                Beam(self.y, self.x, dx=-1)
            ]
        
        return [self]
    
    @property
    def hash(self) -> str:
        # used for deduping
        # use the full hash to determine if a state has been visited before
        # use hash.split("/")[0] when counting total visited tiles
        return f"{self.x}-{self.y}/{self.dx}-{self.dy}"

class Mirrors:
    def __init__(self, width, height, mirrors, y=0, x=-1, dy=0, dx=1):
        self.width = width
        self.height = height
        self.mirrors = mirrors
        first_beam = Beam(y=y, x=x, dy=dy, dx=dx)
        self.beams = [first_beam]
        self.visited = set()

        self.step() # walk onto the board
        self.visited = set()

    def step(self):
        next_beams = []
        for beam in self.beams:

             # if we've already been to this exact position and speed, end this beam
            if beam.hash in self.visited:
                continue

            # log the visit
            self.visited.add(beam.hash)

            # update position
            beam.x += beam.dx
            beam.y += beam.dy

            # remove if off-board
            if beam.x < 0 or beam.x >= self.width:
                continue
            if beam.y < 0 or beam.y >= self.height:
                continue

            mirror = self.mirrors.get((beam.y, beam.x), None)

            # process reflections
            if mirror in {"/", "\\"}:
                beam.reflect(mirror)
                next_beams.append(beam)
            elif mirror in {"|", "-"}:
                next_beams.extend(beam.split(mirror))
            else:
                next_beams.append(beam)

        self.beams = next_beams

    def run(self):
        while True:
            self.step()
            if len(self.beams) == 0:
                return self.energized

    @property
    def energized(self):
        return len(set([h.split("/")[0] for h in self.visited]))

    def __repr__(self):
        """useful for debugging"""
        board = [["." for _ in range(self.width)] for _ in range(self.height)]
        for mirror in self.mirrors:
            board[mirror[0]][mirror[1]] = self.mirrors[mirror]

        for beam in self.beams:
            board[beam.y][beam.x] = "B"
        
        viz = ""
        for row in board:
            viz += "".join(row)
            viz += "\n"

        return viz + f"visited: {len(self.visited)}"


if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        file = "test_input.txt"
    else:
        file = "input.txt"

    with open(file) as inputfile:
        lines = [l.strip("\n") for l in inputfile.readlines()]

    HEIGHT = len(lines)
    WIDTH = len(lines[0])

    map = {}
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if lines[y][x] != ".":
                map[(y,x)] = lines[y][x]

    # Part 1:
    mirrors = Mirrors(height=HEIGHT, width=WIDTH, mirrors=map)
    print(f"Part 1: {mirrors.run()}") # 6922: too high

    # Part 2, run the simulation from every edge position:
    energies = []
    for x in range(WIDTH):
        energies.append(Mirrors(height=HEIGHT, width=WIDTH, mirrors=map, x=x, y=-1, dx=0, dy=1).run())
        energies.append(Mirrors(height=HEIGHT, width=WIDTH, mirrors=map, x=x, y=HEIGHT, dx=0, dy=-1).run())

    for y in range(HEIGHT):
        energies.append(Mirrors(height=HEIGHT, width=WIDTH, mirrors=map, x=-1, y=y, dx=1, dy=0).run())
        energies.append(Mirrors(height=HEIGHT, width=WIDTH, mirrors=map, x=WIDTH, y=y, dx=-1, dy=0).run())


    print(f"Part 2: {max(energies)}")
