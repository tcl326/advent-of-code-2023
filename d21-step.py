from typing import List, Tuple
import tqdm
import heapq


def get_start(maze: List[str]) -> Tuple[int, int]:
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == "S":
                return i, j
    return -1, -1


def part1(maze: List[str], steps: int = 64, start=None):
    if not start:
        si, sj = get_start(maze)
    else:
        si, sj = start
    step = 0
    seen = set([(step, si, sj)])
    queue = [(step, si, sj)]
    p_s = -1
    while True:
        s, i, j = heapq.heappop(queue)
        if s == steps:
            return len(queue) + 1
        if s != p_s:
            # print(s, len(queue) + 1)
            p_s = s
        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            ni, nj = i + di, j + dj
            if ni < 0 or ni >= len(maze) or nj < 0 or nj >= len(maze[0]) or maze[ni][nj] == "#":
                continue
            if (s + 1, ni, nj) in seen:
                continue
            seen.add((s + 1, ni, nj))
            heapq.heappush(queue, (s + 1, ni, nj))


def part2(maze: List[str], steps: int = 26501365):
    si, sj = get_start(maze)
    n = len(maze)
    m = len(maze[0])
    
    q = set([(si, sj)])
    res = []
    for it in tqdm.tqdm(range(1, 100_000)):
        nq = set()
        for i, j in q:
            for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                ni, nj = i + di, j + dj
                if maze[ni % n][nj % m] != "#":
                    nq.add((ni, nj))
        q = nq
        if it % n == steps % n:
            res.append(len(q))
        if len(res) == 3:
            break
    
    
    def f(n: int, a):
        a0, a1, a2 = a
        b0 = a0
        b1 = a1 - a0
        b2 = a2 - a1
        return b0 + b1 * n + (n * (n - 1) // 2) * ( b2 - b1)
    
    return f(steps // n, res)



if __name__ == "__main__":
    file_name = "d21-input.text"
    maze = []
    with open(file_name, "r") as f:
        line = f.readline()
        while line:
            maze.append(line.strip())
            line = f.readline()

    print(part1(maze, 65, (130, 0)))
    print(part2(maze))
