from typing import List
import heapq


directions = {
    'r': (0, 1),
    'l': (0, -1),
    'u': (-1, 0),
    'd': (1, 0),
}


def part1(heatloss: List[List[int]]) -> int:
    n = len(heatloss)
    m = len(heatloss[0])
    
    queue = [(0, (0, 0, 'r', 0), ''), (0, (0, 0, 'd', 0), '')]
    seen = set([t for _, t, _ in queue])
    c = 0
    while queue:
        c += 1
        score, (i, j, d, dc), p = heapq.heappop(queue)
        if i == n - 1 and j == m - 1:
            return score, p
        for nd, (di, dj) in directions.items():
            if ( d == 'u' and nd == 'd') or ( d == 'd' and nd == 'u' ) or ( d == 'l' and nd == 'r' ) or ( d == 'r' and nd == 'l' ):
                continue
            if ( dc > 2 and nd == d):
                continue
            ni, nj = i + di, j + dj
            if ni < 0 or ni >= n or nj < 0 or nj >= m:
                continue
            tup = (ni, nj, nd, 1 if nd != d else dc + 1)
            if tup in seen:
                continue
            else:
                seen.add(tup)
            heapq.heappush(queue, (score + heatloss[ni][nj], tup, p + nd))



def part2(heatloss: List[List[int]]) -> int:
    n = len(heatloss)
    m = len(heatloss[0])
    
    queue = [(0, (0, 0, 'r', 0), ''), (0, (0, 0, 'd', 0), '')]
    seen = set([t for _, t, _ in queue])
    c = 0
    while queue:
        c += 1
        score, (i, j, d, dc), p = heapq.heappop(queue)
        if i == n - 1 and j == m - 1:
            if dc < 4:
                continue
            return score, p
        for nd, (di, dj) in directions.items():
            if ( d == 'u' and nd == 'd') or ( d == 'd' and nd == 'u' ) or ( d == 'l' and nd == 'r' ) or ( d == 'r' and nd == 'l' ):
                continue
            if (dc > 9 and nd == d):
                continue
            if (dc < 4 and nd != d):
                continue
            ni, nj = i + di, j + dj
            if ni < 0 or ni >= n or nj < 0 or nj >= m:
                continue
            tup = (ni, nj, nd, 1 if nd != d else dc + 1)
            if tup in seen:
                continue
            else:
                seen.add(tup)
            heapq.heappush(queue, (score + heatloss[ni][nj], tup, p + nd))



if __name__ == "__main__":
    file_name = "d17-input.text"
    # file_name = "test_input.text"
    heatloss = []
    with open(file_name, "r") as f:
        line = f.readline()
        while line:
            heatloss.append([int(l) for l in line.strip()])
            line = f.readline()

    print(part1(heatloss))
    print(part2(heatloss))
