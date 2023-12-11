# moving tests out to their own file...

from solution import mark_edges, flood, count_enclosed_squares

test_board = [
                ["N", "F", "-", "7"],
                ["N", "|", "N", "|"],
                ["N", "L", "-", "J"],
                ["N", "N", "N", "N"]
            ]

mark_edges(test_board)

assert test_board == [
                ["O", "F", "-", "7"],
                ["O", "|", "N", "|"],
                ["O", "L", "-", "J"],
                ["O", "O", "O", "O"]
            ]

# Testing the flood-fill implementation

test_board = [
                ["◼️", "◼️", "◼️", "◼️"],
                ["◼️", "N", "N", "◼️"],
                ["◼️", "◼️", "N", "◼️"],
                ["N", "◼️", "◼️", "◼️"]
            ]

flood(test_board, 1, 1)

assert test_board == [
                ["◼️", "◼️", "◼️", "◼️"],
                ["◼️", "I", "I", "◼️"],
                ["◼️", "◼️", "I", "◼️"],
                ["N", "◼️", "◼️", "◼️"]
            ]


test_board = [
                ["◼️", "◼️", "◼️", "◼️"],
                ["◼️", "N", "N", "◼️"],
                ["◼️", "N", "N", "◼️"],
                ["◼️", "◼️", "O", "◼️"]
            ]

flood(test_board, 1, 1)

assert test_board == [
                ["◼️", "◼️", "◼️", "◼️"],
                ["◼️", "O", "O", "◼️"],
                ["◼️", "O", "O", "◼️"],
                ["◼️", "◼️", "O", "◼️"]
            ]


# Testing the full part 2 code

test_board = [
                ["◼️", "◼️", "◼️", "◼️"],
                ["◼️", "N", "N", "◼️"],
                ["◼️", "N", "N", "◼️"],
                ["◼️", "◼️", "◼️", "◼️"]
            ]

assert count_enclosed_squares(test_board) == 4

test_board = [list(row) for row in """
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
""".replace(".", "N").split("\n") if len(row) != 0]

assert count_enclosed_squares(test_board) == 4

test_board = [list(row) for row in """
..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........
""".replace(".", "N").split("\n") if len(row) != 0]

assert count_enclosed_squares(test_board) == 4

test_board = [list(row) for row in """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
""".replace(".", "N").split("\n") if len(row) != 0]

assert count_enclosed_squares(test_board) == 8