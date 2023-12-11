from typing import List


import itertools
import heapq

def get_shortest_distance(g1, g2, universe, r_no_galaxy, c_no_galaxy, expansion=2):
    def d(g1, g2):
        return abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
    ei, ej = g2
    scores = [(d(g1, g2), 0, g1)]
    while scores:
        _, step, (i, j) = heapq.heappop(scores)
        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            ni, nj = i + di, j + dj
            if ni < 0 or ni >= len(universe) or nj < 0 or nj >= len(universe[i]):
                continue
            cost = expansion if ni in r_no_galaxy or nj in c_no_galaxy else 1
            if ni == ei and nj == ej:
                return step + cost
            heapq.heappush(scores, (d((ni, nj), g2), step + cost, (ni, nj)))
    return -1



def part1(universe: List[str]) -> int:
    rows_without_galaxy = set([i for i in range(len(universe))])
    columns_without_galaxy = set([i for i in range(len(universe[0]))])
    galaxies = []
    for i in range(len(universe)):
        for j in range(len(universe[i])):
            if universe[i][j] == "#":
                rows_without_galaxy.discard(i)
                columns_without_galaxy.discard(j)
                galaxies.append((i, j))
    
    res = 0
    for c in itertools.combinations(galaxies, 2):
        res += get_shortest_distance(c[0], c[1], universe, rows_without_galaxy, columns_without_galaxy)
        print(c, res)
    return res

def part2(universe: List[str]) -> int:
    rows_without_galaxy = set([i for i in range(len(universe))])
    columns_without_galaxy = set([i for i in range(len(universe[0]))])
    galaxies = []
    for i in range(len(universe)):
        for j in range(len(universe[i])):
            if universe[i][j] == "#":
                rows_without_galaxy.discard(i)
                columns_without_galaxy.discard(j)
                galaxies.append((i, j))
    
    res = 0
    for c in itertools.combinations(galaxies, 2):
        print(c)
        res += get_shortest_distance(c[0], c[1], universe, rows_without_galaxy, columns_without_galaxy, expansion=1_000_000)
    return res


if __name__ == "__main__":
    file_name = "d11-input.text"
    universe = []
    with open(file_name, "r") as f:
        line = f.readline().strip()
        while line:
            universe.append(line)
            line = f.readline().strip()
    print(part1(universe))
    print(part2(universe))