# moving tests out to their own file...

from solution import (
    mark_edges,
    flood,
    count_enclosed_squares,
    triple_board,
    count_3x3_squares,
)

test_board = [
    [".", "F", "-", "7"],
    [".", "|", ".", "|"],
    [".", "L", "-", "J"],
    [".", ".", ".", "."],
]

assert mark_edges(test_board) == [
    ["O", "F", "-", "7"],
    ["O", "|", ".", "|"],
    ["O", "L", "-", "J"],
    ["O", "O", "O", "O"],
]

# Testing the flood-fill implementation

test_board = [
    ["◼️", "◼️", "◼️", "◼️"],
    ["◼️", ".", ".", "◼️"],
    ["◼️", "◼️", ".", "◼️"],
    [".", "◼️", "◼️", "◼️"],
]

flood(test_board, 1, 1)

assert flood(test_board, 1, 1) == [
    ["◼️", "◼️", "◼️", "◼️"],
    ["◼️", "I", "I", "◼️"],
    ["◼️", "◼️", "I", "◼️"],
    [".", "◼️", "◼️", "◼️"],
]


test_board = [
    ["◼️", "◼️", "◼️", "◼️"],
    ["◼️", ".", ".", "◼️"],
    ["◼️", ".", ".", "◼️"],
    ["◼️", "◼️", "O", "◼️"],
]

flood(test_board, 1, 1)

assert test_board == [
    ["◼️", "◼️", "◼️", "◼️"],
    ["◼️", "O", "O", "◼️"],
    ["◼️", "O", "O", "◼️"],
    ["◼️", "◼️", "O", "◼️"],
]

assert count_enclosed_squares([["F", "-", "7"], ["|", ".", "|"], ["L", "-", "J"]]) == 1

# testing scaling up the board

assert triple_board([["-"]]) == [[".", ".", "."], ["-", "-", "-"], [".", ".", "."]]

assert triple_board([["|"]]) == [[".", "|", "."], [".", "|", "."], [".", "|", "."]]

assert triple_board([["F"]]) == [[".", ".", "."], [".", "F", "F"], [".", "F", "."]]

assert triple_board([["L"]]) == [[".", "L", "."], [".", "L", "L"], [".", ".", "."]]

assert triple_board([["J"]]) == [[".", "J", "."], ["J", "J", "."], [".", ".", "."]]

assert triple_board([["7"]]) == [[".", ".", "."], ["7", "7", "."], [".", "7", "."]]

expected = [
    list(row)
    for row in """
.........
.FF---77.
.F.....7.
.|.....|.
.|.....|.
.|.....|.
.L.....J.
.LL---JJ.
.........
""".split(
        "\n"
    )
    if len(row) != 0
]

assert triple_board([["F", "-", "7"], ["|", ".", "|"], ["L", "-", "J"]]) == expected

assert count_3x3_squares([[".", ".", "."], [".", ".", "."], [".", ".", "."]], ".") == 1
assert count_3x3_squares([[".", ".", "."], [".", ".", "."], [".", ".", "F"]], ".") == 0

assert count_3x3_squares(triple_board([[".", "."], [".", "."]]), ".") == 4
assert count_3x3_squares(triple_board([["-", "."], [".", "-"]]), ".") == 2

test_board = [
    list(row)
    for row in """
...........
.F-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
""".replace(
        ".", "."
    ).split(
        "\n"
    )
    if len(row) != 0
]

assert count_enclosed_squares(test_board) == 4

test_board = [
    list(row)
    for row in """
..........
.F------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........
""".replace(
        ".", "."
    ).split(
        "\n"
    )
    if len(row) != 0
]

assert count_enclosed_squares(test_board) == 4

test_board = [
    list(row)
    for row in """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJF7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
""".replace(
        ".", "."
    ).split(
        "\n"
    )
    if len(row) != 0
]

assert count_enclosed_squares(test_board) == 8
