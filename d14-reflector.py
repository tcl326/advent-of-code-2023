from typing import List

def print_maze(maze):
    for m in maze:
        print(m)
    print()


def tilt_north(maze: List[str]) -> List[str]:
    lowest_y = [0 for _ in range(len(maze[0]))]
    filled = [
        [maze[i][j] if maze[i][j] != "O" else "." for j in range(len(maze[i]))]
            for i in range(len(maze))
    ]
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == "#":
                lowest_y[j] = i + 1
            if maze[i][j] == "O":
                filled[lowest_y[j]][j] = "O"
                lowest_y[j] += 1
    return filled

def tilt_south(maze: List[str]) -> List[str]:
    highest_y = [len(maze) - 1 for _ in range(len(maze))]
    filled = [
        [maze[i][j] if maze[i][j] != "O" else "." for j in range(len(maze[i]))]
            for i in range(len(maze))
    ]
    for i in range(len(maze) - 1, -1, -1):
        for j in range(len(maze[i]) - 1, -1, -1):
            if maze[i][j] == "#":
                highest_y[j] = i - 1
            if maze[i][j] == "O":
                filled[highest_y[j]][j] = "O"
                highest_y[j] -= 1
    return filled

def tilt_west(maze: List[str]) -> List[str]:
    lowest_x = [0 for _ in range(len(maze))]
    filled = [
        [maze[i][j] if maze[i][j] != "O" else "." for j in range(len(maze[i]))]
            for i in range(len(maze))
    ]
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == "#":
                lowest_x[i] = j + 1
            if maze[i][j] == "O":
                filled[i][lowest_x[i]] = "O"
                lowest_x[i] += 1
    return filled

def tilt_east(maze: List[str]) -> List[str]:
    highest_x = [len(maze) - 1 for _ in range(len(maze))]
    filled = [
        [maze[i][j] if maze[i][j] != "O" else "." for j in range(len(maze[i]))]
            for i in range(len(maze))
    ]
    for i in range(len(maze) - 1, -1, -1):
        for j in range(len(maze[i]) - 1, -1, -1):
            if maze[i][j] == "#":
                highest_x[i] = j - 1
            if maze[i][j] == "O":
                filled[i][highest_x[i]] = "O"
                highest_x[i] -= 1
    return filled 


def get_load(maze: List[int]) -> int:
    res = 0
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == "O":
                res += len(maze) - i
    return res


def part1(maze: List[str]) -> int:
    north = tilt_north(maze)
    return get_load(north)


def cycle(maze) -> List[str]:
    return tilt_east(tilt_south(tilt_west(tilt_north(maze))))


def get_maze_hash(maze):
    return "".join("".join(l) for l in maze)


def part2(maze: List[str]) -> int:
    seen = {}
    scores = []
    non_rep = []
    rep = []
    for i in range(1000):
        maze = cycle(maze)
        score = get_load(maze)
        maze_hash = get_maze_hash(maze)
        if maze_hash in seen:
            start_idx = seen[maze_hash]
            non_rep = scores[:start_idx]
            rep = scores[start_idx:]
            break
        else:
            seen[get_maze_hash(maze)] = i
        scores.append(score)
    print(non_rep, rep)
    return rep[(1_000_000_000 - len(non_rep) - 1) % len(rep)]


if __name__ == "__main__":
    file_name = "d14-input.text"
    # file_name = "test_input.text"
    maze = []
    with open(file_name, "r") as f:
        l = f.readline().strip()
        while l:
            maze.append(l)
            l = f.readline().strip()

    print(part1(maze))
    print(part2(maze))