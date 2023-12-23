from typing import List
import heapq
import collections
import sys

sys.setrecursionlimit(10000)

direction_mapping = {
    ".": [(0, 1), (1, 0), (0, -1), (-1, 0)],
    ">": [(0, 1)],
    "v": [(1, 0)],
    "^": [(-1, 0)],
    "<": [(0, -1)],
    "#": []
}

direction_mapping_v2 = {
    ".": [(0, 1), (1, 0), (0, -1), (-1, 0)],
    ">": [(0, 1), (1, 0), (0, -1), (-1, 0)],
    "v": [(0, 1), (1, 0), (0, -1), (-1, 0)],
    "^": [(0, 1), (1, 0), (0, -1), (-1, 0)],
    "<": [(0, 1), (1, 0), (0, -1), (-1, 0)],
    "#": []
}





def part2(maze: List[str], direction_mapping=direction_mapping):
    groups = collections.defaultdict(list)
    intersections = set()
    seen = set()
    g_id = 0
    queue = [(g_id, (0, 1))]
    goal_gid = 0
    while queue:
        gid, (i, j) = heapq.heappop(queue)
        if i == len(maze) - 1:
            goal_gid = gid
        if (i, j) in seen:
            continue
        seen.add((i, j))
        neighbours = []
        found = 0
        for di, dj in direction_mapping[maze[i][j]]:
            ni, nj = i + di, j + dj
            if ni < 0 or ni >= len(maze) or nj < 0 or nj >= len(maze[0]) or maze[ni][nj] == "#":
                continue
            if (ni, nj) in seen:
                found += 1
            else:
                found += 1
                neighbours.append((ni, nj))
        if found == 2:
            groups[gid].append((i, j))
            if neighbours:
                heapq.heappush(queue, (gid, neighbours[0]))
        else:
            intersections.add((i, j))
            for idx, (ni, nj) in enumerate(neighbours):
                g_id += 1
                heapq.heappush(queue, (g_id, (ni, nj)))

    print(intersections)

    connections = collections.defaultdict(set)
    for ci, cj in intersections:
        group_sets = set()
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ni, nj = di + ci, dj + cj
            for gid, group in groups.items():
                if group[0] == (ni, nj) or group[-1] == (ni, nj):
                    connections[(ci, cj)].add(gid)

    print("connections:", connections)
    print([(gid, len(group)) for gid, group in groups.items()])
    seen_gid = set([1])
    seen_intersection = set()
    max_len = [0]
    def dfs(gid, end, path_len, goal_gid, path):
        if gid == goal_gid:
            if max_len[0] < path_len:
                print(path_len, path)
                max_len[0] = path_len
            return path_len, path
        v = 0
        vpath = []
        ci, cj = end
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ni, nj = di + ci, dj + cj
            if (ni, nj) in connections and (ni, nj) not in seen_intersection:
                seen_intersection.add((ni, nj))
                for ngid in connections[(ni, nj)]:
                    if ngid in seen_gid:
                        continue
                    seen_gid.add(ngid)
                    gi, gj = groups[ngid][0]
                    if abs(gi - ni + gj - nj) == 1:
                        end = groups[ngid][-1]
                    else:
                        end = groups[ngid][0]
                    r, rp = dfs(ngid, end, path_len + len(groups[ngid]) + 1, goal_gid, path + [ngid])
                    if v < r:
                        v = r
                        vpath = rp
                    seen_gid.discard(ngid)
                seen_intersection.discard((ni, nj))
        return v, vpath

    v, path = dfs(1, groups[1][-1], len(groups[1]), goal_gid, [1])

    to_print = [[m for m in l] for l in maze]

    # path = [1, 2, 4, 8, 16, 27, 26, 25, 38, 54, 68, 57, 43, 44, 46, 31, 18, 10, 6, 7, 13, 21, 23, 24, 37, 50, 49, 63, 65, 75, 80, 78, 77, 84]
    for idx, gid in enumerate(path):
        for i, j in groups[gid]:
            to_print[i][j] = str(idx % 10)
        
    for p in to_print:
        print("".join(p))

    return v + 1, path



if __name__ == "__main__":
    file_name = "d23-input.text"
    # file_name = "test_input.text"
    maze = []
    with open(file_name, "r") as f:
        line = f.readline()
        while line:
            maze.append(line.strip())
            line = f.readline()
    
    # print(part1(maze))
    print(part2(maze, direction_mapping_v2))