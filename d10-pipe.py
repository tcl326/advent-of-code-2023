from typing import List


connections = {
    "|": [(-1, 0), (1, 0)],
    "-": [(0, 1), (0, -1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(1, 0), (0, -1)],
    "F": [(1, 0), (0, 1)],
    ".": [],
}


def part1(maze: List[str]):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == "S":
                si = i
                sj = j
    walled = [["." for _ in range(len(maze[0]))] for _ in range(len(maze))]
    seen = set()
    travelled = 0
    c_set = set([(si, sj)])
    while c_set:
        n_set = set()
        for i, j in c_set:
            if maze[i][j] in ["|", "L", "J"]:
                walled[i][j] = "!"
            else:
                walled[i][j] = "-"
            seen.add((i, j))
            if maze[i][j] == "S":
                for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    if i + di < 0 or i + di >= len(maze) or j + dj < 0 or j + dj >= len(maze[i]):
                        continue
                    for ci, cj in connections[maze[i + di][j + dj]]:
                        if di + ci == 0 and cj + dj == 0:
                            n_set.add((i + di, j + dj))
            else:
                for di, dj in connections[maze[i][j]]:
                    if i + di < 0 or i + di >= len(maze) or j + dj < 0 or j + dj >= len(maze[i]):
                        continue
                    if (i + di, j + dj) not in seen:
                        n_set.add((i + di, j + dj))
        c_set = n_set
        travelled += 1

    return travelled - 1, walled


def part2(walled: List[List[str]]):
    area = 0
    for i in range(len(walled)):
        wall_count = 0
        for j in range(len(walled[i])):
            if walled[i][j] == ".":
                if wall_count % 2 == 1:
                    area += 1
                    walled[i][j] = "0"
            if walled[i][j] == "!":
                wall_count += 1
    return area



if __name__ == "__main__":
    file_name = 'd10-input.text'
    # file_name = "test_input.text"
    maze = []
    with open(file_name, 'r') as f:
        line = f.readline()
        while line:
            maze.append(line.strip())
            line = f.readline()

    res, walled = part1(maze)
    print("part1:", res)
    print(part2(walled))
    for w in walled:
        print(w)
