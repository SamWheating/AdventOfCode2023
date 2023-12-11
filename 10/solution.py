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


def mark_edges(board: List[List[str]]) -> List[List[str]]:
    # marks any non-pipe spots around the edge of the board as outside.
    # this has side affects, as it modifies the original list.
    for y in [0, len(board) - 1]:
        for x in range(len(board[0])):
            if board[y][x] == ".":
                board[y][x] = "O"

    for y in range(len(board)):
        for x in [0, len(board[0]) - 1]:
            if board[y][x] == ".":
                board[y][x] = "O"

    return board


def flood(board: List[List[str]], y: int, x: int) -> List[List[str]]:
    edges = [(y, x)]  # all of the nodes marked in the previous iteration
    visited = set()  # all of the nodes to mark at the end
    inside = True  # are these inside or outside
    while True:
        next_edges = set()
        for node in edges:
            for y, x in [  # four surrounding nodes
                (node[0] - 1, node[1]),
                (node[0] + 1, node[1]),
                (node[0], node[1] - 1),
                (node[0], node[1] + 1),
            ]:
                if y < 0 or y > len(board) - 1 or x < 0 or x > len(board[0]) - 1:
                    continue
                if board[y][x] == "." and (y, x) not in visited:
                    next_edges.add((y, x))
                if (
                    board[y][x] == "O"
                ):  # this block of nodes is connected to the outside
                    inside = False

        visited.update(edges)
        edges = next_edges
        if len(edges) == 0:
            break

    # now mark all of the tiles as either inside or outside
    mark = "I" if inside else "O"
    for y, x in visited:
        board[y][x] = mark

    return board


def triple_board(board: List[List[str]]) -> List[List[str]]:
    """
    scales up the board, turning something like

    F-7
    |.|
    L-J

    into :

    .........
    .FF---77.
    .F.....7.
    .|.....|.
    .|.....|.
    .|.....|.
    .L.....J.
    .LL---JJ.
    .........

    since this allows for flood filling between the gaps between ||, etc

    Also preserves the original symbols for easier debugging / viz.
    """

    new_board = [["." for _ in range(len(board[0]) * 3)] for _ in range(len(board) * 3)]
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == "-":
                new_board[y * 3 + 1][x * 3] = "-"
                new_board[y * 3 + 1][x * 3 + 1] = "-"
                new_board[y * 3 + 1][x * 3 + 2] = "-"

            elif board[y][x] == "|":
                new_board[y * 3][x * 3 + 1] = "|"
                new_board[y * 3 + 1][x * 3 + 1] = "|"
                new_board[y * 3 + 2][x * 3 + 1] = "|"

            elif board[y][x] == "F":
                new_board[y * 3 + 2][x * 3 + 1] = "F"
                new_board[y * 3 + 1][x * 3 + 1] = "F"
                new_board[y * 3 + 1][x * 3 + 2] = "F"

            elif board[y][x] == "7":
                new_board[y * 3 + 2][x * 3 + 1] = "7"
                new_board[y * 3 + 1][x * 3 + 1] = "7"
                new_board[y * 3 + 1][x * 3] = "7"

            elif board[y][x] == "J":
                new_board[y * 3][x * 3 + 1] = "J"
                new_board[y * 3 + 1][x * 3 + 1] = "J"
                new_board[y * 3 + 1][x * 3] = "J"

            elif board[y][x] == "L":
                new_board[y * 3][x * 3 + 1] = "L"
                new_board[y * 3 + 1][x * 3 + 1] = "L"
                new_board[y * 3 + 1][x * 3 + 2] = "L"

    return new_board


def count_3x3_squares(board: List[List[str]], char="I") -> int:
    total = 0
    for y in range(len(board) // 3):
        for x in range(len(board[y]) // 3):
            empty = True
            for dy in range(3 * y, 3 * y + 3):
                for dx in range(3 * x, 3 * x + 3):
                    if board[dy][dx] != char:
                        empty = False
            if empty:
                total += 1

    return total


def count_enclosed_squares(board: List[List[str]]) -> int:
    """
    1) mark all of the non-pipe edges as outside
    2) flood fill every single non-visited node
    3) return the total number of I squares
    """

    board = triple_board(board)
    board = mark_edges(board)
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == ".":
                board = flood(board, y, x)

    return count_3x3_squares(board, "I")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        file = "test_input.txt"
        STARTING_TILE = (
            "F"  # just gonna hardcode this, not worth the time to implement it
        )
        STARTING_DIRECTION = (0, 1)  # >
    else:
        file = "input.txt"
        STARTING_TILE = "|"
        STARTING_DIRECTION = (1, 0)  # ^

    with open(file) as inputfile:
        lines = [l.strip("\n") for l in inputfile.readlines()]

    # build a maze from the input rows
    init_x, init_y = 0, 0
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
    x, y = init_x, init_y
    dist = 0
    direction = STARTING_DIRECTION
    board = [["." for _ in range(len(lines[0]))] for _ in range(len(lines))]
    while True:
        # step position then rotate according to tile + direction
        board[y][x] = maze[y][x]
        y, x = y + direction[0], x + direction[1]
        dist += 1
        direction = TILES_TO_DIRECTIONS[maze[y][x]][direction]
        if x == init_x and y == init_y:
            break

    print(f"Part 1: {dist//2}")  # Its a loop, so the furthest point is halfway

    print(f"Part 2{count_enclosed_squares(board)}")
