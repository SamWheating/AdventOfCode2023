import sys
from typing import Tuple, Dict

from re import match

def count_groups(springs: str) -> Tuple[int,int]:
    # Counts the number of existing groups from the left side of the string
    groups = []
    current = 0
    for s in springs:
        if s == "#":
            current += 1
        else:
            if current != 0:
                groups.append(current)
                current = 0 
    
    if current != 0:
        groups.append(current)
    
    return tuple(groups)

assert count_groups("##.##.##?????") == (2,2,2)
assert count_groups("??????") == ()
assert count_groups("#.#.#") == (1,1,1)

def is_complete(springs: str, reqs: Tuple[int]) -> bool:
    return count_groups(springs) == reqs

assert is_complete("##.##.##?????", (2,2,2))
assert is_complete("#.#.#", (1,1,1))
assert not is_complete("??????", (1,1))

def gen_partial_regex(reqs: Tuple[int]):
    """This provides a regex expression which ensures there's still a solution or a possible soluition
    
    The max number of groups is capped since otherwise greedy regex matches can take _forever_.

    There's probably some sort of optimization here, as a longer regex means more aggresive pruning,
    but also more time spend computing regex matches.
    """
    MAX_N_GROUPS = 3

    regex = "^[.?]*" # since the leading ... are optional
    for group in reqs[:min(MAX_N_GROUPS, len(reqs))]:
        regex += f"[#?]{{{group}}}[.?]+"
    regex = regex[:-1] + "*" # since the tailing ... are optional
    if len(reqs) <= MAX_N_GROUPS:
        regex += "$" # this regex should validate the whole pattern, so we can anchor the end.
    return regex

r = gen_partial_regex((2,2,2))
assert match(r, "##.##.##??????")
assert match(r, "?????????")

def get_subproblem(springs, reqs) -> Tuple[str, Tuple[int]]:
    """removes the solved part of the problem, as it has no affect on the result.
    
    i.e get_subproblem("##.????", (2,1,1)) -> "????", (1,1)

    This will also increase cache hit rate
    """
    immutable_up_to = 0
    counting = False
    for i, s in enumerate(springs):
        if s == "#":
            counting = True
        if s == ".":
            immutable_up_to = i + 1
            if counting:
                reqs = reqs[1:] # remove one of the groups
                counting = False
        if s == "?":
            break
    
    return springs[immutable_up_to:], reqs

assert get_subproblem("##.????", (2,1,1)) == ("????", (1,1))
assert get_subproblem("#.............???", (1,2)) == ("???", (2,))
assert get_subproblem("#.......?.....???", (1,2)) == ("?.....???", (2,))
assert get_subproblem("?", (1,)) == ("?", (1,))


def count_ways(springs: str, reqs: Tuple[int], memo: Dict[str, int] = None) -> int:    

    if memo is None:
        memo = {}

    if (reqs, springs) in memo:
        return memo[(reqs, springs)]

    pattern = gen_partial_regex(reqs)
    if match(pattern, springs): # quick check: is this still a valid path to traverse?

        if is_complete(springs, reqs): # end of recursion, this is a complete solution.
            memo[(reqs, springs)] = 1
            return 1

        # reduce the problem by eliminating any completed groups (no ?, .-delimited) from springs and reqs
        #   i.e: count_ways(###.##.?????, (3,2,1,1)) -> count_ways("?????", (1,1))
        # 
        # then solve rescursively and memoize the solutions.
        #
        # then cache all of the partial solutions in memo:
        #   i.e memo = {
        #          ("#####", (1,1)): 6
        #          ("##", (1,)): 2
        #       }
        #
        # since we've already pre-validated this solution, we can avoid a lot of checking

        total = 0

        subsprings, subreqs = get_subproblem(springs, reqs)

        # add the next group:
        if all([s in "?#" for s in subsprings[:subreqs[0]]]):
            if len(subsprings) == subreqs[0] or subsprings[subreqs[0]] in "?.":
            # the first n elements can just be the next group of springs
                total += count_ways(
                    subsprings[subreqs[0]+1:], subreqs[1:], memo
                )


        if subsprings[0] in ".?": # do we have the option of adding a period here?
            total += count_ways(
                subsprings[1:], subreqs, memo
            )

        memo[(reqs, springs)] = total
        return total

    memo[(reqs, springs)] = 0
    return 0

assert count_ways("##.##", (2,2)) == 1
assert count_ways("#####", (2,2)) == 0
assert count_ways("?###????????", (3,2,1)) == 10, count_ways("?###????????", (3,2,1))

def count_ways_5x(springs: str, reqs: Tuple[int], memo: Dict[str, int] = None) -> int:
    """convenience function for pt 2"""
    springs = "?".join([springs]*5)
    reqs *= 5
    return count_ways(springs, reqs, memo)

assert count_ways_5x("???.###", (1,1,3), {}) == 1
assert count_ways_5x(".??..??...?##.", (1,1,3), {}) == 16384
assert count_ways_5x("?#?#?#?#?#?#?#?", (1,3,1,6), {}) == 1
assert count_ways_5x("????.#...#...", (4,1,1), {}) == 16
assert count_ways_5x("?###????????", (3,2,1), {}) == 506250

if __name__ == "__main__":
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        file = "test_input.txt"
    else:
        file = "input.txt"

    with open(file) as inputfile:
        lines = [l.strip("\n") for l in inputfile.readlines()]

    # Part 1
    total = 0
    for line in lines:
        springs = line.split(" ")[0]
        reqs = tuple(int(c) for c in line.split(" ")[1].split(","))
        total += count_ways(springs, reqs)

    print(f"Part 1: {total}")

    # Part 2:
    total = 0
    for i, line in enumerate(lines):
        springs = line.split(" ")[0]
        reqs = tuple(int(c) for c in line.split(" ")[1].split(","))
        total += count_ways_5x(springs, reqs, None)

    print(f"Part 2: {total}") # should be 525152 on test input
