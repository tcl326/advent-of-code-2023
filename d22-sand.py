from typing import List, Tuple, Dict, Set
import collections


def parse_line(line: str) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
    s, e = line.split("~")
    return tuple([int(i) for i in reversed(s.split(","))]), tuple([int(i) for i in reversed(e.split(","))])


def get_graph(snapshots: List[Tuple[Tuple[int, int, int], Tuple[int, int, int]]]) -> int:
    z_sorted = sorted(snapshots)
    min_height = {}
    z_view = {}
    graph = {}
    for code, ((sz, sy, sx), (ez, ey, ex)) in enumerate(z_sorted):
        code = chr(ord('A') + code)
        height = 0
        deps = set()
        for i in range(sx, ex + 1):
            for j in range(sy, ey + 1):
                if (i, j) in min_height:
                    m_height = min_height[(i, j)] + ez - sz + 1
                    if m_height > height:
                        deps = set([z_view[(i, j)]])
                        height = m_height
                    if m_height == height:
                        deps.add(z_view[(i, j)])
                else:
                    if height:
                        continue
                    height = 1 + ez - sz
        graph[code] = deps
        for i in range(sx, ex + 1):
            for j in range(sy, ey + 1):
                min_height[(i, j)] = height        
                z_view[(i, j)] = code
    return graph


def part1(graph: Dict[str, Set[str]]) -> int:
    can_be_removed = set(graph.keys())

    for k in graph:
        if len(graph[k]) == 1:
            for c in graph[k]:
                can_be_removed.discard(c)
    
    return len(can_be_removed)


def part2(graph: Dict[str, Set[str]]) -> int:
    depends = graph
    supports = collections.defaultdict(set)

    for n, deps in depends.items():
        for d in deps:
            supports[d].add(n)

    def would_fall(d: str):
        fallen = set()
        queue = collections.deque([d])
        while queue:
            n = queue.popleft()
            fallen.add(n)
            for s in supports[n]:
                # get all the nodes supported by 'd'
                if set(depends[s]) - fallen:
                    # if the supported node has more than one support it won't fall
                    continue
                # if the supported node is only supported by 'd' it will fall
                fallen.add(s)
                queue.append(s)
        return len(fallen) - 1

    res = 0
    for d in depends.keys():
        res += would_fall(d)
    return res



if __name__ == "__main__":
    file_name = "d22-input.text"
    # file_name = "test_input.text"
    snapshots = []
    with open(file_name, "r") as f:
        line = f.readline()
        while line:
            snapshots.append(parse_line(line.strip()))
            line = f.readline()
    graph = get_graph(snapshots)
    print(part1(graph))
    print(part2(graph))