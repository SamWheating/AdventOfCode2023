import sys
from typing import List

# for a given tile, what are the mappings of incoming -> outgoing direction
# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.

# using this coord system
#      
#       -y
#        |
#  -x ---+--- +x
#        |
#       +y

TILES_TO_DIRECTIONS = {
    "|": {
        (1, 0): (1, 0),
        (-1, 0): (-1, 0)
    },
    "-": {
        (0, 1): (0, 1),
        (0, -1): (0, -1)
    },
    "L": {
        (1, 0): (0, 1), # v -> >
        (0, -1): (-1, 0)  # < -> ^
    },
    "J": {
        (1, 0): (0, -1), # v -> <
        (0, 1): (-1, 0)  # > -> ^
    },
    "7": {
        (-1, 0): (0, -1), # ^ -> <
        (0, 1): (1, 0)  # > -> v
    },
    "F": {
        (-1, 0): (0, 1), # ^ -> >
        (0, -1): (1, 0)  # < -> v
    },
}

# board is a 2d array of only parts of the maze which are actually visited.
# I = inside
# O = outside
# N = not visited

def mark_edges(board: List[List[str]]) -> None:
    # marks any non-pipe spots around the edge of the board as outside.
    # returns None (all changes in-place)
    for y in [0, len(board)-1]:
        for x in range(len(board[0])):
            if board[y][x] == "N":
                board[y][x] = "O"
    
    for y in range(len(board)):
        for x in [0, len(board[0])-1]:
            if board[y][x] == "N":
                board[y][x] = "O"

def flood(board: List[List[str]], y: int, x: int) -> None:
    edges = [(y,x)] # all of the nodes marked in the previous iteration
    visited = [] # all of the nodes to mark at the end
    inside = True # are these inside or outside
    while True:
        next_edges = []
        for node in edges:
            for y,x in [ # four surrounding nodes
                (node[0]-1,node[1]),
                (node[0]+1,node[1]),
                (node[0],node[1]-1),
                (node[0],node[1]+1)
            ]:
                if y < 0 or y > len(board)-1 or x < 0 or x > len(board[0])-1:
                    continue
                if board[y][x] == "N" and (y,x) not in visited:
                    next_edges.append((y,x))
                if board[y][x] == "O": # this block of nodes is connected to the outside
                    inside = False

        visited.extend(edges)
        edges = next_edges
        if len(edges) == 0:
            break

    # now mark all of the tiles as either inside or outside
    mark = "I" if inside else "O"
    for y,x in visited:
            board[y][x] = mark

def count_enclosed_squares(board: List[List[str]]) -> int:
    """
    1) mark all of the non-pipe edges as outside
    2) flood fill every single non-visited node
    3) return the total number of I squares 
    """
    mark_edges(board)
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == "N":
                flood(board, y, x)

    total = 0
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == "I":
                total += 1

    return total


if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        file = "test_input.txt"
        STARTING_TILE = "F" # just gonna hardcode this, not worth implementing it
        STARTING_DIRECTION = (0,1) # >
    else:
        file = "input.txt"
        STARTING_TILE = "|"
        STARTING_DIRECTION = (1,0) # ^

    with open(file) as inputfile:
        lines = [l.strip("\n") for l in inputfile.readlines()]

    # build a maze from the input rows
    init_x, init_y = 0,0
    maze = {y: {} for y in range(len(lines))}
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == "S":
                maze[y][x] = STARTING_TILE
                init_x = x
                init_y = y
            else:
                maze[y][x] = lines[y][x]

    # follow the maze and count the distance
    x,y = init_x, init_y
    dist = 0
    direction = STARTING_DIRECTION
    board = [['N' for _ in range(len(lines[0]))] for _ in range(len(lines))]
    while True:
        # step position then rotate according to tile + direction
        board[y][x] = maze[y][x]
        y,x = y + direction[0], x + direction[1]
        dist += 1
        direction = TILES_TO_DIRECTIONS[maze[y][x]][direction]
        if x == init_x and y == init_y:
            break

    print(f"Part 1: {dist//2}") # Its a loop, so the furthest point is halfway
