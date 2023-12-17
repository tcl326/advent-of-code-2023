import collections
from typing import List

directions = {
    'r': (0, 1),
    'l': (0, -1),
    'u': (-1, 0),
    'd': (1, 0),
}


def part1(layout: List[str], start=(0, 0, 'r')) -> int:
    seen = collections.defaultdict(set)
    n = len(layout)
    m = len(layout[0])
    queue = [start]
    while queue:
        i, j, d = queue.pop()
        seen[(i, j)].add(d)
        nd = []
        if layout[i][j] == ".":
            nd.append(d)
        elif layout[i][j] == "\\":
            if d == "r":
                nd.append("d")
            elif d == "l":
                nd.append("u")
            elif d == "u":
                nd.append("l")
            else:
                nd.append("r")
        elif layout[i][j] == "/":
            if d == "r":
                nd.append("u")
            elif d == "l":
                nd.append("d")
            elif d == "u":
                nd.append("r")
            else:
                nd.append("l")
        elif layout[i][j] == "-":
            if d == "u" or d == "d":
                nd.append("l")
                nd.append("r")
            else:
                nd.append(d)
        else:
            if d == "l" or d == "r":
                nd.append("u")
                nd.append("d")
            else:
                nd.append(d)
        for ind in nd:
            di, dj = directions[ind]
            ni, nj = di + i, dj + j
            if ni < 0 or ni >= n or nj < 0 or nj >= m:
                continue
            if (ni, nj) in seen and ind in seen[(ni, nj)]:
                continue
            queue.append((ni, nj, ind))
    # print(seen)                 
    return len(seen)


def part2(layout):
    n = len(layout)
    m = len(layout[0])
    res = 0
    for i in range(n):
        res = max(res, part1(layout, start=(i, 0, "r")))
        res = max(res, part1(layout, start=(i, m - 1, "l")))
    
    for j in range(m):
        res = max(res, part1(layout, start=(0, j, "d")))
        res = max(res, part1(layout, start=(n - 1, j, "u")))
    
    return res



if __name__ == "__main__":
    file_name = "d16-input.text"
    layout = []
    with open(file_name, "r") as f:
        line = f.readline()
        while line:
            layout.append(line.strip())
            line = f.readline()
    
    print(part1(layout))
    print(part2(layout))