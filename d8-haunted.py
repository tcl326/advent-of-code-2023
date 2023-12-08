from typing import Tuple
import math

def parse_island(line: str) -> Tuple[str, str, str]:
    return line[0:3], line[7:10], line[12:15]


def part1(direction, islands) -> int:
    res = 0
    curr = "AAA"
    while curr != "ZZZ":
        d = direction[res % len(direction)]
        # print(curr, d, islands[curr])
        if d == "L":
            n = islands[curr][0]
        else:
            n = islands[curr][1]
        res += 1
        curr = n
    
    return res

def part2(direction, islands) -> int:
    res = 0
    curr_islands = [a for a in islands.keys() if a[-1] == "A"]
    all_reached = False
    reached_indices = {}
    while not all_reached:
        n_islands = []
        d = direction[res % len(direction)]
        reached = 0
        res += 1
        for i, c in enumerate(curr_islands):
            if d == "L":
                n = islands[c][0]
            else:
                n = islands[c][1]
            n_islands.append(n)
            if n[-1] == "Z":
                reached += 1
                if i not in reached_indices:
                    reached_indices[i] = res
        if len(reached_indices) == len(curr_islands):
            return math.lcm(*list(reached_indices.values()))
        curr_islands = n_islands
    return res

def product(lst):
    p = 1
    for i in lst:
        p *= i
    return p


if __name__ == "__main__":
    file_name = "d8-input.text"
    # file_name = "test_input.text"
    islands = {}

    with open(file_name, "r") as f:
        direction = f.readline().strip()
        f.readline()

        line = f.readline()
        while line:
            island, left, right = parse_island(line)
            islands[island] = (left, right)
            line = f.readline()

    print(part1(direction, islands))
    print(part2(direction, islands))
    print(product([2, 2, 2, 2, 3, 3, 11, 17, 43, 47, 59, 67, 71, 79, 89, 109]))